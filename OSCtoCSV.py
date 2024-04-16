import argparse
import csv
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

# Initialize variables to store received data
eda_data = None
hr_data = None
temp_data = None

def write_to_csv(eda, hr, temp, csv_writer):
    csv_writer.writerow({'EDA': eda, 'HR': hr, 'TEMP': temp})

def osc_handler(address, *args):
    global eda_data, hr_data, temp_data

    print(f"Received data from {address}: {args}")
    
    # Check the address and update corresponding data
    if address == "/EmotiBit/0/EDA":
        eda_data = args[0] if len(args) > 0 else None
    elif address == "/EmotiBit/0/HR":
        hr_data = args[0] if len(args) > 0 else None
    elif address == "/EmotiBit/0/TEMP":
        temp_data = args[0] if len(args) > 0 else None

    # If all data is available, write to CSV
    if eda_data is not None and hr_data is not None and temp_data is not None:
        write_to_csv(eda_data, hr_data, temp_data, csv_writer)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="172.20.10.10", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
    parser.add_argument("--output", default="osc_data.csv", help="Output CSV file")
    args = parser.parse_args()

    with open(args.output, 'w', newline='') as csvfile:
        fieldnames = ['EDA', 'HR', 'TEMP']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()

        dispatcher = Dispatcher()
        dispatcher.map("/EmotiBit/0/HR", osc_handler)
        dispatcher.map("/EmotiBit/0/EDA", osc_handler)
        dispatcher.map("/EmotiBit/0/TEMP", osc_handler)

        server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
        print(f"Writing OSC data to {args.output}...")
        print("Press Ctrl+C to stop.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Stopping server...")
            server.server_close()
