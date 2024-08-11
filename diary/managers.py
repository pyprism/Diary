from django.db import models


class TagManager(models.Manager):
    def create_tag(self, user, tag):
        return self.create(user=user, tag=tag)

    def get_tag(self, user, tag):
        return self.filter(user=user, name=tag).first()

    def get_all_tags(self, user=None):
        if user:
            return self.filter(user=user).order_by('name')
        return self.order_by('name')


class DiaryManager(models.Manager):
    def create_diary(self, user, diary, post_type, tag):
        return self.create(user=user, diary=diary, post_type=post_type, tags=tag)

    def get_diary_by_tag(self, user, tag):
        return self.filter(user=user, name=tag).all()


