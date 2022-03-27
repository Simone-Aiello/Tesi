from django.urls import path
from .views import VehicleDataVisualizerView
urlpatterns = [
    path("",VehicleDataVisualizerView.as_view()),
]
