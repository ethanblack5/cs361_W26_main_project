import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

def sort_dict(dictionary):
    sorted_obj = dict(sorted(dictionary.items()))
    return sorted_obj

while True:
    msg = socket.recv_json()
    sorted_dict = sort_dict(msg)
    time.sleep(0.1)
    socket.send_json(sorted_dict)