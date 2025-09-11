


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
import game

PORT : int = 8765
NUM_PLAYERS = 2


class Server:

    def __init__(self,):
        self.game = game.game()
        self.connected : set = set()
        self.game_started = False
    
    def check_round_submitted(self,) -> bool:
        
        return False
    
    def move_to_next_round(self):
        pass
    
    async def add_player(self):
        ID = self.game.make_ID()
        new_player = game.player(None,ID,0)
        self.game.add_player(ID, new_player)
        return ID

    def encode_message(self, title, message):
        new_message = {}
        if type(title) is list and type(message) is list and len(title) == len(message):
            for sub_title, sub_message in zip(title, message):
                new_message[sub_title] = sub_message
            return json.dumps(new_message).encode()
        else:
            return json.dumps({title: message}).encode()
    # @qasync.asyncSlot()
    async def handle_message(self, message,websocket) -> None:
        print(message)
        message_str : str = json.loads(message)
        if self.game.num_players >= NUM_PLAYERS and not self.game_started:
                    print("HEEHEE")
                    await websocket.send(json.dumps({"STARTGAME": True, "PLAYERS":self.game.id_players}).encode())
    

    # @qasync.asyncSlot()
    async def server_handler(self, websocket) -> None:
        try:
            message = await websocket.recv()
            self.connected.add(websocket)
            new_player_id = await self.add_player()
            await websocket.send(self.encode_message(["ID", "RESPONSE"], [new_player_id, "CONNECTED"]))
            print("Client Connected")

            while self.game.num_players < NUM_PLAYERS and not self.game_started:

                message = await websocket.recv()
                print(f"Server received: {message}")
                #Handle message here
                await websocket.send(f"Echo: {message}")
                

               

        # Exceptions handling        
        except websockets.exceptions.ConnectionClosedOK:
            print(f"Client {websocket.remote_address} disconnected gracefully.")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Client {websocket.remote_address} disconnected with error: {e}")
        finally:
            print(f"Cleanup for client {websocket.remote_address}.\nRemoving ID: {new_player_id}")
            self.connected.remove(websocket)
            self.game.remove_player(new_player_id, None)


    # @qasync.asyncSlot()
    async def main(self):
        print("Server Started")
        async with websockets.serve(self.server_handler, "localhost", PORT):
            await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        print("Starting Server...")
        print("Listening on port: " + str(PORT))
        server = Server()
        asyncio.run(server.main())
    except KeyboardInterrupt:
        print("Killed for Keyboard interrupts")
        exit()