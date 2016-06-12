from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=500, unique=True)


class Diary(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    date = models.DateTimeField()
    tag = models.ForeignKey('Tag', null=True)


class Notes(models.Model):
    content = models.TextField()
    date = models.DateTimeField()
    tag = models.ForeignKey('Tag', null=True)


class Secret(models.Model):
    key = models.CharField(max_length=500)
