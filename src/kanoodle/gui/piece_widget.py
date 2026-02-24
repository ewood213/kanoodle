from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QMenu
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
import kanoodle.game.pieces as pieces

class ColorCell(QLabel):
    def __init__(self, fill_color=None, border_color=None, size=50, transparent=False):
        super().__init__()
        self.setFixedSize(size, size)  # Force square size
        self.transparent = transparent
        if not transparent:
            self.set_color(fill_color, border_color)
        else:
            self.set_transparent()

    def set_color(self, fill_color, border_color, border_thickness=2):
        self.setStyleSheet(f'''
                background-color: {fill_color};
                border: {border_thickness}px solid {border_color};
            ''')

    def set_transparent(self):
        self.setStyleSheet('background-color: transparent')


class PieceWidget(QWidget):
    place_piece_signal = pyqtSignal(int)
    remove_piece_signal = pyqtSignal(int)

    def __init__(self, piece: pieces.Piece, color: str, idx: int, square_size=50):
        super().__init__()
        self.piece = piece
        self.color = color
        self.square_size = square_size
        self.idx = idx
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
        policy = self.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(policy)

         # Set the widget size based on number of rows and columns
        rows, cols = self.piece.layout.shape
        most = max(rows, cols)
        self.setFixedSize(most * square_size, most * square_size)  # cols -> width, rows -> height
        self.original_pos = None
        self.placed = False

    def contextMenuEvent(self, a0):
        if not self.placed and not self.global_position_in_transparent(a0.globalPos()):
            self.context_menu.exec(a0.globalPos())

    def showEvent(self, event):
        super().showEvent(event)
        if self.original_pos is None:
            self.original_pos = self.pos()

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

    def global_position_in_transparent(self, global_position):
        for i in range(self.layout().count()):
            cell = self.layout().itemAt(i).widget()
            local_position = cell.mapFromGlobal(global_position)
            if cell.rect().contains(local_position):
                return cell.transparent
        assert False

    def mousePressEvent(self, event):
        self.widget_start_pos = None
        self.mouse_move_pos = None
        if event.button() == Qt.MouseButton.LeftButton:
            self.raise_()
            self.widget_start_pos = self.pos()
            self.mouse_move_pos = event.globalPosition()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPosition()
            diff = (globalPos - self.mouse_move_pos).toPoint()
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)
            self.mouse_move_pos = globalPos
            if self.placed:
                self.remove_piece_signal.emit(self.idx)

    def mouseReleaseEvent(self, event):
        if self.widget_start_pos is not None:
            self.place_piece_signal.emit(self.idx)

    def rotate(self):
        self.piece = self.piece.rotate_piece(pieces.Rotation.Ninety)
        self.update_piece_layout()

    def mirror(self):
        self.piece = self.piece.rotate_piece(pieces.Rotation.ZeroMirroed)
        self.update_piece_layout()

    def return_to_original_location(self):
        self.move(self.original_pos)
