from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, null=True, blank=True,unique=True)
    full_name = models.CharField(max_length=150, null=True, blank=True)
    primary_address = models.CharField(max_length=250, null=True, blank=True)
    secondary_address = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    pincode = models.IntegerField( null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email