from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (('owner', 'Owner'),('tenant', 'Tenant'),)

    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='tenant')

    def __str__(self):
        return self.email