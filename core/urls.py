from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import TruckViewSet, DriverViewSet, TripViewSet, mark_notification_as_read, trip_details, get_trip_updates, driver_home, previous_trips, landing, signup, login_view, home, logout_view, truck_management, truck_detail, driver_management, add_driver, edit_driver, delete_driver, view_driver, add_truck, edit_truck, delete_truck, view_truck, route_management, add_route, edit_route, delete_route, view_route, update_truck_location, track_location, get_truck_location, trip_management, add_trip, start_trip, edit_trip, delete_trip, pause_trip, end_trip, resume_trip, visualize_trucks, get_truck_locations

router = DefaultRouter()
router.register(r'trucks', TruckViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'trips', TripViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', landing, name='landing'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('driver/home/', driver_home, name='driver_home'),
    path('logout/', logout_view, name='logout'),
    path('truck_management/', truck_management, name='truck_management'),
    path('driver_management/', driver_management, name='driver_management'),
    path('driver/add/', add_driver, name='add_driver'),
    path('driver/edit/<str:driver_id>/', edit_driver, name='edit_driver'),
    path('driver/delete/<str:driver_id>/', delete_driver, name='delete_driver'),
    path('driver/view/<str:driver_id>/', view_driver, name='view_driver'),
    path('truck/add/', add_truck, name='add_truck'),
    path('truck_detail/<str:truck_id>/', truck_detail, name='truck_detail'),
    path('truck/edit/<str:truck_id>/', edit_truck, name='edit_truck'),
    path('truck/delete/<str:truck_id>/', delete_truck, name='delete_truck'),
    path('truck/view/<str:truck_id>/', view_truck, name='view_truck'),
    path('route_management/', route_management, name='route_management'),
    path('route/add/', add_route, name='add_route'),
    path('route/edit/<str:route_id>/', edit_route, name='edit_route'),
    path('route/delete/<str:route_id>/', delete_route, name='delete_route'),
    path('route/view/<str:route_id>/', view_route, name='view_route'),
    path('update_location/<str:truck_id>/', update_truck_location, name='update_truck_location'),
    path('track/<str:truck_id>/', track_location, name='track_location'),
    path('get_truck_location/<str:truck_id>/', get_truck_location, name='get_truck_location'),
    path('trip_management/', trip_management, name='trip_management'),
    path('trip/add/', add_trip, name='add_trip'),
    path('trip/edit/<str:trip_id>/', edit_trip, name='edit_trip'),
    path('trip/delete/<str:trip_id>/', delete_trip, name='delete_trip'),
    path('trip/start/<str:trip_id>/', start_trip, name='start_trip'),
    path('trip/pause/<str:trip_id>/', pause_trip, name='pause_trip'),
    path('trip/resume/<str:trip_id>/', resume_trip, name='resume_trip'),
    path('trip/end/<str:trip_id>/', end_trip, name='end_trip'),
    path('visualize_trucks/', visualize_trucks, name='visualize_trucks'),
    path('get_truck_locations/', get_truck_locations, name='get_truck_locations'),
    path('previous_trips/', previous_trips, name='previous_trips'),
    path('trip/details/<str:trip_id>/', trip_details, name='trip_details'),
    path('get_trip_updates/', get_trip_updates, name='get_trip_updates'),
    path('mark_notification_as_read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),

]