import asyncio
import argparse
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import websockets

async def send_data(websocket, path):
    try:
        while True:
            await asyncio.sleep(0.1)  # Adjust the sleep duration based on your needs
            # Replace the following line with the data you want to send
            data = "Your data here"
            print(f"Sending data: {data}")
            await websocket.send(data)
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed unexpectedly: {e}")
    except Exception as e:
        print(f"Error sending data: {e}")
    finally:
        await websocket.close()

def print_handler(address, *args):
    print(f"Received data from {address}: {args}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="172.20.10.10", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()

    # Add dispatcher mappings for each data type
    dispatcher.map("/EmotiBit/0/EDA", print_handler)
    # Add mappings for other data types as needed

    # Start the OSC server
    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))

    # Start the WebSocket server
    try:
        start_server = websockets.serve(send_data, "localhost", 8765)  # Adjust the port as needed
        print("WebSocket server started on ws://localhost:8765")
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        print(f"WebSocket server error: {e}")
