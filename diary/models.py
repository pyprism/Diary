from django.db import models
from taggit.managers import TaggableManager


class Diary(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    date = models.DateTimeField()
    tag = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Notes(models.Model):
    content = models.TextField()
    date = models.DateTimeField()
    tag = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

