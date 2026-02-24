from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt6.QtCore import Qt
from kanoodle.gui.piece_widget import PieceWidget
from kanoodle.gui.board_widget import BoardWidget
from kanoodle.game.pieces import Piece
import numpy as np

_p1 = Piece(np.array([[1, 1], [0, 1]]))
_p2 = Piece(np.array([[1, 0, 0], [1, 0, 0], [1, 1, 1]]))
_p3 = Piece(np.array([[1, 1, 1, 1]]))
_p4 = Piece(np.array([[0, 0, 1, 1], [1, 1, 1, 0]]))
_p5 = Piece(np.array([[1, 1, 1, 1], [1, 0, 0, 0]]))
_p6 = Piece(np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]))
_p7 = Piece(np.array([[1, 1], [1, 1]]))
_p8 = Piece(np.array([[0, 1, 0, 0], [1, 1, 1, 1]]))
_p9 = Piece(np.array([[1, 1, 0], [0, 1, 1], [0, 0, 1]]))
_p10 = Piece(np.array([[1, 0, 1], [1, 1, 1]]))
_p11 = Piece(np.array([[1, 1, 1], [0, 1, 1]]))
_p12 = Piece(np.array([[0, 1], [0, 1], [1, 1]]))

KANOODLE_PIECES = [_p1, _p2, _p3, _p4, _p5, _p6, _p7, _p8, _p9, _p10, _p11, _p12]
KANOODLE_COLORS = ['#D3CCCA', '#76C3D2', '#7943B7', '#01A74C', '#0243B5', '#B2BBCA',
                   '#61EB5D', '#F2C4C5', '#EF4BA2', '#F6D400', '#D81511', '#FD7A07' ]

class GameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setStyleSheet("background-color: gray")
        layout = QVBoxLayout()

        self.board = BoardWidget(5, 11, "dimgray", 50)
        board_layout = QVBoxLayout()
        board_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        board_layout.addWidget(self.board)
        layout.addLayout(board_layout)
        self.piece_widgets = [PieceWidget(piece, color, i) for i, (piece, color) in enumerate(zip(KANOODLE_PIECES, KANOODLE_COLORS))]
        self.position_piece_rows()
        for w in self.piece_widgets:
            w.setParent(self)
            w.show()
            w.place_piece_signal.connect(self.try_place_piece)
            w.remove_piece_signal.connect(self.remove_piece)
            w.clicked_signal.connect(self.handle_piece_click)
        self.setLayout(layout)

    def resizeEvent(self, event):
        self.position_piece_rows()
        super().resizeEvent(event)

    def position_piece_rows(self):
        padding = 10
        first_row_start = int(self.height() * .5)
        first_row = self.piece_widgets[:len(self.piece_widgets) // 2]
        second_row = self.piece_widgets[len(self.piece_widgets) // 2:]
        self.position_piece_row(first_row_start, first_row, padding)
        second_row_start = first_row_start + max((w.height() + padding for w in first_row))
        self.position_piece_row(second_row_start, second_row, padding)

    def position_piece_row(self, row_start, piece_widgets, padding=10):
        parent_width = self.width()
        n = len(piece_widgets)
        total_piece_width = sum(w.sizeHint().width() for w in piece_widgets)

        # Compute spacing between pieces
        available_space = parent_width - total_piece_width - 2 * padding
        spacing = available_space // (n - 1)

        # Position each piece
        x = padding
        for w in piece_widgets:
            w.move(x, row_start)
            w.original_pos = w.pos()
            x += w.sizeHint().width() + spacing

    def try_place_piece(self, piece_index):
        assert piece_index != -1
        piece_widget = self.piece_widgets[piece_index]
        if self.board.can_place_piece(piece_widget):
            self.board.place_piece(piece_widget)
            piece_widget.placed = True
        else:
            piece_widget.return_to_original_location()

    def remove_piece(self, piece_index):
        assert piece_index != -1
        piece_widget = self.piece_widgets[piece_index]
        self.board.remove_piece(piece_widget)
        piece_widget.placed = False

    def handle_piece_click(self, event):
        for w in self.piece_widgets:
            if w.global_position_within_bounds(event.globalPosition().toPoint()):
                QApplication.sendEvent(w, event)