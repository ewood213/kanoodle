from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
import kanoodle.game.pieces as pieces

class ColorCell(QLabel):
    def __init__(self, fill_color=None, border_color=None, size=30, transparent=False):
        super().__init__()
        self.setFixedSize(size, size)  # Force square size
        self.transparent = transparent
        if not transparent:
            self.set_color(fill_color, border_color)

    def set_color(self, fill_color, border_color, border_thickness=2):
        self.setStyleSheet(f'''
                background-color: {fill_color};
                border: {border_thickness}px solid {border_color};
            ''')


class PieceWidget(QWidget):
    def __init__(self, piece: pieces.Piece, color: str, square_size=30):
        super().__init__()
        self.piece = piece
        self.color = color
        self.square_size = square_size
        self.selected = False
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0,0,0,0)
        self.fill_grid()
        self.setLayout(self.grid)

        # Set the widget size based on number of rows and columns
        rows, cols = self.piece.layout.shape
        self.setFixedSize(cols * square_size, rows * square_size)  # cols -> width, rows -> height

    def fill_grid(self):
        rows, cols = self.piece.layout.shape
        for i in range(rows):
            for j in range(cols):
                if self.piece.layout[i][j] == 1:
                    cell = ColorCell(self.color, "black", size=self.square_size)
                else:
                    cell = ColorCell(size=self.square_size, transparent=True)
                self.grid.addWidget(cell, i, j)

    def mousePressEvent(self, a0):
        pos = a0.position().toPoint()
        self.set_all_siblings_as_unselected()
        if self.childAt(pos).transparent:
            self.set_unselected()
            return
        self.set_selected()

    def set_all_siblings_as_unselected(self):
        for sibling in self.parent().findChildren(PieceWidget):
            if sibling is not self:
                sibling.set_unselected()

    def set_selected(self):
        self.selected = True
        for i in range(self.grid.count()):
            cell = self.grid.itemAt(i).widget()
            if not cell.transparent:
                cell.set_color(self.color, "white", border_thickness=3)

    def set_unselected(self):
        self.selected = False
        for i in range(self.grid.count()):
            cell = self.grid.itemAt(i).widget()
            if not cell.transparent:
                cell.set_color(self.color, "black")
