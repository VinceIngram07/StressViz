# from flask import Flask, request
# import threading
# import argparse
# import csv
# import os
# from pythonosc.dispatcher import Dispatcher
# from pythonosc import osc_server
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)
# server = None
# server_thread = None

# hr = None
# eda = None
# temp = None

# def write_to_csv(filename):
#     global hr, eda, temp
#     with open(filename, 'a', newline='') as f:
#         writer = csv.writer(f)
#         if os.stat(filename).st_size == 0:
#             writer.writerow(['HR', 'EDA', 'TEMP'])
#         writer.writerow([hr, eda, temp])

# def print_handler(address, *args):
#     global hr, eda, temp
#     print(f"Received data from {address}: {args}")
#     if address == "/EmotiBit/0/HR":
#         hr = args[0]
#     elif address == "/EmotiBit/0/EDA":
#         eda = args[0]
#     elif address == "/EmotiBit/0/TEMP":
#         temp = args[0]
#     write_to_csv('data.csv')

# @app.route('/start', methods=['POST'])
# def start():
#     global server, server_thread
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--ip", default="172.20.10.10", help="The ip to listen on")
#     parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
#     args = parser.parse_args()

#     dispatcher = Dispatcher()
#     dispatcher.map("/EmotiBit/0/HR", print_handler)
#     dispatcher.map("/EmotiBit/0/EDA", print_handler)
#     dispatcher.map("/EmotiBit/0/TEMP", print_handler)

#     server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
#     server_thread = threading.Thread(target=server.serve_forever)
#     server_thread.start()

#     return 'Started'

# @app.route('/stop', methods=['POST'])
# def stop():
#     global server, server_thread
#     if server:
#         server.shutdown()
#         server_thread.join()
#         server = server_thread = None

#     return 'Stopped'

# if __name__ == "__main__":
#     app.run(port=8080)

#With Streaming:

from flask import Flask, request
from flask_socketio import SocketIO, emit
import threading
import argparse
import csv
import os
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

app = Flask(__name__)
socketio = SocketIO(app)
server = None
server_thread = None

hr = None
eda = None
temp = None

import csv  # Import the missing csv module

def write_to_csv(filename):
    global hr, eda, temp
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)  # Define the writer variable
        if os.stat(filename).st_size == 0:
            writer.writerow(['HR', 'EDA', 'TEMP'])
        writer.writerow([hr, eda, temp])

def print_handler(address, *args):
    global hr, eda, temp
    print(f"Received data from {address}: {args}")
    if address == "/EmotiBit/0/HR":
        hr = args[0]
    elif address == "/EmotiBit/0/EDA":
        eda = args[0]
    elif address == "/EmotiBit/0/TEMP":
        temp = args[0]
    write_to_csv('data.csv')
    socketio.emit('data', {'hr': hr, 'eda': eda, 'temp': temp})

@app.route('/start', methods=['POST'])
def start():
    global server, server_thread
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="172.20.10.10", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()
    dispatcher.map("/EmotiBit/0/HR", print_handler)
    dispatcher.map("/EmotiBit/0/EDA", print_handler)
    dispatcher.map("/EmotiBit/0/TEMP", print_handler)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    return 'Started'

@app.route('/stop', methods=['POST'])
def stop():
    global server, server_thread
    if server:
        server.shutdown()
        server_thread.join()
        server = server_thread = None

    return 'Stopped'

if __name__ == "__main__":
    socketio.run(app, port=8080)