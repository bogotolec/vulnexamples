from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import HostsAuthManager


class HostsAuthUser(AbstractUser):
    subdomain = models.TextField(max_length=500, blank=True)
    login = models.TextField(max_length=100, blank=True)
    balance = models.IntegerField(default=10)
    objects = HostsAuthManager()
