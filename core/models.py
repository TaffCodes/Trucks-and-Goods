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
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_trip', 'In Trip'),
        ('maintenance', 'Under Maintenance')
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )
    @property
    def is_available(self):
        active_trips = self.trip_set.filter(
            status__in=['started', 'paused', 'resumed', 'pending']
        ).exists()
        return not active_trips
        
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
    gpx_file = models.FileField(upload_to='gpx_files/', null=True, blank=True)
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



class Trip(models.Model):
    id = models.CharField(max_length=6, primary_key=True, editable=False, unique=True)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('started', 'started'),
        ('paused', 'paused'),
        ('resumed', 'resumed'),
        ('ended', 'ended'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    last_longitude = models.FloatField(null=True, blank=True)
    last_latitude = models.FloatField(null=True, blank=True)
    simulation_active = models.BooleanField(default=False)
    

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_id('T')
        
        # Update truck status based on trip status
        if self.status in ['started', 'paused', 'resumed']:
            self.truck.status = 'in_trip'
        elif self.status == 'ended':
            # Check if there are any other active trips for this truck
            active_trips = Trip.objects.filter(
                truck=self.truck,
                status__in=['started', 'paused', 'resumed']
            ).exclude(id=self.id)
            
            if not active_trips.exists():
                self.truck.status = 'available'
        
        self.truck.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # When deleting a trip, check if it's the last active trip for the truck
        if self.status in ['started', 'paused', 'resumed']:
            active_trips = Trip.objects.filter(
                truck=self.truck,
                status__in=['started', 'paused', 'resumed']
            ).exclude(id=self.id)
            
            if not active_trips.exists():
                self.truck.status = 'available'
                self.truck.save()
        
        super().delete(*args, **kwargs)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} at {self.timestamp}"