from PyQt6.QtWidgets import QWidget, QMenu, QApplication
import sys

class MyWindow(QWidget):
    def __init__(self,):
        super().__init__()

        self.context = QMenu(self)
        action1 = self.context.addAction("Action 1")
        action2 = self.context.addAction("Action 2")


        self.show()

    
    def contextMenuEvent(self,event):
        self.context.exec(event.globalPos())


app = QApplication(sys.argv)
window = MyWindow()
sys.exit(app.exec())


