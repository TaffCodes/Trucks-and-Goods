import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


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



class Route(models.Model):
    id = models.CharField(max_length=6, primary_key=True, editable=False, unique=True)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    distance_km = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="Distance in kilometers"
    )
    estimated_fuel_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Estimated cost in currency"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_id('R')  # Route ID format: R-XXXX
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}: {self.start_location} ➝ {self.end_location} ({self.distance_km} km)"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Route'
        verbose_name_plural = 'Routes'