from django.db import models
from taggit.managers import TaggableManager
from django.utils import timezone


class Diary(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    iv = models.CharField(max_length=500)
    salt = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)
    tag = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Notes(models.Model):
    content = models.TextField()
    iv = models.CharField(max_length=500)
    salt = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)
    tag = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

