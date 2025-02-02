from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import TruckViewSet, DriverViewSet, TripViewSet, landing, signup, login_view, home, logout_view, truck_management, truck_detail

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
    path('truck/<str:truck_id>/', truck_detail, name='truck_detail'),
]
