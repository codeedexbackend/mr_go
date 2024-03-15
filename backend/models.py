from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    # Add additional fields for normal sign up
    # For example:
    full_name = models.TextField(max_length=500, blank=True)
