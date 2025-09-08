


# """
# this class is going to start a python server using websockets

# It is going to connect to a certain amount of clients and then start the game.
# When started, it will send a packet to the clients with information about the 
# other clients (Id, and amount)

# The clients will give their input and that will be processed on the server then sent
# back.


# """

# import asyncio
# import json
# from websockets.asyncio.server import serve
# import time

# last_message_time = None  # Global timestamp of the last received message
# server_task = None  # Will hold reference to the server
# shutdown_event = asyncio.Event()  # To trigger full shutdown

# TIMEOUT = 20
# PORT = 4001


# connected = set() # this is for the peers/ connections


# async def echo(websocket):

#     print("A client connected")
#     connected.add(websocket)
   
 

#     async for message in websocket:
#         print("Recieved message from client " + message)
#         await websocket.send("Response: " + message)





# async def parse_messages(websocket):
#     global last_message_time
#     try:
#         init_message_str = await asyncio.wait_for(websocket.recv(), timeout= TIMEOUT)
    
#     except asyncio.TimeoutError:
#         await websocket.close()
#         return


# async def main():
#     global server_task, last_message_time

#     last_message_time = asyncio.get_event_loop().time() # initialize the first timestamp

#     server = await serve(echo, "localhost", PORT)
#     print("Server running on ws://localhost:4001")

#     await shutdown_event.wait()
    
#     server.close()
#     await server.wait_closed()


# if __name__ == "__main__":
#     print("Starting Server...")
#     try:
#         # asyncio.get_event_loop().run_until_complete(main())
#         asyncio.run(main())
#     except Exception as e:
#         print(e)



import asyncio
import websockets
import json
import qasync

PORT : int = 8765

connected : set = set()


async def handle_message(message) -> None:
    print(message)
    message_str : str = json.loads(message)
    

async def server_handler(websocket) -> None:
    try:
        message = await websocket.recv()
        connected.add(websocket)
        print("Client Connected")
        await websocket.send("CONNECTED")
        while True:
            message = await websocket.recv()
            print(f"Server received: {message}")
            #Handle message here
            await websocket.send(f"Echo: {message}")
            print("sent")

    # Exceptions handling        
    except websockets.exceptions.ConnectionClosedOK:
        print(f"Client {websocket.remote_address} disconnected gracefully.")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Client {websocket.remote_address} disconnected with error: {e}")
    finally:
        print(f"Cleanup for client {websocket.remote_address}.")
        connected.remove(websocket)
        print(connected)

async def main():
    print("Server Started")
    async with websockets.serve(server_handler, "localhost", PORT):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        print("Starting Server...")
        print("Listening on port: " + str(PORT))
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Killed for Keyboard interrupts")
        exit()