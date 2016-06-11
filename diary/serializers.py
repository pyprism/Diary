from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Diary, Notes, Tag, Secret


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes


class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary


class SecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret

