from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import TruckViewSet, DriverViewSet, TripViewSet, landing, signup, login_view, home, logout_view, truck_management, truck_detail, driver_management, add_driver, edit_driver, delete_driver, view_driver, add_truck, edit_truck, delete_truck, view_truck
from .views import *

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
    path('logout/', logout_view, name='logout'),
    path('truck_management/', truck_management, name='truck_management'),
    path('driver_management/', driver_management, name='driver_management'),
    path('driver/add/', add_driver, name='add_driver'),
    path('driver/edit/<str:driver_id>/', edit_driver, name='edit_driver'),
    path('driver/delete/<str:driver_id>/', delete_driver, name='delete_driver'),
    path('driver/view/<str:driver_id>/', view_driver, name='view_driver'),
    path('truck/add/', add_truck, name='add_truck'),
    path('truck/edit/<str:truck_id>/', edit_truck, name='edit_truck'),
    path('truck/delete/<str:truck_id>/', delete_truck, name='delete_truck'),
    path('truck/view/<str:truck_id>/', view_truck, name='view_truck'),
    path('truck/<str:truck_id>/', truck_detail, name='truck_detail'),


]
