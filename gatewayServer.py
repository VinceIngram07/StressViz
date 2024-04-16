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

    osc_server_thread = threading.Thread(target=start_osc_server, args=(args.ip, args.port, dispatcher))
    osc_server_thread.start()

    socketio.run(app)
