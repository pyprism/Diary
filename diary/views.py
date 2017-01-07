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


class NotesViewset(viewsets.ModelViewSet):
    """
        API endpoint that allows notes to be created, viewed ,edited and deleted.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer


class DiaryViewset(viewsets.ModelViewSet):
    """
        API endpoint that allows diary to be created, viewed ,edited and deleted.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
