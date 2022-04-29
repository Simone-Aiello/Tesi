from django.urls import path
from .views import SpeedRpmDataVisualizerView, WheelDataVisualizer
urlpatterns = [
    path("",SpeedRpmDataVisualizerView.as_view()),
    path("wheels",WheelDataVisualizer.as_view()),
]
