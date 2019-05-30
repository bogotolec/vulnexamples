from django.db.models import Model
from django.db import models


class Note(Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=500)
