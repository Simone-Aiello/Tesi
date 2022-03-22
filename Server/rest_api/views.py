# from django.shortcuts import render
# from rest_framework.parsers import JSONParser
# from django.http import HttpResponse,JsonResponse
from .models import Vehicle
from .serializer import VehicleSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class VehicleAPIView(APIView):
    
    #if license_plate is specified as a GET parameters return only one vehicle, otherwise returns all
    def get(self, request):
        lp = request.query_params.get("license_plate")
        if lp is None:
            vehicles = Vehicle.objects.all()
            all_serializer = VehicleSerializer(vehicles,many=True)
            return Response(all_serializer.data)
        else:
            try:
                vehicle = Vehicle.objects.get(license_plate=lp)
                serializer = VehicleSerializer(vehicle) 
                return Response(serializer.data)
            except Vehicle.DoesNotExist:
                return Response({"Not found": f"Cannot find vehicle with license plate: {lp}"},status=status.HTTP_404_NOT_FOUND)

    
    def post(self, request):
        serializer = VehicleSerializer(data=request.data,many=True)
        if serializer.is_valid():
            print(serializer.data)
        else:
            print("NOT VALID")
        return Response({"OK"})
