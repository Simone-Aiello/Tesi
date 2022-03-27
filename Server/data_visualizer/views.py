from django.shortcuts import render
from django.views import View
from rest_api.models import Measurement,Vehicle

class VehicleDataVisualizerView(View):

    def get(self,request):
        return render(request=request,template_name="index.html")
