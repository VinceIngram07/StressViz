import argparse
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import asyncio
import websockets

# Global variable to store the WebSocket connection
websocket_clients = set() 

async def send_to_clients(data):
    # Send data to all connected clients
    for client in websocket_clients:
        await client.send(data)

async def print_handler(address, *args):
    data = f"Received data from {address}: {args}"
    print(data)
    await send_to_clients(data)

async def server(websocket, path):
    # Add the new WebSocket client to the set
    websocket_clients.add(websocket)
    try:
        # Keep the connection open
        await websocket.wait_closed()
    finally:
        # Remove the WebSocket client when the connection is closed
        websocket_clients.remove(websocket)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="172.20.10.10", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()
    dispatcher.map("/EmotiBit/0/EDA", print_handler)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))

    # Start the WebSocket server on a separate thread
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(server, "localhost", 8765)
    )

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
