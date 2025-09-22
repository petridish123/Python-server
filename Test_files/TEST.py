from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

app = QApplication([])

window = QWidget()
layout = QVBoxLayout(window)

btn = QPushButton("Delete me")
layout.addWidget(btn)

def delete_button():
    layout.removeWidget(btn)
    btn.hide()
    btn.deleteLater()

btn.clicked.connect(delete_button)

window.show()
app.exec()
