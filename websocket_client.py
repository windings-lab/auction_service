import argparse
import asyncio
import websockets

async def main(lot_id: int, url: str, port: int):
    uri = f"ws://{url}:{port}/ws/lots/{lot_id}"
    async with websockets.connect(uri) as websocket:
        print(f"Connected to lot {lot_id} WebSocket!")

        # Example: send a message to the server
        await websocket.send("Hello server!")

        # Listen for messages from server
        try:
            while True:
                message = await websocket.recv()
                print("Received:", message)
        except websockets.ConnectionClosed:
            print("WebSocket connection closed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebSocket client for lot updates")
    parser.add_argument("lot_id", type=int, help="ID of the lot to subscribe to", default=1)
    parser.add_argument("--url", type=str, help="url to connect to", default="localhost")
    parser.add_argument("--port", type=int, help="port to connect to", default=8000)
    args = parser.parse_args()

    try:
        asyncio.run(main(args.lot_id, args.url, args.port))
    except KeyboardInterrupt:
        pass