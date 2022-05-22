from django.urls import path
from . import views
from .views import VehicleAPIView,VehicleDataAPIView,WheelApiView,LatestCarData
urlpatterns = [
    path("Vehicle",VehicleAPIView.as_view()),
    path("VehicleData",VehicleDataAPIView.as_view()),
    path("WheelData",WheelApiView.as_view()),
    path("LatestValues",LatestCarData.as_view()),
]
