import GameServer


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

"""
Purpose of this class:
Create a server from the gameserver class and give it a qt interface

"""

class eventWindow(QWidget):
    def __init__(self, players : dict):
        super().__init__()

        self.layout : QGridLayout = QGridLayout()
        self.setLayout(self.layout)

        self.to_col = 1
        self.from_col = 0
        self.watcher_col = 2

        self.cur_row = 0
        """
        What I want is to get all the players and their ID's
        Then make the events based on their IDS
        
        """
        for i in range(self.from_col, self.watcher_col):
            label = QLabel({0:"From", 1:"To", 2:"Watcher"}[i])
            self.layout.addWidget(label, self.cur_row, i)
        self.cur_row += 1
        for ID in players:
            """Create a row for the player. Watcher, to and from"""
    
    def create_row(self, ID : int):
        for i in []

class QTServer(QWidget):

    def __init__(self, num_players : int = 1, url : str = "localhost", port : int = 8765):
        super().__init__()

        self.server = GameServer.Server(num_players, url, port)
        asyncio.run(self.server.main())

        


    def create_event(self):
        print("attempting to create event window")
        new_window = QWidget()


"""
TODO:
- Make the qtserver hold a server object
- set up the event menu
- collect all data here instead of in the server class (hold game here, not in gameserver)

"""
