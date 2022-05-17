from django.urls import path
from .views import SpeedRpmDataVisualizerView, WheelDataVisualizer,Car3DVisualizer
urlpatterns = [
    path("",SpeedRpmDataVisualizerView.as_view()),
    path("wheels",WheelDataVisualizer.as_view()),
    path("car",Car3DVisualizer.as_view())
]
