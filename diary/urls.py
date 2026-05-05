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
        views.CurrentUserShareListView.as_view(),
        name="current-user-shares",
    ),
    re_path(
        r"^v1/uploads/presign/?$", views.PresignView.as_view(), name="uploads-presign"
    ),
    re_path(
        r"^v1/uploads/image/?$",
        views.ImageUploadView.as_view(),
        name="uploads-image",
    ),
    re_path(
        r"^v1/uploads/read-url/?$",
        views.ImageReadUrlView.as_view(),
        name="uploads-read-url",
    ),
    re_path(
        r"^v1/share/(?P<token>[^/]+)/?$",
        views.PublicShareView.as_view(),
        name="public-share",
    ),
]
