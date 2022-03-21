#!/usr/bin/python3
from time import sleep
import serial
class OBD2Interface:

    def __readValue(self,code):
        print("Writing request for code %s ..." %(code))
        encoded = str.encode(f"{code}\r\r")
        self.ser.write(encoded)
        resp = self.ser.read_until(expected=b'\r\r>')
        return resp  

    def __init__(self,portName,baudRate,timeout):
        self.portName = portName
        self.baudRate = baudRate
        self.timeout = timeout
        self.letters = ["A","B","C","D"]
        self.ser = serial.Serial(port = self.portName, baudrate = self.baudRate, timeout=self.timeout)

    def __parse_response(self, response,expected_values):
        d = {}
        string = response.decode('UTF-8')
        splitted = string.split(" ")
        values = splitted[2:len(splitted) -1]
        if len(values) != expected_values:
            raise ValueError("Expected values: %d, found: %d \n %s" %(expected_values, len(values), ' '.join(values)))
        index = 0
        for v in values:
            print(v)
            d[self.letters[index]] = v
            index+=1
        return d
        
    def get_current_speed(self):
        resp = self.__readValue("010D")
        speed = None
        try:
            values = self.__parse_response(resp,expected_values=1)
            speed = int(values["A"],16)
        except:
            pass
        return speed

    def get_current_rpm(self):
        resp = self.__readValue("010C")
        rpm = None
        try:
            values = self.__parse_response(resp,expected_values=2)
            a = int(values["A"],16)
            b = int(values["B"],16)
            rpm = (256*a+b)/4
        except:
            pass
        return rpm

    def get_current_engine_coolant_temperature(self):
        resp = self.__readValue("0105")
        coolant = None
        try:
            values = self.__parse_response(resp,expected_values=1)
            a = int(values["A"],16)
            coolant = a-40
        except:
            pass
        return coolant
    
    def get_current_throttle_position(self):
        resp = self.__readValue("0147")
        position = None
        try:
            values = self.__parse_response(resp,expected_values=1)
            a = int(values["A"],16)
            position = 100*a/255
        except:
            pass
        return position
    
    def get_current_fuel_level(self):
        resp = self.__readValue("012F")
        level = None
        try:
            values = self.__parse_response(resp,expected_values=1)
            a = int(values["A"],16)
            level = 100*a/255
        except:
            pass
        return level
    def get_engine_oil_temperature(self):
        resp = self.__readValue("015C")
        temp = None
        try:
            values = self.__parse_response(resp,expected_values=1)
            a = int(values["A"],16)
            temp = a - 40
        except:
            pass
        return temp

# delay = 0.1
# with open("values.txt","a") as f:
#     s = OBD2Interface("/dev/ttyUSB0",38400,3)
#     while True:
#         speed = s.get_current_speed()
#         f.write("Speed "+ str(speed) + " " + str(time.time()))
#         f.write("\n")
#         sleep(delay)
#         rpm = s.get_current_rpm()
#         f.write("RPM "+ str(rpm) + " " + str(time.time()))
#         f.write("\n")
#         sleep(delay)
#         coolant = s.get_current_engine_coolant_temperature()
#         f.write("Coolant "+ str(coolant) + " " + str(time.time()))
#         f.write("\n")
#         sleep(delay)
#         th = s.get_current_throttle_position()
#         f.write("Throttle "+ str(th) + " " + str(time.time()))
#         f.write("\n")
#         sleep(delay)
#         fuel = s.get_current_fuel_level()
#         f.write("Fuel "+ str(fuel) + " " + str(time.time()))
#         f.write("\n")
#         sleep(delay)
#         en = s.get_engine_oil_temperature()
#         f.write("Oil temp "+ str(en) + " " + str(time.time()))
#         f.write("\n")