import asyncio
import websockets

connected_clients = set()

async def handler(websocket):
    # Register new client
    connected_clients.add(websocket)
    print(f"Client connected. Total: {len(connected_clients)}")

    try:
        # If 3 clients are connected, broadcast a message
        if len(connected_clients) == 3:
            message = "3 clients connected! Broadcasting message."
            await asyncio.gather(*(client.send(message) for client in connected_clients))

        # Always listen for incoming messages from this client
        async for msg in websocket:
            print(f"Received from client: {msg}")

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected_clients.remove(websocket)
        print(f"Client removed. Total: {len(connected_clients)}")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Server started on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
