from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, TagSerializer, NotesSerializer, DiarySerializer
from .models import Tag, Diary, Notes


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows tags to be created, viewed ,edited and deleted.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


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
