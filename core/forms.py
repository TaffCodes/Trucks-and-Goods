from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from .models import Truck, Driver, Trip, Route
from django.db.models import Q


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)

class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck
        fields = ['number_plate', 'model', 'capacity', 'status']
        widgets = {
            'number_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }


class TruckChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.number_plate} ({obj.id})"


class DriverForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(
            groups__name='Driver'
        ).exclude(
            driver__isnull=False
        ),
        empty_label="Select a Driver",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number'
        })
    )
    # assigned_truck = TruckChoiceField(
    #     queryset=Truck.objects.filter(
    #         status='available'
    #     ).filter(
    #         Q(driver__isnull=True)
    #     ),
    #     empty_label="Select a Truck",
    #     required=False,
    #     widget=forms.Select(attrs={
    #         'class': 'form-control'
    #     })
    # )

    class Meta:
        model = Driver
        fields = ['user', 'phone']
        labels = {
            'user': 'Driver',
            'phone': 'Phone Number',
            # 'assigned_truck': 'Assign Truck (Optional)'
        }


class TruckForm(forms.ModelForm):
    number_plate = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter number plate'
        })
    )
    model = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter truck model'
        })
    )
    capacity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter capacity'
        })
    )
    status = forms.ChoiceField(
        choices=[
            ('available', 'Available'),
            ('in_use', 'In Use'),
            ('maintenance', 'Under Maintenance')
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Truck
        fields = ['number_plate', 'model', 'capacity', 'status']
        labels = {
            'number_plate': 'Number Plate',
            'model': 'Truck Model',
            'capacity': 'Capacity (tons)',
            'status': 'Current Status'
        }
        help_texts = {
            'number_plate': 'Enter the truck\'s registration number',
            'capacity': 'Enter the maximum load capacity in tons'
        }

    def clean_number_plate(self):
        number_plate = self.cleaned_data.get('number_plate')
        if Truck.objects.filter(number_plate=number_plate).exists():
            raise forms.ValidationError('This number plate is already registered')
        return number_plate.upper()

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['start_location', 'end_location', 'distance_km', 'estimated_fuel_cost', 'gpx_file']
        widgets = {
            'start_location': forms.TextInput(attrs={'class': 'form-control'}),
            'end_location': forms.TextInput(attrs={'class': 'form-control'}),
            'distance_km': forms.NumberInput(attrs={'class': 'form-control'}),
            'estimated_fuel_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'gpx_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }



class TripForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get drivers who are not in active trips
        available_drivers = Driver.objects.exclude(
            trip__status__in=['started', 'paused', 'resumed', 'pending']
        ).distinct()
        
        # Get trucks that are not in active trips
        available_trucks = Truck.objects.exclude(
            trip__status__in=['started', 'paused', 'resumed', 'pending']
        ).distinct()
        
        # Update form field querysets
        self.fields['driver'].queryset = available_drivers
        self.fields['truck'].queryset = available_trucks
        
        # Add help texts
        self.fields['driver'].help_text = "Only drivers not currently assigned to active trips"
        self.fields['truck'].help_text = "Only trucks not currently assigned to active trips"

    class Meta:
        model = Trip
        fields = ['truck', 'driver', 'route']
        widgets = {
            'truck': forms.Select(attrs={'class': 'form-control'}),
            'driver': forms.Select(attrs={'class': 'form-control'}),
            'route': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        driver = cleaned_data.get('driver')
        truck = cleaned_data.get('truck')

        if driver:
            active_trips = Trip.objects.filter(
                driver=driver,
                status__in=['started', 'paused', 'resumed', 'pending']
            )
            if active_trips.exists():
                raise forms.ValidationError("This driver is already assigned to an active trip.")

        if truck:
            active_trips = Trip.objects.filter(
                truck=truck,
                status__in=['started', 'paused', 'resumed', 'pending']
            )
            if active_trips.exists():
                raise forms.ValidationError("This truck is already assigned to an active trip.")

        return cleaned_data