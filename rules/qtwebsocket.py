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

url = "127.0.0.1"
PORT = 8765


class QtWebsocket(QWidget):





    def __init__(self,):
        super().__init__()

        self.setWindowTitle("Client")

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.send_message) # connect to a function
        self.layout.addWidget(self.button,0,0)
        
        self.run()

    @asyncSlot()    
    async def send_message(self, message = "Hello!"):
        new_message = {
            "MESSAGE":message
        }
        new_message = json.dumps(new_message).encode()
        await self.socket.send(new_message)

    @asyncSlot()
    async def send_allocation(self, allocation : int):
        new_message = {
            "ALLOCATION" : allocation,
            "ID" : 0,
        }
        new_message = json.dumps(new_message).encode()
        await self.socket.send(new_message)

    @asyncSlot()
    async def run(self):
        self.socket = await websockets.connect("ws://localhost:8765")
        await self.socket.send(json.dumps({"REQUEST" : "CONNECT"}).encode())
        message = await self.socket.recv()
        print(message)
        while True:
            try:
                message = await self.socket.recv()
                print(message)
            except KeyboardInterrupt:
                print("AWW")

def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = QtWebsocket()
    window.show()
    # sys.exit(app.exec())
    with loop:
        loop.run_forever()

        

if __name__ == "__main__":
    main()

