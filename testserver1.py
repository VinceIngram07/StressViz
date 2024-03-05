import asyncio
import websockets
import random

async def send_random_data(websocket, path):
    try:
        while True:
            await asyncio.sleep(1)  # Adjust the sleep duration based on your needs
            random_number = random.randint(1, 100)
            print(f"Sending random number: {random_number}")
            await websocket.send(str(random_number))
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed unexpectedly: {e}")
    except Exception as e:
        print(f"Error sending data: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    start_server = websockets.serve(send_random_data, "localhost", 8765)  # Adjust the port as needed
    print("WebSocket server started on ws://localhost:8765")

    try:
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        print(f"WebSocket server error: {e}")
