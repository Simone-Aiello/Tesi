from django.urls import path
from . import views
from .views import VehicleAPIView
urlpatterns = [
    path("VehicleData",VehicleAPIView.as_view())
]
