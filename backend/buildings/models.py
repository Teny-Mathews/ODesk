from django.db import models
from accounts.models import User


class Building(models.Model):

    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='buildings')
    building_name = models.CharField(max_length=150)
    address = models.TextField()
    city = models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.building_name