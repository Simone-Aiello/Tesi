#!/usr/bin/python3
import requests
from random import randrange
from datetime import datetime
from time import sleep
if __name__ == "__main__":
    anomalous = False
    while True:
        coin = randrange(0,6)
        anomalous = True if coin == 2 else False
        data = []
        rpm = 0
        speed = 0
        if anomalous:
            print("ANOMALO")
            tp = randrange(0,2)
            #High Speed low RPM
            if tp == 1:
                rpm = randrange(0,800)
                speed = randrange(90,140)
            #High RPM low Speed
            else:
                rpm = randrange(2500,4000)
                speed = randrange(0,35)
        else:
            print("NON ANOMALO")
            with open("rpm.csv","r") as rpm_file:
                with open("speed.csv","r") as speed_file:
                    r = rpm_file.readlines()
                    s = speed_file.readlines()
                    index = randrange(1,len(r))
                    rpm = int(r[index].split(",")[1])
                    speed = int(s[index].split(",")[1])
                    print(rpm,speed)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        speed_dict = {
            "vehicle": "FG868XN",
            "sensor": "speed",
            "data": speed,
            "timestamp":  timestamp,
        }
        rpm_dict = {
            "vehicle": "FG868XN",
            "sensor": "rpm",
            "data": rpm,
            "timestamp": timestamp,
        }
        data.append(speed_dict)
        data.append(rpm_dict)
        sleep(1)
        response = requests.post("http://localhost:8000/rest_api/VehicleData",json=data,timeout=3)
        print(response.json())
"""
[
    {
        "vehicle": "FG868XN",
        "sensor": "front_right_wheel_pressure",
        "data": 2.1,
        "timestamp": "2022-04-21 14:21:27"
    },
    {
        "vehicle": "FG868XN",
        "sensor": "front_left_wheel_pressure",
        "data": 0,
        "timestamp": "2022-04-21 14:21:27"
    },
    {
        "vehicle": "FG868XN",
        "sensor": "rear_left_wheel_pressure",
        "data": 0,
        "timestamp": "2022-04-21 14:21:27"
    }
]
"""