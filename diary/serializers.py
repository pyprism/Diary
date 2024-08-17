from rest_framework import serializers

from base.models import User
from diary.models import Tag, Diary


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')

    def validate(self, data):
        user = self.context['request'].user
        name = data.get('name')

        # Check if the tag with the same name already exists for this user
        if Tag.objects.is_tag_exists_for_user(user, name):
            raise serializers.ValidationError("A tag with this name already exists for the user.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class DiarySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tags_attach = serializers.ListField(child=serializers.CharField(), write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        tags = data.get('tags_attach')

        # Check if the tag exists for this user
        if tags:
            for tag in tags:
                if not Tag.objects.is_tag_exists_for_user(user, tag):
                    raise serializers.ValidationError(f"The tag {tag} doesn't exists for the user.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        tags_data = validated_data.pop('tags_attach', None, [])
        diary = super().create(validated_data)

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(user=user, name=tag_data)
            diary.tags.add(tag)

        return diary

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags_attach', None)
        instance = super().update(instance, validated_data)

        if tags_data is not None:
            # Clear existing tags
            instance.tags.clear()

            # then add tags to the diary
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(user=self.context['request'].user, name=tag_data)
                instance.tags.add(tag)

        return instance

    class Meta:
        model = Diary
        fields = ('id', 'title', 'created_at', 'updated_at', 'tags', 'content', 'tags_attach')

