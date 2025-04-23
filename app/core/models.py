from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin','Admin'),
        ('patient','Patient'),
        ('premium_patient','Premium_Patient'),
    )
    fullname = models.CharField(max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=100,choices=ROLE_CHOICES,default='patient')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['fullname']

    objects = CustomUserManager()

    def __str__(self):
        return self.email