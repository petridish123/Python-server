import asyncio
import websockets

url = "ws://localhost:8765"

async def listen():
    async with websockets.connect(url) as ws:
        await ws.send("HIHO")
        while True:
            msg = await ws.recv()
            print(msg)


if __name__ == "__main__":
    try:
        asyncio.run(listen())
    except Exception as e:
        print(e)