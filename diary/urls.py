from django.urls import re_path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("tags", views.TagViewSet, basename="tags")
router.register("diaries", views.DiaryViewSet, basename="diaries")
router.register("homepage", views.HomepageViewSet, basename="homepage")

# Nested share routes under /api/v1/diaries/{diary_pk}/shares/
share_router = routers.DefaultRouter()
share_router.register("shares", views.ShareLinkViewSet, basename="shares")

urlpatterns = [
    re_path(r"^v1/", include(router.urls)),
    re_path(r"^v1/diaries/(?P<diary_pk>[0-9]+)/", include(share_router.urls)),
    re_path(
        r"^v1/shares/?$",
        views.CurrentUserShareViewSet.as_view({"get": "list"}),
        name="current-user-shares",
    ),
    re_path(
        r"^v1/uploads/presign/?$",
        views.UploadViewSet.as_view({"post": "presign"}),
        name="uploads-presign",
    ),
    re_path(
        r"^v1/uploads/image/?$",
        views.UploadViewSet.as_view({"post": "image"}),
        name="uploads-image",
    ),
    re_path(
        r"^v1/uploads/read-url/?$",
        views.UploadViewSet.as_view({"post": "read_url"}),
        name="uploads-read-url",
    ),
    re_path(
        r"^v1/share/(?P<token>[^/]+)/?$",
        views.PublicShareViewSet.as_view({"get": "retrieve"}),
        name="public-share",
    ),
]
