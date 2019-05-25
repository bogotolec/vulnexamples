from django.db.models import Model
from django.db import models


class AdditionalInfo(Model):
    login = models.CharField(max_length=70)
    birthdate = models.DateField(blank=True, null=True)
    birthdate_hidden = models.BooleanField(default=False)
    bio = models.CharField(max_length=500, blank=True, null=True)
