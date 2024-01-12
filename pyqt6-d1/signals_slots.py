# signals_slots.py

"""Signals and slots example."""

import sys

from functools import partial

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


def greet2(name):
    if msg.text():
        msg.setText("")
    else:
        msg.setText(f"Hello, {name}")


ready_greet2 = partial(greet2, "from George!")


def greet():
    if msgLabel.text():
        msgLabel.setText("")
    else:
        msgLabel.setText("Hello, World!")


app = QApplication([])
window = QWidget()
window.setWindowTitle("Signals and slots")

layout = QVBoxLayout()

button = QPushButton("Greet")

button.clicked.connect(greet)
button.clicked.connect(ready_greet2)

layout.addWidget(button)
msgLabel = QLabel("")
msg = QLabel("")
layout.addWidget(msgLabel)
layout.addWidget(msg)

window.setLayout(layout)

window.show()
sys.exit(app.exec())
