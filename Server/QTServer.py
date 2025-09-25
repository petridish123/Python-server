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

class QTServer(QWidget):

    def __init__(self, num_players : int = 1, url : str = "localhost", port : int = 8765):
        super().__init__()

        self.server = GameServer.Server(num_players, url, port)
        asyncio.run(self.server.main())


"""
TODO:
- Make the qtserver hold a server object
- set up the event menu
- collect all data here instead of in the server class (hold game here, not in gameserver)

"""
