from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QLineEdit, QVBoxLayout, QGridLayout
)
import sys
from PyQt6.QtCore import Qt

from PyQt6.QtGui import QIcon

import os
import game


class Window(QWidget):
    def __init__(self, x = 300, y = 300, name = "My Window", player_num = 3):
        super().__init__()
        self.cur_row = 0
        self.players = {}
        self.num_player = player_num
        abspath = "C:/Users/Mango/Desktop/Python_server_client/Python-server/"
        self.setWindowIcon(QIcon(abspath+ "Saturn.png"))
        self.setWindowTitle(name)

    

        self.layout = QGridLayout()
        if not x== 0 and not y == 0:
            self.resize(x,y)
        else:
            pass
        self.setLayout(self.layout)

        for player in range(self.num_player):
            self.add_player()

        # self.label1 = QLabel("Username: ")
        # self.layout.addWidget(self.label1, 0,0)

        # self.label1 = QLabel("Password: ")
        # self.layout.addWidget(self.label1, 1,0)

        # self.input1 = QLineEdit()
        # self.layout.addWidget(self.input1 ,0 , 1)

        # self.input2 = QLineEdit()
        # self.layout.addWidget(self.input2,1,1)

        self.button = QPushButton("Submit")
        self.button.setFixedWidth(50)
        self.button.clicked.connect(self.display)
        self.layout.addWidget(self.button,self.cur_row,1, Qt.AlignmentFlag.AlignRight)

    def display(self):
        print("moving on")
        for player in self.players:
            self.players[player].set_next_round()
    
    def add_player(self):
        
        label1 = QLabel("Player: " + str(self.cur_row))
        self.layout.addWidget(label1, self.cur_row, 0)

        new_label = QLabel("Points: " + str(0))
        self.layout.addWidget(new_label, self.cur_row, 6)
        
        new_player = game.player(new_label)
        self.players[self.cur_row] = new_player


        button = QPushButton("Very Negative")
        button.setFixedWidth(100)
        button.clicked.connect(new_player.set_score_from_player(self.cur_row, -2))
        self.layout.addWidget(button,self.cur_row,1)

        button = QPushButton("Negative")
        button.setFixedWidth(100)
        button.clicked.connect(new_player.set_score_from_player(self.cur_row,-1))
        self.layout.addWidget(button,self.cur_row,2)

        button = QPushButton("Neutral")
        button.setFixedWidth(100)
        button.clicked.connect(new_player.set_score_from_player(self.cur_row,0))
        self.layout.addWidget(button,self.cur_row,3)

        button = QPushButton("Positive")
        button.setFixedWidth(100)
        button.clicked.connect(new_player.set_score_from_player(self.cur_row,1))
        self.layout.addWidget(button,self.cur_row,4)

        button = QPushButton("Very Positive")
        button.setFixedWidth(100)
        button.clicked.connect(new_player.set_score_from_player(self.cur_row,2))
        self.layout.addWidget(button,self.cur_row,5)


        self.cur_row += 1
        # x5
        """
        add 5 buttons, and 2 labels
        name, buttons, points/reputation

        """

def main():
    app = QApplication(sys.argv)
    abspath = "C:/Users/Mango/Desktop/Python_server_client/Python-server/"
    set_style(app, abspath + "css_style_qwidget.css")
    window = Window(x = 0 ,y = 0 ,name = " ")
    window.show()
    sys.exit(app.exec())  

def set_style(app : QApplication, sheet : str):
    with open(sheet, "r") as f:
        if not f:
            return False
        lines = f.read()
        # print(lines) 
        
        app.setStyleSheet(lines)

if __name__ == "__main__":
    main()

