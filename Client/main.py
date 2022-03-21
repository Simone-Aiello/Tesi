#!/usr/bin/python3
from queue import Queue
from Reader import Reader
from Sender import Sender
if __name__ == "__main__":
    buffer_queue = Queue(20)
    r = Reader(buffer_queue)
    s = Sender(buffer_queue)
    r.start()
    s.start()
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