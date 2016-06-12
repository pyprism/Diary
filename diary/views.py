from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, TagSerializer, NotesSerializer, DiarySerializer, SecretSerializer
from .models import Tag, Diary, Notes, Secret
from django.core import serializers
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import status


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

    @list_route(methods=['get'])
    def cloud(self, request, *args, **kwargs):
        """
        Get tag cloud items
        """
        cloud = {}
        tags = Tag.objects.all()
        for i in tags:
            hiren = Diary.objects.filter(tag=i).count()
            cloud[i.name] = hiren
        return Response(cloud)


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


class SecretViewset(viewsets.ModelViewSet):
    """
        API endpoint that allows secret key  to be created, viewed ,edited and deleted.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Secret.objects.all()
    serializer_class = SecretSerializer

    def create(self, request, *args, **kwargs):
        """
        Check if secret key already created
        """
        count = Secret.objects.all().count()
        if count == 1:
            content = {'error': 'key already exits'}
            return Response(content, status.HTTP_403_FORBIDDEN)
        else:
            instance = self.get_object()
            Secret.objects.create(key=instance)
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        bunny = {'error': 'method not supported :/'}
        return Response(bunny, status.HTTP_403_FORBIDDEN)



