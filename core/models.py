import random
import string
from django.db import models
from django.contrib.auth.models import User

def generate_unique_id(prefix):
    return f"{prefix}-{''.join(random.choices(string.ascii_uppercase, k=4))}"

class Truck(models.Model):
    id = models.CharField(max_length=6, primary_key=True, editable=False, unique=True)
    number_plate = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=50)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, default="available")

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_id('V')
        super().save(*args, **kwargs)

class Driver(models.Model):
    id = models.CharField(max_length=6, primary_key=True, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default="", editable=True)
    phone = models.CharField(max_length=15)
    assigned_truck = models.OneToOneField(Truck, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_id('D')
        super().save(*args, **kwargs)

class Trip(models.Model):
    id = models.CharField(max_length=6, primary_key=True, editable=False, unique=True)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    destination = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default="pending")
    start_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_id('T')
        super().save(*args, **kwargs)