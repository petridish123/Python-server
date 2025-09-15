import json, asyncio, websockets, game


PORT = 8765

class Server:

    def __init__(self,NUM_PLAYERS : int ,url = "localhost", port = PORT):
        self.connected = set()
        self.ID_PLAYERS : dict[int:websockets.ClientConnection] = {} #might be a client connection, not server
        self.NUM_PLAYERS = NUM_PLAYERS
        self.game = game.game()
        self.url = url
        self.port = port

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
                    await ws.send(json.dumps({"STARTGAME" : [1,2]}).encode())

            async for msg in websocket:
                print(f"received message: {msg}")

        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")
        finally:
            self.connected.remove(websocket)
            self.game.remove_player(new_player_id)
            for client in self.connected:
                await client.send(json.dumps({"MINUSPLAYER" : new_player_id}).encode())
            print(f"Client removed. Total: {len(self.connected)}")

    async def main(self):
        async with websockets.serve(self.handler, self.url, self.port):
            await asyncio.Future()


if __name__ == "__main__":
    try:
        print("Starting Server...")
        print("listening on port:",str(PORT))
        server = Server(2)
        asyncio.run(server.main())
    except KeyboardInterrupt:
        print("Killed for keyboard interrupt")