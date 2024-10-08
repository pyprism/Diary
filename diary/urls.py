from django.urls import re_path, include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('tags', views.TagViewSet, basename='tags')

urlpatterns = [
    re_path(r'^v1/', include(router.urls)),
]
