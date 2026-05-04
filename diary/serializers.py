from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import URLValidator
from rest_framework import serializers

from base.models import User
from diary.models import Tag, Diary, ShareLink, DiaryAnalysis
from utils.enums import AnalysisStatus, ShareType

ALLOWED_BLOCK_TYPES = {
    "heading",
    "paragraph",
    "bullet_list",
    "checklist",
    "quote",
    "divider",
    "image",
}
MAX_BLOCKS = 500
MAX_LIST_ITEMS = 200
MAX_TEXT_LENGTH = 10000


def validate_diary_content_shape(value):
    if not isinstance(value, dict):
        raise serializers.ValidationError("Content must be a JSON object.")

    if "version" not in value:
        raise serializers.ValidationError("Content must include a 'version' field.")

    if not isinstance(value.get("version"), int):
        raise serializers.ValidationError("Content 'version' must be an integer.")

    blocks = value.get("blocks")
    if not isinstance(blocks, list):
        raise serializers.ValidationError("Content must include a 'blocks' list.")

    if len(blocks) > MAX_BLOCKS:
        raise serializers.ValidationError(
            f"Content cannot contain more than {MAX_BLOCKS} blocks."
        )

    for i, block in enumerate(blocks):
        if not isinstance(block, dict):
            raise serializers.ValidationError(f"Block {i} must be an object.")

        block_type = block.get("type")
        if block_type not in ALLOWED_BLOCK_TYPES:
            raise serializers.ValidationError(
                f"Block {i} has unsupported type '{block_type}'. "
                f"Allowed types: {', '.join(sorted(ALLOWED_BLOCK_TYPES))}."
            )

        if block_type in {"heading", "paragraph", "quote"}:
            text = block.get("text")
            if not isinstance(text, str) or not text.strip():
                raise serializers.ValidationError(
                    f"Block {i} ({block_type}) must have a non-empty 'text' string."
                )
            if len(text) > MAX_TEXT_LENGTH:
                raise serializers.ValidationError(
                    f"Block {i} ({block_type}) text is too long."
                )

        if block_type == "heading":
            level = block.get("level")
            if level not in (1, 2, 3):
                raise serializers.ValidationError(
                    f"Block {i} (heading) must have 'level' of 1, 2, or 3."
                )

        if block_type == "bullet_list":
            _validate_text_list(block.get("items"), i, "bullet_list")

        if block_type == "checklist":
            _validate_checklist(block.get("items"), i)

        if block_type == "image":
            url = block.get("url")
            if not isinstance(url, str) or not url.strip():
                raise serializers.ValidationError(
                    f"Block {i} (image) must have a non-empty 'url' string. "
                    "Upload images to S3 first and include the URL."
                )
            _validate_http_url(url, i)

    return value


def _validate_text_list(items, block_index, block_type):
    if not isinstance(items, list):
        raise serializers.ValidationError(
            f"Block {block_index} ({block_type}) must have an 'items' list."
        )
    if len(items) > MAX_LIST_ITEMS:
        raise serializers.ValidationError(
            f"Block {block_index} ({block_type}) cannot contain more than {MAX_LIST_ITEMS} items."
        )
    for item_index, item in enumerate(items):
        if not isinstance(item, str) or not item.strip():
            raise serializers.ValidationError(
                f"Block {block_index} ({block_type}) item {item_index} must be a non-empty string."
            )
        if len(item) > MAX_TEXT_LENGTH:
            raise serializers.ValidationError(
                f"Block {block_index} ({block_type}) item {item_index} is too long."
            )


def _validate_checklist(items, block_index):
    if not isinstance(items, list):
        raise serializers.ValidationError(
            f"Block {block_index} (checklist) must have an 'items' list."
        )
    if len(items) > MAX_LIST_ITEMS:
        raise serializers.ValidationError(
            f"Block {block_index} (checklist) cannot contain more than {MAX_LIST_ITEMS} items."
        )
    for item_index, item in enumerate(items):
        if not isinstance(item, dict):
            raise serializers.ValidationError(
                f"Block {block_index} (checklist) item {item_index} must be an object."
            )
        text = item.get("text")
        if not isinstance(text, str) or not text.strip():
            raise serializers.ValidationError(
                f"Block {block_index} (checklist) item {item_index} must have non-empty text."
            )
        if len(text) > MAX_TEXT_LENGTH:
            raise serializers.ValidationError(
                f"Block {block_index} (checklist) item {item_index} text is too long."
            )
        if not isinstance(item.get("checked"), bool):
            raise serializers.ValidationError(
                f"Block {block_index} (checklist) item {item_index} must have a boolean 'checked'."
            )


def _validate_http_url(url, block_index):
    try:
        URLValidator(schemes=["http", "https"])(url)
    except DjangoValidationError:
        raise serializers.ValidationError(
            f"Block {block_index} (image) must have a valid http(s) URL."
        )


def extract_plain_text(content):
    if not isinstance(content, dict):
        return ""
    parts = []
    for block in content.get("blocks", []):
        if not isinstance(block, dict):
            continue
        block_type = block.get("type")
        if block_type in {"heading", "paragraph", "quote"} and isinstance(
            block.get("text"), str
        ):
            parts.append(block["text"])
        elif block_type == "bullet_list":
            parts.extend(
                item for item in block.get("items", []) if isinstance(item, str)
            )
        elif block_type == "checklist":
            parts.extend(
                item.get("text")
                for item in block.get("items", [])
                if isinstance(item, dict) and isinstance(item.get("text"), str)
            )
    return "\n".join(parts)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")

    def validate(self, data):
        user = self.context["request"].user
        name = data.get("name")

        if name is not None:
            matches = Tag.objects.filter(user=user, name=name)
            if self.instance is not None:
                matches = matches.exclude(pk=self.instance.pk)
            if matches.exists():
                raise serializers.ValidationError(
                    "A tag with this name already exists for the user."
                )

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)


class DiaryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views — title only with key metadata."""

    date = serializers.DateField(format="%d-%m-%Y", input_formats=["%d-%m-%Y"])

    class Meta:
        model = Diary
        fields = ("id", "title", "date", "post_type")


class TaggedDiaryEntrySerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = Diary
        fields = ("pk", "title")


class DiarySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tags_attach = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    date = serializers.DateField(format="%d-%m-%Y", input_formats=["%d-%m-%Y"])

    class Meta:
        model = Diary
        fields = (
            "id",
            "title",
            "date",
            "post_type",
            "content",
            "tags",
            "tags_attach",
            "created_at",
            "updated_at",
        )

    def validate_content(self, value):
        return validate_diary_content_shape(value)

    def validate(self, data):
        user = self.context["request"].user
        tags = data.get("tags_attach")

        if tags:
            for tag in tags:
                if not Tag.objects.is_tag_exists_for_user(user, tag):
                    raise serializers.ValidationError(
                        f"The tag '{tag}' doesn't exist for this user."
                    )

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        tags_data = validated_data.pop("tags_attach", [])
        diary = super().create(validated_data)

        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(user=user, name=tag_name)
            diary.tags.add(tag)

        return diary

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags_attach", None)
        instance = super().update(instance, validated_data)

        if tags_data is not None:
            instance.tags.clear()
            for tag_name in tags_data:
                tag, _ = Tag.objects.get_or_create(
                    user=self.context["request"].user, name=tag_name
                )
                instance.tags.add(tag)

        return instance


class PresignSerializer(serializers.Serializer):
    filename = serializers.CharField(max_length=255)
    content_type = serializers.CharField(max_length=100)

    def validate_content_type(self, value):
        allowed_prefixes = ("image/",)
        if not any(value.startswith(prefix) for prefix in allowed_prefixes):
            raise serializers.ValidationError(
                "Only image uploads are allowed via presigned URLs."
            )
        return value


class ShareLinkCreateSerializer(serializers.Serializer):
    """Input serializer for creating a share link."""

    share_type = serializers.ChoiceField(
        choices=ShareType.choices, default=ShareType.FULL
    )
    excerpt = serializers.CharField(required=False, allow_blank=True, default="")
    expiry_seconds = serializers.IntegerField(
        required=False,
        min_value=60,
        max_value=60 * 60 * 24 * 30,  # 30 days max
    )

    def validate(self, data):
        if "expiry_seconds" not in data:
            data["expiry_seconds"] = settings.SHARE_LINK_EXPIRY_SECONDS
        if data["share_type"] == "EXCERPT" and not data.get("excerpt"):
            raise serializers.ValidationError(
                "An 'excerpt' is required for EXCERPT share type."
            )
        if data["share_type"] == "EXCERPT":
            excerpt = data.get("excerpt", "").strip()
            diary = self.context.get("diary")
            if diary is None or excerpt not in extract_plain_text(diary.content):
                raise serializers.ValidationError(
                    "The excerpt must be copied from the diary content."
                )
            data["excerpt"] = excerpt
        else:
            data["excerpt"] = ""
        return data


class ShareLinkSerializer(serializers.ModelSerializer):
    """Read serializer for the owner's view of a share link."""

    is_expired = serializers.BooleanField(read_only=True)
    diary_id = serializers.IntegerField(source="diary.id", read_only=True)
    diary_title = serializers.CharField(source="diary.title", read_only=True)
    public_url = serializers.SerializerMethodField()

    class Meta:
        model = ShareLink
        fields = (
            "id",
            "token",
            "share_type",
            "excerpt",
            "diary_id",
            "diary_title",
            "expires_at",
            "is_expired",
            "created_at",
            "public_url",
        )
        read_only_fields = fields

    def get_public_url(self, obj):
        request = self.context.get("request")
        path = f"/api/v1/share/{obj.token}"
        if request:
            return request.build_absolute_uri(path)
        return path


class PublicShareSerializer(serializers.ModelSerializer):
    """Public serializer — no auth required, exposes only safe fields."""

    diary_title = serializers.CharField(source="diary.title", read_only=True)
    diary_date = serializers.DateField(
        source="diary.date", read_only=True, format="%d-%m-%Y"
    )
    content = serializers.SerializerMethodField()

    class Meta:
        model = ShareLink
        fields = ("share_type", "diary_title", "diary_date", "content", "expires_at")

    def get_content(self, obj):
        if obj.share_type == "EXCERPT":
            return obj.excerpt
        return obj.diary.content


class DiaryAnalysisSerializer(serializers.ModelSerializer):
    """Read-only serializer for the analysis result of a diary entry."""

    retry_after_seconds = serializers.SerializerMethodField()

    class Meta:
        model = DiaryAnalysis
        fields = (
            "status",
            "mood",
            "summary",
            "bangla_content",
            "task_id",
            "error",
            "retry_after_seconds",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields

    def get_retry_after_seconds(self, obj):
        if obj.status in (AnalysisStatus.PENDING, AnalysisStatus.PROCESSING):
            return 10
        return None
