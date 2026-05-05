import logging
import uuid

from celery.exceptions import CeleryError
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework import viewsets, views, status, permissions
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from diary.filters import DiaryFilter
from diary.models import Tag, Diary, ShareLink, DiaryAnalysis
from diary.serializers import (
    TagSerializer,
    TaggedDiaryEntrySerializer,
    DiarySerializer,
    DiaryListSerializer,
    DiaryAnalysisSerializer,
    PresignSerializer,
    ImageUploadSerializer,
    ImageReadUrlSerializer,
    ShareLinkCreateSerializer,
    ShareLinkSerializer,
    PublicShareSerializer,
)
from utils.enums import AnalysisStatus
from utils.file_convert import convert_image_to_web
from utils.s3 import get_s3_uploader

logger = logging.getLogger(__name__)
ANALYSIS_POLL_SECONDS = 10


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.get_all_tags()
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        return Tag.objects.get_all_tags(self.request.user)

    @action(detail=True, methods=["get"], url_path="entries")
    def entries(self, request, pk=None):
        tag = self.get_object()
        entries = (
            Diary.objects.filter(user=request.user, tags=tag)
            .only("id", "title", "date")
            .order_by("-date", "-id")
        )
        serializer = TaggedDiaryEntrySerializer(entries, many=True)
        return Response(
            {
                "tag": {
                    "pk": tag.pk,
                    "name": tag.name,
                },
                "entries": serializer.data,
            }
        )


class DiaryViewSet(viewsets.ModelViewSet):
    queryset = Diary.objects.get_all_diaries()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DiaryFilter
    ordering_fields = ["date", "created_at", "title"]
    ordering = ["-date"]

    def get_serializer_class(self):
        if self.action == "list":
            return DiaryListSerializer
        return DiarySerializer

    def get_queryset(self):
        return Diary.objects.get_all_diaries(self.request.user)

    def perform_create(self, serializer):
        """Save the diary entry and immediately dispatch the LLM analysis task."""
        diary = serializer.save()
        self._dispatch_analysis(diary)

    def perform_update(self, serializer):
        should_refresh_analysis = "content" in serializer.validated_data
        diary = serializer.save()
        if should_refresh_analysis:
            self._dispatch_analysis(diary)

    def destroy(self, request, *args, **kwargs):
        diary = self.get_object()
        image_urls = _extract_image_urls(diary.content)
        failed_urls = []
        if image_urls:
            uploader = get_s3_uploader()
            managed_image_urls = [
                url for url in image_urls if uploader.is_managed_url(url)
            ]
            failed_urls = [
                url for url in managed_image_urls if not uploader.delete_file(url)
            ]
        if failed_urls:
            return Response(
                {
                    "detail": "Failed to delete one or more diary images.",
                    "failed_images": failed_urls,
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        diary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get", "post"], url_path="analyze")
    def analyze(self, request, pk=None):
        """
        GET  /api/v1/diaries/{id}/analyze  → return current analysis status/result
        POST /api/v1/diaries/{id}/analyze  → (re-)trigger LLM analysis task
        """
        diary = self.get_object()  # enforces ownership via get_queryset

        if request.method == "POST":
            analysis = DiaryAnalysis.objects.get_for_diary(diary)
            force = request.data.get("force") is True
            if (
                analysis
                and analysis.status
                in (
                    AnalysisStatus.PENDING,
                    AnalysisStatus.PROCESSING,
                )
                and not force
            ):
                return self._analysis_response(
                    analysis,
                    response_status=status.HTTP_202_ACCEPTED,
                )

            analysis = self._dispatch_analysis(diary)
            return self._analysis_response(
                analysis,
                response_status=status.HTTP_202_ACCEPTED,
            )

        # GET
        analysis = DiaryAnalysis.objects.get_for_diary(diary)
        if analysis is None:
            return Response(
                {"detail": "No analysis found. POST to this endpoint to trigger one."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return self._analysis_response(analysis)

    # private helper
    @staticmethod
    def _dispatch_analysis(diary):
        """Create/reset the analysis record and enqueue the Celery task."""
        # Import task lazily to avoid circular imports
        from diary.tasks import analyze_diary_task

        # Create a PENDING record first so the client can poll immediately
        analysis, _ = DiaryAnalysis.objects.get_or_create_for_diary(diary)
        task_id = uuid.uuid4().hex
        analysis.status = "PENDING"
        analysis.error = ""
        analysis.task_id = task_id
        analysis.save(update_fields=["status", "error", "task_id", "updated_at"])

        try:
            analyze_diary_task.apply_async(args=[diary.pk], task_id=task_id)
        except (CeleryError, OSError) as exc:
            logger.exception("Failed to dispatch analysis task for diary %s", diary.pk)
            analysis.status = "FAILED"
            analysis.error = f"Failed to dispatch analysis task: {exc}"
            analysis.save(update_fields=["status", "error", "updated_at"])
        return analysis

    @staticmethod
    def _analysis_response(analysis, response_status=status.HTTP_200_OK):
        response = Response(
            DiaryAnalysisSerializer(analysis).data,
            status=response_status,
        )
        if analysis.status in (AnalysisStatus.PENDING, AnalysisStatus.PROCESSING):
            response["Retry-After"] = str(ANALYSIS_POLL_SECONDS)
        return response


def _extract_image_urls(content):
    if not isinstance(content, dict):
        return []

    urls = []
    seen = set()
    for block in content.get("blocks", []):
        if not isinstance(block, dict) or block.get("type") != "image":
            continue
        url = block.get("url")
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            continue
        if url in seen:
            continue
        seen.add(url)
        urls.append(url)
    return urls


class HomepageViewSet(viewsets.ViewSet):
    """
    Homepage API: returns diary entry titles from previous years.

    - If entries exist for today's month/day in past years, return those.
    - Otherwise return entries from the next available date in past years.
    """

    permission_classes = [IsAuthenticated]

    def list(self, request):
        today = timezone.now().date()
        user = request.user

        entries = Diary.objects.get_on_this_day(user, today)

        if entries.exists():
            matched_date = {"month": today.month, "day": today.day}
            is_exact = True
        else:
            entries = Diary.objects.get_next_available_in_past_years(user, today)
            if entries.exists():
                first_entry = entries.first()
                matched_date = {
                    "month": first_entry.date.month,
                    "day": first_entry.date.day,
                }
            else:
                matched_date = None
            is_exact = False

        serializer = DiaryListSerializer(entries, many=True)
        return Response(
            {
                "is_exact_date": is_exact,
                "matched_date": matched_date,
                "entries": serializer.data,
            }
        )


class PresignView(views.APIView):
    """
    POST /api/v1/uploads/presign/

    Request body: { "filename": "photo.jpg", "content_type": "image/jpeg" }
    Returns a presigned S3 PUT URL for direct upload from the Flutter app.
    After uploading, insert the returned URL into the diary content JSON.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PresignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        filename = serializer.validated_data["filename"]
        content_type = serializer.validated_data["content_type"]

        uploader = get_s3_uploader()
        result = uploader.generate_presigned_upload_url(
            user_id=request.user.pk,
            filename=filename,
            content_type=content_type,
            category="diary-images",
        )

        if result is None:
            return Response(
                {"detail": "Failed to generate upload URL. S3 may not be configured."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(result, status=status.HTTP_200_OK)


class ImageUploadView(views.APIView):
    """
    POST /api/v1/uploads/image/

    Multipart body: { "image": <file> }
    Converts the image to WebP on the backend, uploads it to R2, and returns
    the stable private object URL for diary content.
    """

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        filename, content = convert_image_to_web(serializer.validated_data["image"])
        url = get_s3_uploader().upload_file(
            content,
            user_id=request.user.pk,
            category="diary-images",
            filename=filename,
        )
        if url is None:
            return Response(
                {"detail": "Failed to upload image. S3 may not be configured."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            {"file_url": url, "filename": filename, "content_type": "image/webp"},
            status=status.HTTP_201_CREATED,
        )


class ImageReadUrlView(views.APIView):
    """
    POST /api/v1/uploads/read-url/

    Request body: { "url": "https://..." }
    Returns a short-lived presigned GET URL for displaying private R2 images.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ImageReadUrlSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data["url"]
        signed_url = get_s3_uploader().generate_presigned_url(url, expiration=3600)
        if signed_url is None:
            return Response(
                {"detail": "Unable to sign image URL."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"url": signed_url}, status=status.HTTP_200_OK)


class ShareLinkViewSet(viewsets.ViewSet):
    """
    Authenticated endpoints for managing share links on the owner's diary entries.

    list   GET  /api/v1/diaries/{diary_pk}/shares/
    create POST /api/v1/diaries/{diary_pk}/shares/
    detail GET  /api/v1/diaries/{diary_pk}/shares/{token}/
    delete DEL  /api/v1/diaries/{diary_pk}/shares/{token}/
    """

    permission_classes = [IsAuthenticated]

    def _get_diary(self, request, diary_pk):
        try:
            return Diary.objects.get(pk=diary_pk, user=request.user)
        except Diary.DoesNotExist:
            return None

    def list(self, request, diary_pk=None):
        diary = self._get_diary(request, diary_pk)
        if diary is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        shares = ShareLink.objects.get_all_for_user(request.user).filter(diary=diary)
        serializer = ShareLinkSerializer(
            shares, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def create(self, request, diary_pk=None):
        diary = self._get_diary(request, diary_pk)
        if diary is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ShareLinkCreateSerializer(
            data=request.data, context={"diary": diary}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        share = ShareLink.objects.create_share(
            diary=diary,
            user=request.user,
            expiry_seconds=data["expiry_seconds"],
            share_type=data["share_type"],
            excerpt=data.get("excerpt", ""),
        )
        return Response(
            ShareLinkSerializer(share, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, diary_pk=None, pk=None):
        diary = self._get_diary(request, diary_pk)
        if diary is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            share = ShareLink.objects.get(
                token=pk, diary=diary, created_by=request.user
            )
        except ShareLink.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(ShareLinkSerializer(share, context={"request": request}).data)

    def destroy(self, request, diary_pk=None, pk=None):
        diary = self._get_diary(request, diary_pk)
        if diary is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            share = ShareLink.objects.get(
                token=pk, diary=diary, created_by=request.user
            )
        except ShareLink.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        share.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CurrentUserShareListView(views.APIView):
    """
    GET /api/v1/shares/
    Return every share link created by the current user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        shares = ShareLink.objects.get_all_for_user(request.user)
        serializer = ShareLinkSerializer(
            shares, many=True, context={"request": request}
        )
        return Response(serializer.data)


class PublicShareView(views.APIView):
    """
    GET /api/v1/share/{token}/
    No authentication required.  Returns shared content if the link is still valid.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        share = ShareLink.objects.get_valid(token)
        if share is None:
            return Response(
                {"detail": "This link is invalid or has expired."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PublicShareSerializer(share)
        return Response(serializer.data)
