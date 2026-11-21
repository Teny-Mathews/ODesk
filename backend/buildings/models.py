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
    amenities = models.ManyToManyField('Amenity',blank=True,related_name='buildings')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.building_name


class OfficeSpace(models.Model):

    STATUS_CHOICES = (('available', 'Available'),('rented', 'Rented'),('maintenance', 'Maintenance'),)
    building = models.ForeignKey(Building,on_delete=models.CASCADE,related_name='office_spaces')
    office_number = models.CharField(max_length=50)
    area_sqft = models.PositiveIntegerField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='available')
    description = models.TextField(blank=True)
    amenities = models.ManyToManyField('Amenity',blank=True,related_name='office_spaces')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('building', 'office_number')

    def __str__(self):
        return f"{self.office_number} - {self.building.building_name}"



class BuildingImage(models.Model):

    building = models.ForeignKey(Building,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='buildings/')
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.building.building_name}"
    

class OfficeImage(models.Model):

    office_space = models.ForeignKey(OfficeSpace,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='offices/')
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.office_space.office_number}"


class Amenity(models.Model):

    AMENITY_TYPE_CHOICES = (('building', 'Building'),('office', 'Office'),('both', 'Both'),)

    name = models.CharField(max_length=100, unique=True)
    amenity_type = models.CharField(max_length=10,choices=AMENITY_TYPE_CHOICES,default='both')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.amenity_type}"

