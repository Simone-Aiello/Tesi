from django.urls import path
from . import views
from .views import VehicleAPIView,VehicleDataAPIView,WheelApiView
urlpatterns = [
    path("Vehicle",VehicleAPIView.as_view()),
    path("VehicleData",VehicleDataAPIView.as_view()),
    path("WheelData",WheelApiView.as_view()),
]
