#!/usr/bin/python3
from threading import Thread
import json
import requests
class Sender(Thread):
    def __init__(self,queue):
        super().__init__()
        self.queue = queue
        self.write_on_file = False
    
    def run(self):
        while True:
            #Take a dictionary containing data
            current_data = self.queue.get() 
            #Post data to the server (dict to json encoding is done internally)
            response = requests.post("http://localhost:8000/rest_api/VehicleData",json=current_data,timeout=3) 



# [{'vehicle': 'FG868XN', 'sensor': 'speed', 'data': 3, 'timestamp': '2022-04-21 14:21:27'},
# {'vehicle': 'FG868XN', 'sensor': 'rpm', 'data': 800, 'timestamp': '2022-04-21 14:21:27'},
# {'vehicle': 'FG868XN', 'sensor': 'coolant_temperature', 'data': 80, 'timestamp': '2022-04-21 14:21:27'},
# {'vehicle': 'FG868XN', 'sensor': 'throttle_position', 'data': 30, 'timestamp': '2022-04-21 14:21:27'},
# {'vehicle': 'FG868XN', 'sensor': 'fuel_level', 'data': 40, 'timestamp': '2022-04-21 14:21:27'},
# {'vehicle': 'FG868XN', 'sensor': 'engine_oil_temperature', 'data': 50, 'timestamp': '2022-04-21 14:21:27'}]
#'[{"vehicle": "FG868XN", "sensor": "speed", "data": 3, "timestamp": "2022-04-21 14:21:27"}]'