from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
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
    mobile = models.CharField(max_length=15, null=True, blank=True, unique=True)
    full_name = models.CharField(max_length=150, null=True, blank=True)
    primary_address = models.CharField(max_length=250, null=True, blank=True)
    secondary_address = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    business_name = models.CharField(max_length=50, null=True, blank=True)
    business_details = models.CharField(max_length=250, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Contactus(models.Model):
    Name = models.CharField(max_length=30, null=False, blank=True)
    Email = models.EmailField(null=False, blank=True)
    Mobile = models.IntegerField(null=True, blank=True)
    Message = models.CharField(max_length=3000, null=False, blank=True)


class ShippingRegistration(models.Model):
    objects = None
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE ,null=False)
    Shipping_choices = [
        ('TRACKON', 'TRACKON'),
        ('DTDC', 'DTDC'),
        ('SPEED POST', 'SPEED POST'),
        ('PROFESSIONAL', 'PROFESSIONAL'),
    ]
    Shipping_Through = models.CharField(max_length=15, choices=Shipping_choices)
    Name = models.CharField(max_length=20, blank=False)
    Mobile = models.IntegerField(blank=False)
    Pin_Code = models.IntegerField(blank=False)
    City = models.CharField(max_length=50, blank=False)
    Address = models.CharField(max_length=250, blank=False)
    Consignment_Choices = [
        ('Document', 'Document'),
        ('Non Document', 'Non Document'),
    ]

    Consignment = models.CharField(max_length=20, blank=False, choices=Consignment_Choices)
    ContentType_Choices = [
        ('ARTIFICIAL JWELLARY', 'ARTIFICIAL JWELLARY'),
        ('BAGS', 'BAGS'),
        ('BOOKS', 'BOOKS'),
        ('CLOTHING', 'CLOTHING'),
        ('CORPORATE GIFTS', 'CORPORATE GIFTS'),
        ('LUGGAGE', 'LUGGAGE'),
        ('PERFUMES', 'PERFUMES'),
        ('PHOTO FRAME', 'PHOTO FRAME'),
        ('RAKHI', 'RAKHI'),
        ('SHOES', 'SHOES'),
        ('SLIPPERS', 'SLIPPERS'),
    ]
    Content_Type = models.CharField(max_length=20, blank=False, choices=ContentType_Choices)
    Number_of_box = models.IntegerField(blank=False)
    Declared_value = models.IntegerField(blank=False)
    Booking_date = models.DateField(auto_now_add=True)
    Delivery_date = models.DateField()
