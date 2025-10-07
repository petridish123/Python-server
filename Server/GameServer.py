import json, asyncio, websockets
import Shared.game
import Shared.signals
PORT = 8765

class Server:

    def __init__(self,NUM_PLAYERS : int  = 1 ,url : str = "localhost", port : int = PORT):
        self.connected = set()
        self.ID_PLAYERS : dict[int:websockets.ClientConnection] = {} #might be a client connection, not server
        self.NUM_PLAYERS = NUM_PLAYERS
        self.game = Shared.game()
        self.url = url
        self.port = port
        self.t = self.game.round
        self.scores = {}
        self.update_round = Shared.signals.Signal()
        self.start_game = Shared.signals.Signal()
        

    async def handler(self, websocket : websockets.ClientConnection):
        
        # Adding the connection to the connected set
        self.connected.add(websocket)

        # Adding the player to the game's players and to the server's
        new_player_id = self.game.add_player()
        self.ID_PLAYERS[new_player_id] = websocket
        
        await websocket.send(json.dumps({"ID":new_player_id}).encode())

        try:

            if self.game.num_players == self.NUM_PLAYERS:
                for ws in self.connected:
                    print(self.game.num_players)
                    await self.start_game.emit(self.ID_PLAYERS)
                    await ws.send(json.dumps({"STARTGAME" : list(self.ID_PLAYERS.keys())}).encode())

            async for msg in websocket:
                print(f"received message: {msg}")
                await self.handle_message(msg)


        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")
        finally:
            self.connected.remove(websocket)
            self.game.remove_player(new_player_id)
            self.ID_PLAYERS.pop(new_player_id)
            for client in self.connected:
                await client.send(json.dumps({"MINUSPLAYER" : new_player_id}).encode())
            print(f"Client removed. Total: {len(self.connected)}")

    async def handle_message(self, msg):
        msg = json.loads(msg.decode())
        if "ID" in msg and "ALLOCATION" in msg:
            if self.game.set_score(msg["ID"],msg["ALLOCATION"]):
                
                self.game.new_round()
                self.t = self.game.round
                await self.update_round.emit(self.t)
                for player in self.connected:
                    await player.send(json.dumps({"ROUND" : self.game.round}).encode())

        else:
            print(msg)

    async def main(self):
        print("Starting Server...")
        print("listening on port:",str(PORT))
        async with websockets.serve(self.handler, self.url, self.port):
            await asyncio.Future()
    
    async def _close(self):
        print("Closing server")
        
        


if __name__ == "__main__":
    try:

        server = Server(3)
        asyncio.run(server.main())
    except KeyboardInterrupt:
        server.game.save()
        print("Killed for keyboard interrupt")