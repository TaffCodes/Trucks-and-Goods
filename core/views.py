from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import Truck, Driver, Trip, Route
from .serializers import TruckSerializer, DriverSerializer, TripSerializer
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, LoginForm,DriverForm, TruckForm, RouteForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test



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

@login_required
def home(request):
    trucks = Truck.objects.all()
    return render(request, 'home.html', {'trucks': trucks})


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('landing')
    return render(request, 'landing.html')


def is_fleet_manager(user):
    return user.groups.filter(name='Fleet manager').exists()

# @user_passes_test(is_fleet_manager)
# @login_required
# def truck_management(request):
#     add_truck_form = AddTruckForm()
    
#     if request.method == 'POST':
#         if 'add_truck' in request.POST:
#             add_truck_form = AddTruckForm(request.POST)
#             if add_truck_form.is_valid():
#                 add_truck_form.save()
#                 return redirect('truck_management')
    
#     return render(request, 'truck_management.html', {'add_truck_form': add_truck_form})

@login_required
@user_passes_test(is_fleet_manager)
def truck_management(request):
    trucks = Truck.objects.all()  # Fetch all trucks
    print(f"Number of trucks: {trucks.count()}")  # Debug output
    for truck in trucks:
        print(f"Truck: {truck.id} - {truck.number_plate}")  # Debug each truck
    return render(request, 'truck_management.html', {'trucks': trucks})

@login_required
def truck_detail(request, truck_id):
    truck = get_object_or_404(Truck, id=truck_id)
    return render(request, 'truck_detail.html', {'truck': truck})


@login_required
@user_passes_test(is_fleet_manager)
def driver_management(request):
    drivers = Driver.objects.all()
    return render(request, 'driver_management.html', {'drivers': drivers})

@login_required
@user_passes_test(is_fleet_manager)
def view_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    return render(request, 'view_driver.html', {'driver': driver})

@login_required
@user_passes_test(is_fleet_manager)
def add_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('driver_management')
    else:
        form = DriverForm()
    return render(request, 'add_driver.html', {'form': form})

@login_required
@user_passes_test(is_fleet_manager)
def edit_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('driver_management')
    else:
        form = DriverForm(instance=driver)
    return render(request, 'edit_driver.html', {'form': form})

@login_required
@user_passes_test(is_fleet_manager)
def delete_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        driver.delete()
        return redirect('driver_management')
    return render(request, 'delete_driver.html', {'driver': driver})


@login_required
@user_passes_test(is_fleet_manager)
def add_truck(request):
    if request.method == 'POST':
        form = TruckForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('truck_management')
    else:
        form = TruckForm()
    return render(request, 'add_truck.html', {'form': form})

@login_required
@user_passes_test(is_fleet_manager)
def edit_truck(request, truck_id):
    truck = get_object_or_404(Truck, id=truck_id)
    if request.method == 'POST':
        form = TruckForm(request.POST, instance=truck)
        if form.is_valid():
            form.save()
            return redirect('truck_management')
    else:
        form = TruckForm(instance=truck)
    return render(request, 'edit_truck.html', {'form': form, 'truck': truck})

@login_required
@user_passes_test(is_fleet_manager)
def delete_truck(request, truck_id):
    truck = get_object_or_404(Truck, id=truck_id)
    if request.method == 'POST':
        truck.delete()
        return redirect('truck_management')
    return render(request, 'delete_truck.html', {'truck': truck})

@login_required
@user_passes_test(is_fleet_manager)
def view_truck(request, truck_id):
    truck = get_object_or_404(Truck, id=truck_id)
    return render(request, 'view_truck.html', {'truck': truck})


@login_required
@user_passes_test(is_fleet_manager)
def add_truck(request):
    if request.method == 'POST':
        form = TruckForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('truck_management')
    else:
        form = TruckForm()
    return render(request, 'add_truck.html', {'form': form})

@login_required
@user_passes_test(is_fleet_manager)
def edit_truck(request, truck_id):
    truck = get_object_or_404(Truck, id=truck_id)
    if request.method == 'POST':
        form = TruckForm(request.POST, instance=truck)
        if form.is_valid():
            form.save()
            return redirect('truck_management')
    else:
        form = TruckForm(instance=truck)
    return render(request, 'edit_truck.html', {'form': form, 'truck': truck})

@login_required
@user_passes_test(is_fleet_manager)
def delete_truck(request, truck_id):
    truck = get_object_or_404(Truck, id=truck_id)
    if request.method == 'POST':
        truck.delete()
        return redirect('truck_management')
    return render(request, 'delete_truck.html', {'truck': truck})

@login_required
@user_passes_test(is_fleet_manager)
def view_truck(request, truck_id):
    truck = get_object_or_404(Truck, id=truck_id)
    return render(request, 'view_truck.html', {'truck': truck})


@login_required
def route_management(request):
    routes = Route.objects.all()
    return render(request, 'route_management.html', {'routes': routes})

@login_required
@user_passes_test(is_fleet_manager)
def add_route(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('route_management')
    else:
        form = RouteForm()
    return render(request, 'add_route.html', {'form': form})

@login_required
@user_passes_test(is_fleet_manager)
def edit_route(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            return redirect('route_management')
    else:
        form = RouteForm(instance=route)
    return render(request, 'edit_route.html', {'form': form, 'route': route})

@login_required
@user_passes_test(is_fleet_manager)
def delete_route(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    if request.method == 'POST':
        route.delete()
        return redirect('route_management')
    return render(request, 'delete_route.html', {'route': route})

@login_required
def view_route(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    return render(request, 'view_route.html', {'route': route})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Truck

@csrf_exempt
def update_truck_location(request, truck_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            truck = get_object_or_404(Truck, id=truck_id)
            truck.latitude = data['latitude']
            truck.longitude = data['longitude']
            truck.save()
            return JsonResponse({"status": "success"})
        except Truck.DoesNotExist:
            return JsonResponse({"error": "Truck not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == "GET":
        # Add GET handler for testing
        return JsonResponse({"message": "Use POST method to update location"}, status=405)
    return JsonResponse({"error": "Method not allowed"}, status=405)

def track_location(request, truck_id):
    truck = get_object_or_404(Truck, id=truck_id)
    initial_location = {
        'latitude': truck.latitude or -1.2921,  # Default to Nairobi if no location
        'longitude': truck.longitude or 36.8219
    }
    return render(request, 'track_location.html', {
        'truck': truck,
        'initial_location': initial_location
    })

def get_truck_location(request, truck_id):
    truck = get_object_or_404(Truck, id=truck_id)
    if truck.latitude is None or truck.longitude is None:
        return JsonResponse({
            'error': 'Location not available'
        }, status=404)
    return JsonResponse({
        'latitude': truck.latitude,
        'longitude': truck.longitude,
        'last_updated': truck.last_updated.isoformat()
    })