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
        with open("buffer.txt","w") as f:
            while True:
                try:
                    current_data = {
                        "values" : [self.queue.get()] #take a dictionary containing data
                    }
                    if not self.write_on_file:
                        response = requests.post("http://localhost:8080",json=current_data,timeout=3) #post it to the server (dict to json encoding is done internally)
                        dict = response.json() #decode data from json to python dictionary
                        if response.status_code != 200:
                            self.write_on_file = True
                            f.write(json.dumps(current_data)) # list to JSON String
                            f.write('\n')
                    else:
                        f.write(json.dumps(current_data)) # list to JSON String
                        f.write('\n')
                except:
                    self.write_on_file = True



# {
#     "speed" : {
#         "data": int,
#         "timestamp": float
#     },
#     "rpm" : {
#         "data": int,
#         "timestamp": float
#     },
#     "coolant_temperature" : {
#         "data": int,
#         "timestamp": float
#     },
#     "throttle_position" : {
#         "data": int,
#         "timestamp": float
#     },
#     "fuel_level" : {
#         "data": int,
#         "timestamp": float
#     },
#     "engine_oil_temperature" : {
#         "data": int,
#         "timestamp": float                    
#     },
# }