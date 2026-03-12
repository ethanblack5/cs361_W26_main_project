import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5558")

while True:
    msg = socket.recv_json()
    time.sleep(0.1)
    with open('download.txt', 'w') as f:
        print(msg, file=f)
    socket.send_string("Download complete.")