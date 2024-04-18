import argparse
import csv
import os
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

hr = None
eda = None
temp = None

def write_to_csv(filename):
    global hr, eda, temp
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="172.20.10.10", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()
    dispatcher.map("/EmotiBit/0/HR", print_handler)
    dispatcher.map("/EmotiBit/0/EDA", print_handler)
    dispatcher.map("/EmotiBit/0/TEMP", print_handler)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()