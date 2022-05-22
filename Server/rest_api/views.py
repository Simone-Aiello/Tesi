from datetime import date, datetime
import time
from django.http import HttpRequest,JsonResponse
from django.db.models import Q
import numpy as np
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
            return Response({"OK"})
        else:
            return Response({"Invalid data"})

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
            data[idx_speed]["anomalous"] = True if prediction == -1 else False
            data[idx_rpm]["anomalous"] = True if prediction == -1 else False


    def __trainWheelModel(self,measurement,model : LinearRegression) -> LinearRegression:
        #Optimal bar for (some) car tyres
        max_bar = 2.6 # TODO Da inserire nel database
        measurement['data'] = float(measurement['data'])
        training_data = [measurement['data']]
        training_timestamp = [datetime.strptime(measurement['timestamp'],"%Y-%m-%dT%H:%M:%SZ").date().toordinal()]
        if measurement['data'] > max_bar:
            raise ValueError("Data values exceeded max_bar") #TODO Da modificare
        if(measurement['data'] == max_bar):
            model = LinearRegression()
        else:
            try:
                res = Measurement.objects.filter(data=max_bar,sensor=measurement["sensor"],vehicle=measurement["vehicle"]).values().latest("id","timestamp")
                last_id = res["id"]
                all_data = Measurement.objects.filter(sensor=measurement["sensor"],vehicle=measurement["vehicle"],id__gte=last_id)
                for d in all_data:
                   training_data.append(float(d.data))
                   training_timestamp.append(d.timestamp.date().toordinal())
            except Measurement.DoesNotExist:
                print("Exception")
        df_values = pd.DataFrame(data={"values":training_data})
        df_timestamp = pd.DataFrame(data={"timestamp":training_timestamp})
        model.fit(df_values,df_timestamp)
        return model
    def __updateWheelModel(self,data):
        wheel_sensor_name = ('front_right_wheel_pressure','front_left_wheel_pressure','rear_right_wheel_pressure','rear_left_wheel_pressure')
        for m in data:
            if m['sensor'] in wheel_sensor_name:
                filename = f"ml_models/wheels/{m['sensor']}.pkl"
                model = self.__trainWheelModel(m,joblib.load(filename))
                joblib.dump(value=model,filename=filename,compress=9)

    def get(self, request : HttpRequest):
        requested_sensors = request.GET.getlist("sensor[]")
        requested_vehicle = request.GET.get("vehicle")
        start_date = request.GET.get("start_date","")
        end_date = request.GET.get("end_date","")
        query = Q()
        query &= Q(sensor__in=requested_sensors,vehicle=requested_vehicle)
        if start_date != "":
            query &= Q(timestamp__gte=start_date)
        if end_date != "":
            query &= Q(timestamp__lte=end_date)
        data = Measurement.objects.filter(query)
        serializer = MeasurementSerializer(data,many = True) 
        return Response(serializer.data)
        
    def post(self, request):# TODO QUESTA POST VA MESSA IN UN'API A PARTE
        try:
            self.__checkRpmSpeedAnomalous(request.data)
            serializer = MeasurementSerializer(data = request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.__updateWheelModel(serializer.data)
        except ValueError as e:
            return Response(e,status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class WheelApiView(APIView):
    

    def __calculate_line_points(self,max_bar,slope,intercept):
        points = []
        for i in np.arange(0.0,max_bar + 0.5,0.2):
            y = (slope * i) + intercept
            date_y =  date.fromordinal(int(y))
            string_y = date_y.strftime("%Y-%m-%dT%H:%M:%SZ")
            points.append({
                "x" : round(i,2),
                "y" : string_y,
            })
        return points




    def get(self, request : HttpRequest):
        max_bar = 2.6 #TODO Da mettere nel database
        line_points = []
        sensor = request.GET.get("wheel",None)
        if(sensor not in ("front_right_wheel_pressure","front_left_wheel_pressure","rear_right_wheel_pressure","rear_left_wheel_pressure")):
            return Response("Missing sensor",status=status.HTTP_400_BAD_REQUEST)
        
        #Getting data from the db since the last wheel inflate
        try:
            res = Measurement.objects.filter(data=max_bar,sensor=sensor).values().latest("id","timestamp")
            last_id = res["id"]
            all_data = Measurement.objects.filter(sensor=sensor,id__gte=last_id)
            serializer = MeasurementSerializer(all_data,many=True)
        except Measurement.DoesNotExist:
            return Response({"data":[]},status=status.HTTP_200_OK)

        
        #Loading the Linear regression model to get line equation if data points >= 2
        if len(all_data) >= 2:
            filename = f"ml_models/wheels/{sensor}.pkl"
            model : LinearRegression = joblib.load(filename)
            line_points = self.__calculate_line_points(max_bar=max_bar,slope=model.coef_[0][0],intercept=model.intercept_[0])
        return Response({"data": serializer.data,"line_points":line_points}, status=status.HTTP_200_OK)
    
class LatestCarData(APIView):
    
    #If license_plate is specified as a GET parameters return only one vehicle, otherwise returns all
    def get(self, request):
        values = {}
        requested_sensors = request.GET.getlist("sensor[]")
        print(requested_sensors)
        for sensor in requested_sensors:
            try:
                val = Measurement.objects.filter(sensor=sensor).values().latest("id","timestamp")
                values[sensor] = val
            except Measurement.DoesNotExist: 
                val[sensor] = None
        return JsonResponse(values)