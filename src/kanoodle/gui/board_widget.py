from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QMenu
from PyQt6.QtCore import pyqtSignal
import kanoodle.gui.piece_widget as pieces
import numpy as np

class ColorCell(QLabel):
    def __init__(self, fill_color=None, border_color='black', size=30, piece_index=-1):
        super().__init__()
        self.setFixedSize(size, size)
        self.piece_index = piece_index
        self.fill_color = fill_color
        self.border_color = border_color
        self.set_style()

    def set_color(self, fill_color, border_color):
        self.fill_color = fill_color
        self.border_color = border_color
        self.set_style()

    def set_style(self):
        self.setStyleSheet(f'''
                background-color: {self.fill_color};
                border: 2px solid {self.border_color};
            ''')

    def set_piece(self, piece_widget):
        self.piece_index = piece_widget.idx

    def remove_piece(self):
        self.piece_index = -1

    def has_piece(self):
        return self.piece_index != -1


class BoardWidget(QWidget):
    def __init__(self, rows, cols, color, square_size=30, piece_placed_sound=None):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self.color = color
        self.piece_placed_sound = piece_placed_sound

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

    def find_cell_that_contains_point(self, global_center):
        for i in range(self.layout().count()):
            cell_widget = self.layout().itemAt(i).widget()
            widget_center_in_cell = cell_widget.mapFromGlobal(global_center)
            if cell_widget.rect().contains(widget_center_in_cell):
                    return cell_widget
        return None

    def can_place_piece(self, piece_widget: pieces.PieceWidget):
        for i in range(piece_widget.layout().count()):
            widget = piece_widget.layout().itemAt(i).widget()
            if widget.transparent:
                continue
            global_center = widget.mapToGlobal(widget.rect().center())
            containing_cell = self.find_cell_that_contains_point(global_center)
            if containing_cell is None or containing_cell.has_piece():
                 return False
        return True

    def place_piece(self, piece_widget: pieces.PieceWidget):
        assert self.can_place_piece(piece_widget)
        for i in range(piece_widget.layout().count()):
            widget = piece_widget.layout().itemAt(i).widget()
            if widget.transparent:
                continue
            global_center = widget.mapToGlobal(widget.rect().center())
            containing_cell = self.find_cell_that_contains_point(global_center)
            containing_cell.set_piece(piece_widget)
            cell_center_global = containing_cell.mapToGlobal(
                containing_cell.rect().center()
            )
            offset_global = cell_center_global - global_center
        top_left_global = piece_widget.mapToGlobal(piece_widget.rect().topLeft()) + offset_global
        piece_widget.move(piece_widget.parentWidget().mapFromGlobal(top_left_global))
        piece_widget.placed = True
        if self.piece_placed_sound is not None:
            self.piece_placed_sound.play()

    def remove_piece(self, piece_widget):
        removed = False
        assert piece_widget.placed
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if widget.piece_index == piece_widget.idx:
                widget.remove_piece()
                removed = True
        piece_widget.placed = False
        assert removed

    def get_occupancy_grid(self):
        layout = np.zeros((self.rows, self.cols))
        for i in range(self.rows):
            for j in range(self.cols):
                pos = i * self.cols + j
                cell = self.grid.itemAt(pos).widget()
                if cell.has_piece():
                    layout[i][j] = 1
        return layout

    def get_cell_at_idx(self, row, col):
        assert 0 <= row < self.rows and 0 <= col < self.cols
        return self.grid.itemAt(row * self.cols + col).widget()

