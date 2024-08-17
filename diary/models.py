from django.contrib.auth import get_user_model
from django.db import models

from diary.managers import TagManager, DiaryManager


class Tag(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=50, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TagManager()

    def __str__(self):
        return self.name


POST_TYPE_CHOICES = (
    ('SHORT', 'Short'),
    ('LONG', 'Long'),
)


class Diary(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    post_type = models.CharField(max_length=50, choices=POST_TYPE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = DiaryManager()

    def __str__(self):
        return self.title


