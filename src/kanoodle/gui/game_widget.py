from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QUrl
from PyQt6.QtGui import QPixmap
from kanoodle.gui.piece_widget import PieceWidget
from kanoodle.gui.board_widget import BoardWidget
from kanoodle.game.pieces import Piece
from kanoodle.game.board import Board as SolverBoard
from kanoodle.algorithms.solver import Solver
import numpy as np
import time
import os
from PyQt6.QtMultimedia import QSoundEffect

_p0 = Piece(np.array([[1, 1], [0, 1]]))
_p1 = Piece(np.array([[1, 0, 0], [1, 0, 0], [1, 1, 1]]))
_p2 = Piece(np.array([[1, 1, 1, 1]]))
_p3 = Piece(np.array([[0, 0, 1, 1], [1, 1, 1, 0]]))
_p4 = Piece(np.array([[1, 1, 1, 1], [1, 0, 0, 0]]))
_p5 = Piece(np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]))
_p6 = Piece(np.array([[1, 1], [1, 1]]))
_p7 = Piece(np.array([[0, 1, 0, 0], [1, 1, 1, 1]]))
_p8 = Piece(np.array([[1, 1, 0], [0, 1, 1], [0, 0, 1]]))
_p9 =  Piece(np.array([[1, 0, 1], [1, 1, 1]]))
_p10 = Piece(np.array([[1, 1, 1], [0, 1, 1]]))
_p11 = Piece(np.array([[0, 1], [0, 1], [1, 1]]))

KANOODLE_PIECES = [_p0, _p1, _p2, _p3, _p4, _p5, _p6, _p7, _p8, _p9, _p10, _p11]
KANOODLE_COLORS = ['#D3CCCA', '#76C3D2', '#7943B7', '#01A74C', '#0243B5', '#B2BBCA',
                   '#61EB5D', '#F2C4C5', '#EF4BA2', '#F6D400', '#D81511', '#FD7A07' ]

class SolverThread(QThread):
    finished = pyqtSignal(object, float)

    def __init__(self, board_layout, pieces, indexes):
        super().__init__()
        board = SolverBoard.from_layout(board_layout)
        self.indexes = indexes
        self.solver = Solver(board, pieces)

    def run(self):
        start = time.perf_counter()
        piece_placements = self.solver.solve_dancing_links()
        time_for_algorithm = time.perf_counter() - start
        if piece_placements is None:
            self.finished.emit(None, 0)
        else:
            ret = list(zip(self.indexes, piece_placements))
            self.finished.emit(ret, time_for_algorithm)


class GameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kanoodle!")
        self.setStyleSheet("background-color: gray")
        self.solver_thread = None
        assets_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + "/assets"

        # Create sounds
        piece_placed_sound_path = QUrl.fromLocalFile(assets_directory + "/piece_placed_sound.wav")
        piece_placed_sound = QSoundEffect()
        piece_placed_sound.setSource(piece_placed_sound_path)

        reset_pieces_sound_path = QUrl.fromLocalFile(assets_directory + "/reset_pieces_sound.wav")
        self.reset_pieces_sound = QSoundEffect()
        self.reset_pieces_sound.setSource(reset_pieces_sound_path)
        self.reset_pieces_sound.setVolume(.05)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        kanoodle_title = QLabel()
        kanoodle_image = QPixmap(assets_directory + "/kanoodle_wordart_cropped.png").scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        kanoodle_title.setPixmap(kanoodle_image)
        kanoodle_title.setContentsMargins(0,0,0,0)  # remove label internal padding
        layout.addWidget(kanoodle_title, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        board_row_layout = QHBoxLayout()
        board_row_layout.setSpacing(0)
        board_row_layout.setContentsMargins(0, 0, 0, 0)
        board_row_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        board_row_layout.addStretch(1)


        self.board = BoardWidget(5, 11, "dimgray", 50, piece_placed_sound)
        board_row_layout.addWidget(self.board)
        board_row_layout.addStretch(1)

        # Add solve button on the right
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.solve_button = QPushButton("Solve")
        self.solve_button.clicked.connect(self.begin_solving_puzzle)
        self.solve_button.setStyleSheet('''
                                        background-color: #01A74C;
                                        color: black;
                                        ''')
        button_layout.addWidget(self.solve_button, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)


        self.reset_button = QPushButton("Reset Pieces")
        self.reset_button.clicked.connect(self.remove_all_pieces)
        button_layout.addWidget(self.reset_button, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.reset_button.setStyleSheet('''
                                        background-color: dimgray;
                                        color: black;
                                        ''')
        self.status_text = QLabel()
        self.status_text.setMaximumHeight(self.status_text.sizeHint().height())
        button_layout.addWidget(self.status_text)
        button_layout.addStretch()
        board_row_layout.addLayout(button_layout)
        layout.addLayout(board_row_layout)
        layout.addStretch(1)

        # Place pieces globally in two rows on the bottom
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
        first_row_start = self.board.y() + self.board.size().height() + 20
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
            if not w.placed:
                w.move(x, row_start)
                w.original_pos = w.pos()
                x += w.sizeHint().width() + spacing

    def try_place_piece(self, piece_index):
        assert piece_index != -1
        piece_widget = self.piece_widgets[piece_index]
        if self.board.can_place_piece(piece_widget):
            self.board.place_piece(piece_widget)
        else:
            piece_widget.return_to_original_location()

    def remove_piece(self, piece_index):
        assert piece_index != -1
        piece_widget = self.piece_widgets[piece_index]
        self.board.remove_piece(piece_widget)

    def handle_piece_click(self, event):
        for w in self.piece_widgets:
            if w.global_position_within_bounds(event.globalPosition().toPoint()):
                QApplication.sendEvent(w, event)

    def begin_solving_puzzle(self):
        board_layout = self.board.get_occupancy_grid()
        pieces_and_indices = list(zip(*[(w.piece, i) for i, w in enumerate(self.piece_widgets) if not w.placed]))
        if len(pieces_and_indices) == 0:
            print("Attempted to solve with no pieces available")
            return
        pieces, piece_indices = pieces_and_indices
        for piece in self.piece_widgets:
            piece.can_move = False
        self.solve_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.solver_thread = SolverThread(board_layout, pieces, piece_indices)
        self.solver_thread.finished.connect(self.on_solving_done)
        self.solver_thread.start()

    def on_solving_done(self, result, time_for_algorithm):
        if result is None:
            self.status_text.setText("No solution")
            self.finish_placing_pieces()
            return

        self.status_text.setText(f"Solved in {time_for_algorithm:.2f}s")
        time_between_placements = 500
        for i, (idx, placement) in enumerate(result):
            place_piece_func = lambda idx=idx, placement=placement: self.place_piece_on_board(idx, placement.row, placement.col, placement.layout)
            QTimer.singleShot(i * time_between_placements, place_piece_func)
        QTimer.singleShot(i * time_between_placements, self.finish_placing_pieces)

    def place_piece_on_board(self, idx, row, col, layout):
        piece_widget = self.piece_widgets[idx]
        piece_widget.piece = Piece(layout)
        piece_widget.update_piece_layout()
        top_left_cell = self.board.get_cell_at_idx(row, col)
        cell_global_pos = top_left_cell.mapToGlobal(top_left_cell.rect().topLeft())
        piece_widget.raise_()
        piece_widget.move(piece_widget.parent().mapFromGlobal(cell_global_pos))
        QApplication.processEvents()
        self.board.place_piece(piece_widget)

    def finish_placing_pieces(self):
        for piece in self.piece_widgets:
            piece.can_move = True
        self.solve_button.setEnabled(True)
        self.reset_button.setEnabled(True)

    def remove_all_pieces(self):
        if not any((w.placed for w in self.piece_widgets)):
            return
        self.reset_pieces_sound.play()
        for i in range(len(self.piece_widgets)):
            if self.piece_widgets[i].placed:
                self.remove_piece(i)
                self.piece_widgets[i].return_to_original_location()
