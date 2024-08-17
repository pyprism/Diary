from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from diary.models import Tag, Diary
from diary.serializers import TagSerializer, DiarySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.get_all_tags()
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Tag.objects.get_all_tags(user)
        return queryset


class DiaryViewSet(viewsets.ModelViewSet):
    queryset = Diary.objects.get_all_diaries()
    permission_classes = [IsAuthenticated]
    serializer_class = DiarySerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Diary.objects.get_all_diaries(user)
        return queryset
