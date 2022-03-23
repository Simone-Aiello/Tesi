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
        with open("buffer.txt","a") as f:
            while True:
                try:
                    current_data = self.queue.get() #take a dictionary containing data
                    print("PRENDO DATI")
                    if not self.write_on_file:
                        print("INIZIO INVIO DATI")
                        response = requests.post("http://localhost:8000/rest_api/VehicleData",json=current_data,timeout=3) #post it to the server (dict to json encoding is done internally)
                        print("DATI INVIATI")
                        dict = response.json() #decode data from json to python dictionary
                        print(f"RESPONSE:{response}")
                        if response.status_code != 200:
                            self.write_on_file = True
                            f.write(json.dumps(current_data)) # list to JSON String
                            f.write('\n')
                    else:
                        dump = json.dumps(current_data)
                        f.write(dump) # list to JSON String
                        f.write("\n")
                        f.flush()
                        print("finisco di scrivere su file")
                except Exception as e:
                    print(e)
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