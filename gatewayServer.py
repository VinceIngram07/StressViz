from flask import Flask
from flask_socketio import SocketIO, send
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import argparse
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def print_handler(address, *args):
    print(f"Received data from {address}: {args}")
    socketio.send(args)

def start_osc_server(ip, port, dispatcher):
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

@socketio.on('connect')
def handle_connect():
    print('Client connected')   

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="172.20.10.10", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()
    dispatcher.map("/EmotiBit/0/EDA", print_handler)
    # dispatcher.map("/EmotiBit/0/HR", print_handler)
    # dispatcher.map("/EmotiBit/0/TEMP", print_handler)

    osc_server_thread = threading.Thread(target=start_osc_server, args=(args.ip, args.port, dispatcher))
    osc_server_thread.start()

    socketio.run(app)


# from flask import Flask
# from flask_socketio import SocketIO
# from pythonosc import dispatcher
# from pythonosc import osc_server
# import threading

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app, cors_allowed_origins="*")

# def eda_handler(unused_addr, args, eda):
#     print("EDA handler called with data: ", eda)
#     socketio.emit('eda', eda)

# def hr_handler(unused_addr, args, hr):
#     print("HR handler called with data: ", hr)
#     socketio.emit('hr', hr)

# def temp_handler(unused_addr, args, temp):
#     print("TEMP handler called with data: ", temp)
#     socketio.emit('temp', temp)
#     socketio.emit('temp', temp)

# dispatcher = dispatcher.Dispatcher()
# dispatcher.map("/EmotiBit/0/EDA", eda_handler, "EDA")
# dispatcher.map("/EmotiBit/0/HR", hr_handler, "HR")
# dispatcher.map("/EmotiBit/0/TEMP", temp_handler, "TEMP")

# def start_osc_server():
#     try:
#         print("Starting OSC server...")
#         server = osc_server.ThreadingOSCUDPServer(("localhost", 5005), dispatcher)
#         print("Serving on {}".format(server.server_address))
#         server.serve_forever()
#     except Exception as e:
#         print("Error in OSC server: ", e)

# print("Starting OSC server thread...")
# osc_server_thread = threading.Thread(target=start_osc_server)
# osc_server_thread.start()
# print("OSC server thread started.")

# if __name__ == '__main__':
#     socketio.run(app)