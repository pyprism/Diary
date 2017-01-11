from rest_framework import serializers
from .models import Diary, Notes
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer


class NotesSerializer(TaggitSerializer, serializers.ModelSerializer):
    tag = TagListSerializerField()

    class Meta:
        model = Notes
        fields = '__all__'


class DiarySerializer(TaggitSerializer, serializers.ModelSerializer):
    tag = TagListSerializerField()
    
    class Meta:
        model = Diary
        fields = '__all__'


class TagsListSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

