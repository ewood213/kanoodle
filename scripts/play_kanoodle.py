from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget
from PyQt6.QtCore import QObject, QEvent
from kanoodle.gui.game_widget import GameWidget
import numpy as np
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = GameWidget()
    window.show()
    window.setMinimumSize(1080, 720)

    app.exec()