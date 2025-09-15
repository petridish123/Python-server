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
    
    """
    I need two functions, one that listens and one that sends. This will allow the game to basically always be listening 
    and processing the functions
    """
    async def receive_message(self, ws,id):

        message = await ws.recv()
        await self.handle_message(message.decode(), ws)
 
    async def await_time(self):
        await asyncio.sleep(1)

    # @qasync.asyncSlot()
    async def server_handler(self, websocket) -> None:
        try:
            message = await websocket.recv()
            self.connected.add(websocket)
            new_player_id = await self.add_player()
            await websocket.send(self.encode_message(["ID", "RESPONSE"], [new_player_id, "CONNECTED"]))
            print("Client Connected")

            while self.game.num_players < NUM_PLAYERS or not self.game_started:
                # Needs to do a asyncio.wait thingy so it can cancel the task and go through!

                receive_task = asyncio.create_task(self.receive_message(websocket, new_player_id))
                wait_task = asyncio.create_task(self.await_time())
                done, pending = await asyncio.wait([receive_task,wait_task], return_when=asyncio.FIRST_COMPLETED)
                for task in pending:
                    print(f'task not completed : {task}')
                    task.cancel()
                # message = await websocket.recv()
                # print(f"Server received: {message}")
                #Handle message here
                # await websocket.send(f"Echo: {message}")
                

               

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