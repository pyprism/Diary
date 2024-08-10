from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from diary.models import Tag
from diary.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.get_all_tags()
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Tag.objects.get_all_tags(user)
        return queryset



