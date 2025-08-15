import asyncio
import websockets

LOT_ID = 1  # Replace with the lot ID you want to subscribe to

async def main():
    uri = f"ws://localhost:8000/ws/lots/{LOT_ID}"
    async with websockets.connect(uri) as websocket:
        print(f"Connected to lot {LOT_ID} WebSocket!")

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
    asyncio.run(main())