#!/usr/bin/python3
from threading import Thread
from OBD2Interface import OBD2Interface
import time
from datetime import datetime
import json
class Reader(Thread):
    def __init__(self,queue):
        super().__init__()
        self.queue = queue
    
    def __add_data(self,current_data,sensor,data):
        if data != None:
            dict = {
                "vehicle" : "FG868XN",
                "sensor" : sensor,
                "data" : int(data),
                "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            current_data.append(dict)

    def run(self):
        s = OBD2Interface("/dev/ttyUSB0",38400,3)
        while True:
            time.sleep(2)
            current_data = []
            # speed = 3
            # self.__add_data(current_data,"speed",speed)
            # rpm = 800
            # self.__add_data(current_data,"rpm",rpm)
            # coolant = 80
            # self.__add_data(current_data,"coolant_temperature",coolant)
            # th = 30
            # self.__add_data(current_data,"throttle_position",th)
            # fuel = 40
            # self.__add_data(current_data,"fuel_level",fuel)
            # en = 50
            # self.__add_data(current_data,"engine_oil_temperature",en)
            speed = s.get_current_speed()
            self.__add_data(current_data,'speed',speed)
            rpm = s.get_current_rpm()
            self.__add_data(current_data,'rpm',rpm)
            coolant = s.get_current_engine_coolant_temperature()
            self.__add_data(current_data,'coolant_temperature',coolant)
            th = s.get_current_throttle_position()
            self.__add_data(current_data,'throttle_position',th)
            fuel = s.get_current_fuel_level()
            self.__add_data(current_data,'fuel_level',fuel)
            en = s.get_engine_oil_temperature()
            self.__add_data(current_data,'engine_oil_temperature',en)
            self.queue.put(current_data)
            #print(json.dumps(current_data))