from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import Truck, Driver, Trip, Route, Notification
from .serializers import TruckSerializer, DriverSerializer, TripSerializer
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, LoginForm,DriverForm, TruckForm, RouteForm, TripForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.core.management import call_command
import threading
from django.http import JsonResponse
import gpxpy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt



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
            if user.groups.filter(name='Driver').exists():
                return redirect('driver_home')
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

def is_driver(user):
    return user.groups.filter(name='Driver').exists()



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
@user_passes_test(is_driver)
def driver_home(request):
    driver = request.user.driver
    pending_trips = Trip.objects.filter(driver=driver, status='pending')
    started_trips = Trip.objects.filter(driver=driver, status='started')
    paused_trips = Trip.objects.filter(driver=driver, status='paused')
    resumed_trips = Trip.objects.filter(driver=driver, status='resumed')
    current_trip = Trip.objects.filter(driver=driver, status='started').first()
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'driver_home.html', {
        'driver': driver,
        'pending_trips': pending_trips,
        'started_trips': started_trips,
        'paused_trips': paused_trips,
        'resumed_trips': resumed_trips,
        'current_trip': current_trip,
        'notifications': notifications
    })

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
            messages.success(request, "Driver added successfully")
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
            messages.success(request, f"Driver {driver_id} - {driver.name} updated successfully")
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
        messages.success(request, f"Driver {driver_id} - {driver.name} deleted successfully")
        return redirect('driver_management')
    return render(request, 'delete_driver.html', {'driver': driver})


# @login_required
# @user_passes_test(is_fleet_manager)
# def add_truck(request):
#     if request.method == 'POST':
#         form = TruckForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('truck_management')
#     else:
#         form = TruckForm()
#     return render(request, 'add_truck.html', {'form': form})

# @login_required
# @user_passes_test(is_fleet_manager)
# def edit_truck(request, truck_id):
#     truck = get_object_or_404(Truck, id=truck_id)
#     if request.method == 'POST':
#         form = TruckForm(request.POST, instance=truck)
#         if form.is_valid():
#             form.save()
#             return redirect('truck_management')
#     else:
#         form = TruckForm(instance=truck)
#     return render(request, 'edit_truck.html', {'form': form, 'truck': truck})

# @login_required
# @user_passes_test(is_fleet_manager)
# def delete_truck(request, truck_id):
#     truck = get_object_or_404(Truck, id=truck_id)
#     if request.method == 'POST':
#         truck.delete()
#         return redirect('truck_management')
#     return render(request, 'delete_truck.html', {'truck': truck})

# @login_required
# @user_passes_test(is_fleet_manager)
# def view_truck(request, truck_id):
#     truck = get_object_or_404(Truck, id=truck_id)
#     return render(request, 'view_truck.html', {'truck': truck})


@login_required
@user_passes_test(is_fleet_manager)
def add_truck(request):
    if request.method == 'POST':
        form = TruckForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Truck added successfully")
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
            messages.success(request, f"Truck {truck.id} - {truck.number_plate} updated successfully")
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
        messages.success(request, f"Truck {truck_id} - {truck.number_plate} deleted successfully")
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
def edit_route(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            messages.success(request, f"Route {route.id} - {route.start_location} ➝ {route.end_location} updated successfully")
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
        messages.success(request, f"Route {route_id} - {route.start_location} ➝ {route.end_location} deleted successfully")
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


@login_required
@user_passes_test(is_fleet_manager)
def add_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save()
            Notification.objects.create(
                user=trip.driver.user,
                message=f"You have a NEW trip {trip.id} from {trip.route.start_location} to {trip.route.end_location} with {trip.truck.number_plate}. Distance: {trip.route.distance_km} KM."
            )
            messages.success(request, "Trip  added successfully")
            return redirect('trip_management')
    else:
        form = TripForm()
    return render(request, 'add_trip.html', {'form': form})



@login_required
@user_passes_test(is_fleet_manager)
def trip_management(request):
    trips = Trip.objects.all()
    return render(request, 'trip_management.html', {'trips': trips})


@login_required
@user_passes_test(is_fleet_manager)
def add_route(request):
    if request.method == 'POST':
        form = RouteForm(request.POST, request.FILES)
        if form.is_valid():
            route = form.save()
            # Clear any existing messages
            storage = messages.get_messages(request)
            storage.used = True
            # Add new success message
            messages.success(request, f"Route from {route.start_location} to {route.end_location} added successfully")
            return redirect('route_management')
        else:
            # Clear any existing messages
            storage = messages.get_messages(request)
            storage.used = True
            # Add new error message
            messages.error(request, "Failed to add route. Check the form for errors.")
    else:
        form = RouteForm()
        # Clear messages when loading form
        storage = messages.get_messages(request)
        storage.used = True
        
    return render(request, 'add_route.html', {'form': form})

@login_required
@user_passes_test(is_fleet_manager)
def route_management(request):
    routes = Route.objects.all()
    return render(request, 'route_management.html', {'routes': routes})



from django.utils import timezone

@login_required
@user_passes_test(is_driver)
def start_trip(request, trip_id):
    try:
        trip = get_object_or_404(Trip, id=trip_id)
        trip.status = 'started'
        trip.simulation_active = True
        trip.start_time = timezone.now()
        trip.save()
        Notification.objects.create(
            user=trip.driver.user,
            message=f"You have STARTED your trip {trip.id} with {trip.truck.number_plate}."
        )
        threading.Thread(target=call_command, 
                        args=('simulate_gps_command', 
                              str(trip.truck.id), 
                              trip.route.gpx_file.path)).start()
        
        messages.success(request, f"Trip {trip.id} started successfully.")
        return redirect('driver_home')
    except Exception as e:
        messages.error(request, f"Failed to start trip: {str(e)}")
        return redirect('driver_home')

@login_required
@user_passes_test(is_driver) 
def end_trip(request, trip_id):
    try:
        trip = get_object_or_404(Trip, id=trip_id)
        trip.status = 'ended'
        trip.simulation_active = False
        trip.end_time = timezone.now()
        trip.save()
        Notification.objects.create(
            user=trip.driver.user,
            message=f"You have ENDED your trip {trip.id} with {trip.truck.number_plate}."
        )
        messages.success(request, f"Trip {trip.id} ended successfully.")
        return redirect('driver_home')
    except Exception as e:
        messages.error(request, f"Failed to end trip: {str(e)}")
        return redirect('driver_home')


@login_required
@user_passes_test(is_fleet_manager)
def edit_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                user=trip.driver.user,
                message=f"Your trip {trip.id} from {trip.route.start_location} to {trip.route.end_location} has been updated."
            )
            messages.success(request, f"Trip {trip.id} from {trip.route.start_location} to {trip.route.end_location} updated successfully")
            return redirect('trip_management')
    else:
        form = TripForm(instance=trip)
    return render(request, 'edit_trip.html', {'form': form, 'trip': trip})

@login_required
@user_passes_test(is_fleet_manager)
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == 'POST':
        trip.delete()
        Notification.objects.create(
            user=trip.driver.user,
            message=f"Your trip {trip_id} from {trip.route.start_location} to {trip.route.end_location} has been cancelled."
        )
        messages.success(request, f"Trip {trip_id} from {trip.route.start_location} to {trip.route.end_location} deleted successfully")
        return redirect('trip_management')
    return render(request, 'delete_trip.html', {'trip': trip})


@login_required
@user_passes_test(is_driver)
def pause_trip(request, trip_id):
    try:
        trip = get_object_or_404(Trip, id=trip_id)
        if request.method == 'POST':
            current_latitude = request.POST.get('latitude')
            current_longitude = request.POST.get('longitude')
            pause_reason_rest = request.POST.get('pause_reason_rest') == 'true'
            pause_reason_mechanical = request.POST.get('pause_reason_mechanical') == 'true'
            
            if current_latitude and current_longitude:
                trip.last_latitude = float(current_latitude)
                trip.last_longitude = float(current_longitude)
            
            trip.status = 'paused'
            trip.pause_reason_rest = pause_reason_rest
            trip.pause_reason_mechanical = pause_reason_mechanical
            trip.save()
            Notification.objects.create(
                user=trip.driver.user,
                message=f"You have PAUSED your trip {trip.id} from {trip.route.start_location} to {trip.route.end_location}."
            )
            messages.success(request, f"Trip {trip.id} from {trip.route.start_location} to {trip.route.end_location} paused successfully")
            return redirect('driver_home')
        else:
            last_latitude = trip.last_latitude if trip.last_latitude is not None else ''
            last_longitude = trip.last_longitude if trip.last_longitude is not None else ''
            return render(request, 'pause_trip.html', {
                'trip': trip,
                'last_latitude': last_latitude,
                'last_longitude': last_longitude
            })
    except ValueError:
        messages.error(request, "Invalid coordinates provided")
        return redirect('driver_home')
    except Exception as e:
        messages.error(request, f"Failed to pause trip: {str(e)}")
        return redirect('driver_home')




@login_required
@user_passes_test(is_driver)
def resume_trip(request, trip_id):
    try:
        trip = get_object_or_404(Trip, id=trip_id)
        trip.status = 'resumed'
        trip.simulation_active = True  # Reactivate simulation
        trip.save()
        Notification.objects.create(
            user=trip.driver.user,
            message=f"You have RESUMED your trip {trip.id} from {trip.route.start_location} to {trip.route.end_location}."
        )

        # Trigger the GPS simulation in a separate thread
        threading.Thread(target=call_command, 
                       args=('simulate_gps_command', 
                             str(trip.truck.id), 
                             trip.route.gpx_file.path)).start()

        messages.success(request, f"Trip {trip.id} from {trip.route.start_location} to {trip.route.end_location} resumed successfully")
        return redirect('driver_home')
    except Exception as e:
        messages.error(request, f"Failed to resume trip: {str(e)}")
        return redirect('driver_home')





@login_required
@user_passes_test(is_fleet_manager)
def visualize_trucks(request):
    trucks = Truck.objects.all()
    truck_locations = []

    for truck in trucks:
        if truck.latitude is not None and truck.longitude is not None:
            truck_locations.append({
                'truck_id': truck.id,
                'number_plate': truck.number_plate,
                'latitude': truck.latitude,
                'longitude': truck.longitude
            })

    return render(request, 'visualize_trucks.html', {'truck_locations': truck_locations})



@login_required
@user_passes_test(is_fleet_manager)
def get_truck_locations(request):
    trucks = Truck.objects.all()
    truck_locations = []

    for truck in trucks:
        last_trip = Trip.objects.filter(truck=truck).order_by('-start_time').first()
        if truck.latitude is not None and truck.longitude is not None:
            truck_locations.append({
                'truck_id': truck.id,
                'number_plate': truck.number_plate,
                'latitude': truck.latitude,
                'longitude': truck.longitude,
                'trip_id': last_trip.id if last_trip else None,
                'trip_status': last_trip.status if last_trip else 'No active trip'
            })

    return JsonResponse({'truck_locations': truck_locations})


@login_required
@user_passes_test(is_driver)
def previous_trips(request):
    driver = request.user.driver
    trips = Trip.objects.filter(driver=driver).order_by('-start_time')
    return render(request, 'previous_trips.html', {'trips': trips})


@login_required
def trip_details(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    return render(request, 'trip_details.html', {'trip': trip})

@login_required
@user_passes_test(is_driver)
def get_trip_updates(request):
    driver = request.user.driver
    context = {
        'current_trip': Trip.objects.filter(driver=driver, status='started').first(),
        'pending_trips': Trip.objects.filter(driver=driver, status='pending'),
        'paused_trips': Trip.objects.filter(driver=driver, status='paused'),
        'resumed_trips': Trip.objects.filter(driver=driver, status='resumed')
    }
    return render(request, 'trip_updates.html', context)


@csrf_exempt
@login_required
def mark_notification_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.delete()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)