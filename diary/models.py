from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Diary(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    date = models.DateTimeField()
    tag = models.ForeignKey('Tag')


class Notes(models.Model):
    content = models.TextField()
    date = models.DateTimeField()
    tag = models.ForeignKey('Tag')
