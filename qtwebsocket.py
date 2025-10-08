from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QLineEdit, QVBoxLayout, QGridLayout
)
import sys
from PyQt6.QtCore import Qt

from PyQt6.QtGui import QIcon
import json
import websockets
from qasync import QEventLoop, asyncSlot
import asyncio



from Shared.game import player, sub_player

url = "127.0.0.1"
PORT = 8765


class QtWebsocket(QWidget):

    def __init__(self,):
        super().__init__()
        self.game_running = False

        self.ID = None

        self.setWindowTitle("Client")

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.resize(200,150)
        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.send_allocation) # connect to a function
        self.layout.addWidget(self.button,0,1)
        
        self.round_num = 0
        self.round_num_label = QLabel("Round: " + str(self.round_num))
        self.layout.addWidget(self.round_num_label, 0 , 0)


        self.row = 1
        self.player : player|None = None

        self.players = {} #ID : row

        self.round_allocations = {}
        self.cur_round = 0

        self.run()

    def change_round_num(self, new_int: int):
        self.round_num = new_int
        self.round_num_label.setText("Round: " + str(self.round_num))

    @asyncSlot()    
    async def send_message(self, message = "Hello!"):
        new_message = {
            "MESSAGE":message
        }
        new_message = json.dumps(new_message).encode()
        await self.socket.send(new_message)

    @asyncSlot()
    async def send_allocation(self):
        if not self.player or not self.game_running: 
            print("Game not running or Player not created")
            return
        self.round_allocations = {int(ID):self.players[ID].current_allocation for ID in list(self.players.keys())}
        new_message = {
            "ALLOCATION" : self.round_allocations,
            "ID" : self.player.name,
        }
        new_message = json.dumps(new_message).encode()
        await self.socket.send(new_message)

    def make_player(self, ID):
        self.player = player(None, ID, 0)
        self.ID = ID

    async def handle_message(self,message):
        message = json.loads(message.decode())
        print(message)
        if "ID" in message:
            self.make_player(message["ID"])

        if "STARTGAME" in message:
            self.game_running = True
            for i in range(len(message["STARTGAME"])):
                player_id = message["STARTGAME"][i]
                if not self.ID:
                    break
                elif player_id == self.ID:
                    continue
                new_player = sub_player(player_id,self.layout,self.row)
                self.row += 1
                new_player.add_player()
                self.players[player_id] = new_player
            self.setWindowTitle(f"Player : {self.ID}")
            # pass # Create multiple players here
        if "MINUSPLAYER" in message:
            old_player = self.remove_player(message["MINUSPLAYER"])
            old_player.off_yerself()
            move_row  = old_player.cur_row
            for player in self.players:
                pl = self.players[player]
                if pl.cur_row > move_row:
                    print("MOVING")
                    # pl.change_row(pl.cur_row-1)
                else:
                    print(f"Oldrow : {move_row} and {pl.cur_row}")
            sys.exit()
        if "ROUND" in message:
            self.change_round_num(message["ROUND"])
                    
    
    def remove_player(self, ID):
        old_player = self.players[ID]
        self.players.pop(ID)
        return old_player

    @asyncSlot()
    async def run(self):
        self.socket = await websockets.connect("ws://localhost:8765")
        await self.socket.send(json.dumps({"REQUEST" : "CONNECT"}).encode())
        # message = await self.socket.recv()
        # print(message)
        # await self.handle_message(message)
        while True:
            try:
                message = await self.socket.recv()
                await self.handle_message(message)
            except KeyboardInterrupt:
                print("AWW")
                sys.exit()
            except websockets.exceptions.ConnectionClosed:
                print("Client disconnected")
                sys.exit()

def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    # set_style(app, "C:/Users/Mango/Desktop/Python_server_client/Python-server/rules/style.css")
    window = QtWebsocket()
    window.show()
    # sys.exit(app.exec())
    with loop:
        loop.run_forever()

def set_style(app : QApplication, sheet : str):
    with open(sheet, "r") as f:
        if not f:
            return False
        lines = f.read()
        # print(lines) 
        
        app.setStyleSheet(lines)


if __name__ == "__main__":
    main()

"""
TODO:
- I need to make a remove player from the GUI
- if an ID is already in the players, don't add it again
- send ID in the packet on server side
- make the buttons record score on client
- make scores get sent to server side
- process scores and do something with them (print or send back to client to display)


"""