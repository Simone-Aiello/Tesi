#!/usr/bin/python3
import json
from time import sleep
import pandas as pd
import numpy as np
from datetime import date, timedelta,datetime
from random import uniform
import matplotlib.pylab as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import requests
current_date = date.today()
current_bar = 2.6
while current_bar > 0:
    data =[{
        "vehicle": "FG868XN",
        "sensor": "front_right_wheel_pressure",
        "data": current_bar,
        "timestamp": current_date.strftime("%Y-%m-%d %H:%M:%S")
    }]
    print(data)
    current_bar = current_bar - uniform(0.01 ,0.2) if current_bar - uniform(0,0.2) >= 0 else 0
    current_bar = round(current_bar,2)
    current_date = current_date + timedelta(days=15)
    response = requests.post("http://127.0.0.1:8000/rest_api/VehicleData",json=data,timeout=3)
    print(response)
    sleep(4)