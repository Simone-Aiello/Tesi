from django.db import models

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=10,primary_key=True)
    model_name = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.license_plate


class Measurement(models.Model):

    #enum types
    class Sensors(models.TextChoices):
        RPM = "rpm"
        SPEED = "speed"
        COOLANT_TEMPERATURE = "coolant_temperature"
        THROTTLE_POSITION = "throttle_position"
        FUEL_LEVEL = "fuel_level"
        ENGINE_OIL_TEMPERATURE = "engine_oil_temperature"
        ENGINE_LOAD = "engine_load"
        ENGINE_FUEL_GAUGE = "fuel_rail_gauge"
        INTAKE_AIR_TEMPERATURE = "intake_air_temperature"
        INTAKE_MANIFOLD_PRESSURE = "intake_manifold_pressure"
    
    
    #pk created by default as auto-increment value
    vehicle = models.ForeignKey(Vehicle,on_delete=models.RESTRICT)
    sensor = models.CharField(choices=Sensors.choices, max_length=25)
    data = models.IntegerField()
    timestamp = models.DateTimeField()