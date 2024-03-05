import argparse
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

def print_handler(address, *args):
    print(f"Received data from {address}: {args}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="172.20.10.10", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()
    
    # Add dispatcher mappings for each data type
    # dispatcher.map("/EmotiBit/0/PPG:RED", print_handler)
    # dispatcher.map("/EmotiBit/0/PPG:IR", print_handler)
    # dispatcher.map("/EmotiBit/0/PPG:GRN", print_handler)
    # dispatcher.map("/EmotiBit/0/HR", print_handler)
    dispatcher.map("/EmotiBit/0/EDA", print_handler)
    # dispatcher.map("/EmotiBit/0/SCR:AMP", print_handler)
    # dispatcher.map("/EmotiBit/0/SCR:RIS", print_handler)
    # dispatcher.map("/EmotiBit/0/SCR:FREQ", print_handler)
    # Add mappings for other data types as needed

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
