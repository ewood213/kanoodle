from PyQt6.QtWidgets import QApplication
from kanoodle.gui.game_widget import GameWidget
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = GameWidget()
    window.show()
    window.setFixedSize(1080, 750)

    app.exec()