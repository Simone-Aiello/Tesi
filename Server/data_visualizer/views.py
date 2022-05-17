from django.shortcuts import render
from django.views import View

class SpeedRpmDataVisualizerView(View):

    def get(self,request):
        return render(request=request,template_name="index.html")


class WheelDataVisualizer(View):

    def get(self,request):
        return render(request=request,template_name="wheels.html")

class Car3DVisualizer(View):

    def get(self,request):
        return render(request=request,template_name="car_model.html")
