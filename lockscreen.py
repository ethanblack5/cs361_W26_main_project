import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5557")

current_password = None
locked = False

while True:
    msg = socket.recv_string()

    if msg.startswith("SET_PASSWORD:"):
        current_password = msg.replace("SET_PASSWORD:", "", 1)
        socket.send_string("Password created.")

    elif msg == "LOCK":
        if current_password is None:
            socket.send_string("No password set.")
        else:
            locked = True
            socket.send_string("activate")

    elif msg.startswith("UNLOCK:"):
        attempt = msg.replace("UNLOCK:", "", 1)
        if current_password == attempt:
            locked = False
            socket.send_string("Pass")
        else:
            socket.send_string("Fail")

    else:
        socket.send_string("Unknown request.")