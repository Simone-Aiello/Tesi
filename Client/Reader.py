#!/usr/bin/python3
from threading import Thread
from OBD2Interface import OBD2Interface
import time
class Reader(Thread):
    def __init__(self,queue):
        super().__init__()
        self.queue = queue
    
    def __add_data(self,current_data,key,data):
        if data != None:
            current_data[key] = {
                'data' : data,
                'timestamp' : time.time(),
            }

    def run(self):
        #s = OBD2Interface("/dev/ttyUSB0",38400,3)
        while True:
            current_data = {"speed":3}
            # speed = s.get_current_speed()
            # self.__add_data(current_data,'speed',speed)
            # rpm = s.get_current_rpm()
            # self.__add_data(current_data,'rpm',rpm)
            # coolant = s.get_current_engine_coolant_temperature()
            # self.__add_data(current_data,'coolant_temperature',coolant)
            # th = s.get_current_throttle_position()
            # self.__add_data(current_data,'throttle_position',th)
            # fuel = s.get_current_fuel_level()
            # self.__add_data(current_data,'fuel_level',fuel)
            # en = s.get_engine_oil_temperature()
            # self.__add_data(current_data,'engine_oil_temperature',en)
            self.queue.put(current_data)
            #print(current_data)
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
            
# {
#     "values" : [
#             {
#                 "speed":{
#                     "data" : 3,
#                 }
#             },
#             {

#             }
#         ]
# }