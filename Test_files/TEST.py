from PyQt6.QtWidgets import QWidget, QMenu, QApplication
import sys
import asyncio
class MyWindow(QWidget):
    def __init__(self,):
        super().__init__()

        self.context = QMenu(self)
        action1 = self.context.addAction("Action 1")
        action2 = self.context.addAction("Action 2")


        self.show()

    
    def contextMenuEvent(self,event):
        self.context.exec(event.globalPos())


# app = QApplication(sys.argv)
# window = MyWindow()
# sys.exit(app.exec())




async def func(*args, **kwargs):
    print("yes" in kwargs)
    print(kwargs)
    print(args)

# func(no = 12, yes = 13)
asyncio.run(func(no = 1, yes = "13"))
