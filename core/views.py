from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Truck, Driver, Trip
from .serializers import TruckSerializer, DriverSerializer, TripSerializer
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, LoginForm

@method_decorator(permission_required('core.view_truck'), name='dispatch')
class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

@method_decorator(permission_required('core.view_driver'), name='dispatch')
class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

@method_decorator(permission_required('core.view_trip'), name='dispatch')
class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer



def landing(request):
    return render(request, 'landing.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('landing')