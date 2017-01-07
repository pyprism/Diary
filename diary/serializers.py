from rest_framework import serializers
from .models import Diary, Notes


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'

    # def create(self, validated_data):
    #     print(validated_data)
    #     tags = validated_data.pop('tag')
    #     hiren = Notes.objects.create(**validated_data)
    #     hiren.tag.add(**tags)
    #     return hiren


class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = '__all__'

