from rest_framework import serializers
from .models import Vehicle, Measurement
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        #specifies what fields we want to serialize
        fields = [ 
            "license_plate",
            "model_name",
        ]
        #specifies what field can be null
        extra_kwargs = {
            "model_name" : {"required" : False}
        }

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = [
                "vehicle",
                "sensor",
                "data",
                "timestamp",
            ]
