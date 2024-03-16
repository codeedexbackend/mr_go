from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        username = extra_fields.pop('username', None) 
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, null=True, blank=True,unique=True)
    full_name = models.CharField(max_length=150, null=True, blank=True)
    primary_address = models.CharField(max_length=250, null=True, blank=True)
    secondary_address = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    pincode = models.IntegerField( null=True, blank=True)
    business_name = models.CharField(max_length=50, null=True, blank=True)
    business_details = models.CharField(max_length=250, null=True, blank=True)
    
    objects = CustomUserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email