from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import NotesSerializer, DiarySerializer
from .models import Diary, Notes
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import ListModelMixin
from django.core import serializers


class NotesViewset(viewsets.ModelViewSet, ListModelMixin):
    """
        API endpoint that allows notes to be created, viewed ,edited and deleted.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        if 'tags' in self.request.data:
            instance.tag.set(*self.request.data['tags'])

    def list(self, request, *args, **kwargs):
        notes = Notes.objects.all()
        data = serializers.serialize('json', notes)
        content = {'hiren': data}
        return Response(content)


class DiaryViewset(viewsets.ModelViewSet):
    """
        API endpoint that allows diary to be created, viewed ,edited and deleted.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
