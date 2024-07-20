from django.db import models


class TagManager(models.Manager):
    def create_tag(self, user, tag):
        return self.create(user=user, tag=tag)

    def get_tag(self, user, tag):
        return self.filter(user=user, name=tag).first()


class DiaryManager(models.Manager):
    def create_diary(self, user, diary, post_type, tag):
        return self.create(user=user, diary=diary, post_type=post_type, tags=tag)


