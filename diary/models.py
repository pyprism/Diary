from django.db import models


class Diary(models.Model):
    title = models.CharField()
    content = models.TextField()
    date = models.DateTimeField()


class Notes(models.Model):
    content = models.TextField()
    date = models.DateTimeField()