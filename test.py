# from flask import Flask
# from flask_socketio import SocketIO
# from pythonosc.dispatcher import Dispatcher
# from pythonosc import osc_server
# import argparse
# import threading

# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")

# def print_handler(address, *args):
#     if address in ['/EmotiBit/0/TEMP', '/EmotiBit/0/EDA', '/EmotiBit/0/HR']:
#         print(f"Received data from {address}: {args}")
#         # Emit data to the corresponding namespace based on the address
#         if address == '/EmotiBit/0/TEMP':
#             print('Emitting data to stream1')
#             socketio.emit('stream1_data', {'address': address, 'data': args}, namespace='/stream1')
#         elif address == '/EmotiBit/0/EDA':
#             print('Emitting data to stream2')
#             socketio.emit('stream2_data', {'address': address, 'data': args}, namespace='/stream2')
#         elif address == '/EmotiBit/0/HR':
#             print('Emitting data to stream3')
#             socketio.emit('stream3_data', {'address': address, 'data': args}, namespace='/stream3')


# def start_osc_server(ip, port, dispatcher):
#     server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
#     print("Serving on {}".format(server.server_address))
#     server.serve_forever()

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--ip", default="172.20.10.10", help="The ip to listen on")
#     parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
#     args = parser.parse_args()

#     dispatcher = Dispatcher()
#     dispatcher.map("/EmotiBit/0/EDA", print_handler)
#     dispatcher.map("/EmotiBit/0/HR", print_handler)
#     dispatcher.map("/EmotiBit/0/TEMP", print_handler)

#     osc_server_thread = threading.Thread(target=start_osc_server, args=(args.ip, args.port, dispatcher))
#     osc_server_thread.start()

#     socketio.run(app)


import pandas as pd

# Load the dataset
data = pd.read_csv("Test1_data.csv")

# Count the duplicate rows
duplicate_rows = data.duplicated().sum()

print(f"Number of duplicate rows: {duplicate_rows}")