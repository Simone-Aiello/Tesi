from django.urls import path
from .views import SpeedRpmDataVisualizerView, WheelDataVisualizer,Car3DVisualizer
urlpatterns = [
    path("speedrpm",SpeedRpmDataVisualizerView.as_view()),
    path("wheels",WheelDataVisualizer.as_view()),
    path("",Car3DVisualizer.as_view())
]
