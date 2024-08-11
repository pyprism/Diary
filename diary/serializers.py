from rest_framework import serializers

from base.models import User
from diary.models import Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'created_at', 'updated_at')

    def validate(self, data):
        user = self.context['request'].user
        name = data.get('name')

        # Check if the tag with the same name already exists for this user
        if Tag.objects.filter(user=user, name=name).exists():
            raise serializers.ValidationError("A tag with this name already exists for the user.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


