# from django.shortcuts import render
# from rest_framework.parsers import JSONParser
# from django.http import HttpResponse,JsonResponse
from datetime import datetime
from sklearn.svm import SVC
from .models import Measurement, Vehicle
from .serializer import MeasurementSerializer, VehicleSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from sklearn.linear_model import LinearRegression
import joblib
import pandas as pd
class VehicleAPIView(APIView):
    
    #If license_plate is specified as a GET parameters return only one vehicle, otherwise returns all
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

class VehicleDataAPIView(APIView):

    def __checkRpmSpeedAnomalous(self,data):
        speed = None
        rpm = None
        idx_speed = None
        idx_rpm = None
        for idx,dict in enumerate(data):
            if dict['sensor'] == 'speed':
                speed = dict['data']
                idx_speed = idx
            elif dict['sensor'] == 'rpm':
                rpm = dict['data']
                idx_rpm = idx
        if speed is not None and rpm is not None:      
            model = joblib.load("ml_models/isolation_forest.pkl")
            df = pd.DataFrame({"speed":[speed],"rpm":[rpm]})
            prediction = model.predict(df)
            data[idx_speed]["anomalous"] = 1 if prediction == -1 else 0
            data[idx_rpm]["anomalous"] = 1 if prediction == -1 else 0 


    def __trainWheelModel(self,measurement,model : LinearRegression):
        #Optimal bar for (some) car tyres
        max_bar = 2.6 # TODO Da inserire nel database
        measurement['data'] = float(measurement['data'])
        training_data = [measurement['data']]
        training_timestamp = [datetime.strptime(measurement['timestamp'],"%Y-%m-%dT%H:%M:%SZ").date().toordinal()]
        if measurement['data'] > max_bar:
            raise ValueError("Data values exceeded max") #TODO Da modificare
        if(measurement['data'] == max_bar):
            model = LinearRegression()
        else:
            try:
                res = Measurement.objects.filter(data=max_bar,sensor=measurement["sensor"],vehicle=measurement["vehicle"]).values().latest("timestamp")
                last_id = res["id"]
                all_data = Measurement.objects.filter(sensor=measurement["sensor"],vehicle=measurement["vehicle"],id__gte=last_id)
                for d in all_data:
                   training_data.append(float(d.data))
                   training_timestamp.append(d.timestamp.date().toordinal())
            except Measurement.DoesNotExist:
                print("Exception")
        print(training_data)
        print(training_timestamp)
        df_values = pd.DataFrame(data={"values":training_data})
        df_timestamp = pd.DataFrame(data={"timestamp":training_timestamp})
        print(df_timestamp.head())
        model.fit(df_values,df_timestamp)

    def __updateWheelModel(self,data):
        wheel_sensor_name = ('front_right_wheel_pressure','front_left_wheel_pressure','rear_right_wheel_pressure','rear_left_wheel_pressure')
        for m in data:
            if m['sensor'] in wheel_sensor_name:
                filename = f"ml_models/wheels/{m['sensor']}.pkl"
                model : LinearRegression = joblib.load(filename)
                self.__trainWheelModel(m,model)
                #joblib.dump(value=model,filename=filename,compress=9)

    def get(self, request):
        data = Measurement.objects.all()
        serializer = MeasurementSerializer(data,many = True) 
        return Response(serializer.data)
        
    def post(self, request):
        serializer = MeasurementSerializer(data = request.data, many=True)
        serializer.is_valid(raise_exception=True)
        #self.__checkRpmSpeedAnomalous(serializer.data)
        self.__updateWheelModel(serializer.data)
        #serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)