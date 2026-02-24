from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QMenu
from PyQt6.QtCore import Qt, pyqtSignal
import kanoodle.game.pieces as pieces
import kanoodle.game.board as board

class ColorCell(QLabel):
    def __init__(self, fill_color=None, border_color=None, size=30, transparent=False, piece_index=-1):
        super().__init__()
        self.setFixedSize(size, size)  # Force square size
        self.transparent = transparent
        self.piece_index = piece_index
        if not transparent:
            self.set_color(fill_color, border_color)

    def set_color(self, fill_color, border_color, border_thickness=2):
        self.setStyleSheet(f'''
                background-color: {fill_color};
                border: {border_thickness}px solid {border_color};
            ''')


class BoardWidget(QWidget):
    def __init__(self, rows, cols, color, square_size=30):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self.color = color

        self.piece_set_signal = pyqtSignal(bool, int)

        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0,0,0,0)
        self.add_items_to_grid(self.grid)
        self.setLayout(self.grid)
        self.setFixedSize(square_size * cols, square_size*rows)

    def add_items_to_grid(self, grid):
        for i in range(self.rows):
            for j in range(self.cols):
                    cell = ColorCell(self.color, "black", self.square_size)
                    grid.addWidget(cell, i, j)
        return grid
