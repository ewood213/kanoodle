from PyQt6.QtWidgets import QVBoxLayout, QWidget
from kanoodle.gui.piece_widget import PieceWidget
from kanoodle.game.pieces import Piece
import numpy as np

p1 = Piece(np.array([[1, 1], [0, 1]]))
p2 = Piece(np.array([[1, 0, 0], [1, 0, 0], [1, 1, 1]]))
p3 = Piece(np.array([[1, 1, 1, 1]]))
p4 = Piece(np.array([[0, 0, 1, 1], [1, 1, 1, 0]]))
p5 = Piece(np.array([[1, 1, 1, 1], [1, 0, 0, 0]]))
p6 = Piece(np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]))
p7 = Piece(np.array([[1, 1], [1, 1]]))
p8 = Piece(np.array([[0, 1, 0, 0], [1, 1, 1, 1]]))
p9 = Piece(np.array([[1, 1, 0], [0, 1, 1], [0, 0, 1]]))
p10 = Piece(np.array([[1, 0, 1], [1, 1, 1]]))
p11 = Piece(np.array([[1, 1, 1], [0, 1, 1]]))
p12 = Piece(np.array([[0, 1], [0, 1], [1, 1]]))

KANOODLE_PIECES = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]
KANOODLE_COLORS = ['#D3CCCA', '#76C3D2', '#7943B7', '#01A74C', '#0243B5', '#B2BBCA',
                   '#61EB5D', '#F2C4C5', '#EF4BA2', '#F6D400', '#D81511', '#FD7A07' ]

class GameWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setStyleSheet("background-color: darkgray")
        layout = QVBoxLayout()
        self.piece_widgets = [PieceWidget(piece, color) for piece, color in zip(KANOODLE_PIECES, KANOODLE_COLORS)]
        for widget in self.piece_widgets:
            layout.addWidget(widget)
        self.setLayout(layout)

    def mousePressEvent(self, a0):
        for widget in self.piece_widgets:
            widget.set_unselected()