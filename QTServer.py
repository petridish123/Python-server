

import Server.GameServer


from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QLineEdit, QVBoxLayout, QGridLayout
)
import sys
from PyQt6.QtCore import Qt,QTimer
from PyQt6.QtGui import QIcon
import json
import websockets
from qasync import QEventLoop, asyncSlot
import asyncio

import Shared.game

"""
Purpose of this class:
Create a server from the gameserver class and give it a qt interface

"""



class QTServer(QWidget):

    def __init__(self, num_players : int = 1, url : str = "localhost", port : int = 8765):
        super().__init__()


        self.server = Server.GameServer.Server(num_players, url, port)
        
        self.new_window = None
        self.layout : QGridLayout = QGridLayout()
        self.setLayout(self.layout)

        self.event_button =QPushButton("Create Event")
        self.event_button.clicked.connect(self.create_event)
        self.layout.addWidget(self.event_button)

        QTimer.singleShot(0, lambda: asyncio.create_task(self.run()))


    def create_event(self):
        if self.new_window is not None:
            self.new_window.close()
            self.new_window.deleteLater()
        print("attempting to create event window")
        self.new_window = eventWindow(self.server.ID_PLAYERS, self)
        self.new_window.show()
   
    
    def closeEvent(self, a0):
        print("Closing and cleaning up")
        # await self.server._close()
        if hasattr(self.server, "_close"):
            asyncio.create_task(self.server._close())
        a0.accept()
    
    
    # @asyncSlot()
    async def run(self):
        await self.server.main()


class eventWindow(QWidget):
    def __init__(self, players : dict, mainwindow : QTServer):
        super().__init__()

        self.layout : QGridLayout = QGridLayout()
        self.setLayout(self.layout)

        self.label_names = {0:"From", 1:"To", 2:"Watcher"}

        self.to_col = 1
        self.from_col = 0
        self.watcher_col = 2

        self.cur_row = 0

        self.data = {}

        
        """
        What I want is to get all the players and their ID's
        Then make the events based on their IDS
        
        """
        for i in range(self.from_col, self.watcher_col + 1):
            label = QLabel(self.label_names[i])
            self.layout.addWidget(label, self.cur_row, i)
        self.cur_row += 1
        for ID in players:
            """Create a row for the player. Watcher, to and from"""
            self.create_row(ID)
        
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.close)
        self.layout.addWidget(self.submit_button, self.cur_row, 0)
    
    def info_button_creator(self, ID : int,to : bool = False, from_ : bool = False, watcher :bool = False):
        self.data[ID] = {"To" : False, "From": False, "Watcher": False}
        def _():
            if to:
                self.data[ID]["To"] = True
            elif from_:
                self.data[ID]["From"] = True
            elif watcher:
                self.data[ID]["Watcher"] = True

        return _

    def create_row(self, ID : int):
        for i in self.label_names:
            col = int(i)
            name = f"Player {ID}"
            button1 = QPushButton(name)
            # button1.clicked.connect(callable)
            if col == 0 :
                button1.clicked.connect(self.info_button_creator(ID,from_ = True))
            elif col == 1:
                button1.clicked.connect(self.info_button_creator(ID,to = True))
            elif col == 2:
                button1.clicked.connect(self.info_button_creator(ID,watcher= True))
                            
            self.layout.addWidget(button1, self.cur_row, col)
        self.cur_row += 1



    def close(self):
        # Send the event to the server
        print(self.data)
        super().close()
        self.deleteLater()


"""
TODO:
- Make the qtserver hold a server object
- set up the event menu
- collect all data here instead of in the server class (hold game here, not in gameserver)

"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop()
    asyncio.set_event_loop(loop)
    window = QTServer(3)
    window.show()
    with loop:
        loop.run_forever()
