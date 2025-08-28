from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QLineEdit, QVBoxLayout, QGridLayout
)
import sys
from PyQt6.QtCore import Qt

from PyQt6.QtGui import QIcon

import os

class pointLabel(QLabel):

    def __init__(self, text = ""):
        super().__init__(text)
    
    def set_points(self, points:int):
        self.text = str(points)


class Window(QWidget):
    def __init__(self, x = 300, y = 300, name = "My Window"):
        super().__init__()

        abspath = "C:/Users/Mango/Desktop/Python_server_client/Python-server/"
        self.setWindowIcon(QIcon(abspath+ "Saturn.png"))
        self.setWindowTitle(name)

    

        self.layout = QGridLayout()
        if not x== 0 and not y == 0:
            self.resize(x,y)
        else:
            pass
        self.setLayout(self.layout)

        

        self.label1 = QLabel("Username: ")
        self.layout.addWidget(self.label1, 0,0)

        self.label1 = QLabel("Password: ")
        self.layout.addWidget(self.label1, 1,0)

        self.input1 = QLineEdit()
        self.layout.addWidget(self.input1 ,0 , 1)

        self.input2 = QLineEdit()
        self.layout.addWidget(self.input2,1,1)

        self.button = QPushButton("Submit")
        self.button.setFixedWidth(50)
        self.button.clicked.connect(self.display)
        self.layout.addWidget(self.button,2,1, Qt.AlignmentFlag.AlignRight)

    def display(self):
        print(self.input1.text())
        print(self.input2.text())
        sys.exit()
    
    def add_player(self):
        pass
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
        print(lines) 
        
        app.setStyleSheet(lines)

if __name__ == "__main__":
    main()

