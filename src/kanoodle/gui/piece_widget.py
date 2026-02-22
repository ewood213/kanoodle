from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QMenu
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
        self.context_menu = QMenu()
        rotate_action = self.context_menu.addAction("rotate")
        mirror_action = self.context_menu.addAction("mirror")
        rotate_action.triggered.connect(self.rotate)
        mirror_action.triggered.connect(self.mirror)
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0,0,0,0)
        self.add_items_to_grid(self.grid)
        self.setLayout(self.grid)

         # Set the widget size based on number of rows and columns
        rows, cols = self.piece.layout.shape
        most = max(rows, cols)
        self.setFixedSize(most * square_size, most * square_size)  # cols -> width, rows -> height

    def contextMenuEvent(self, a0):
        self.context_menu.exec(a0.globalPos())

    def update_piece_layout(self):
        old_layout = self.layout()
        while old_layout.count():
            child = old_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.add_items_to_grid(self.grid)

    def add_items_to_grid(self, grid):
        rows, cols = self.piece.layout.shape
        most = max(rows, cols)
        for i in range(most):
            for j in range(most):
                if i >= rows or j >= cols or self.piece.layout[i][j] == 0:
                    cell = ColorCell(size=self.square_size, transparent=True)
                else:
                    cell = ColorCell(self.color, "black", size=self.square_size)
                grid.addWidget(cell, i, j)
        return grid

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

    def rotate(self):
        self.piece = self.piece.rotate_piece(pieces.Rotation.Ninety)
        self.update_piece_layout()

    def mirror(self):
        self.piece = self.piece.rotate_piece(pieces.Rotation.ZeroMirroed)
        self.update_piece_layout()
