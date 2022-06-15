from django.db import models

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=10,primary_key=True)
    model_name = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.license_plate


class Measurement(models.Model):

    #Enum types
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
        FRONT_RIGHT_WHEEL_PRESSURE = "front_right_wheel_pressure"
        FRONT_LEFT_WHEEL_PRESSURE = "front_left_wheel_pressure"
        REAR_RIGHT_WHEEL_PRESSURE = "rear_right_wheel_pressure"
        REAR_LEFT_WHEEL_PRESSURE = "rear_left_wheel_pressure"
    
    
    #Pk created by default as auto-increment value
    vehicle = models.ForeignKey(Vehicle,on_delete=models.RESTRICT)
    sensor = models.CharField(choices=Sensors.choices, max_length=26)
    data = models.DecimalField(max_digits=12,decimal_places=2)
    timestamp = models.DateTimeField()
    anomalous = models.BooleanField(default=False)