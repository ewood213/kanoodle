import numpy as np
from kanoodle.game.pieces import Piece

class Board:
    def __init__(self, rows: int, cols: int):
        self.cells = np.zeros((rows, cols), dtype=np.uint8)

    @classmethod
    def from_layout(cls, layout):
        ret = cls(1, 1)
        ret.cells = layout
        return ret

    def place_piece(self, row: int, col: int, piece: Piece):
        assert self.can_place_piece(row, col, piece)
        filled_cells = np.argwhere(piece.layout)
        board_locations = filled_cells + np.array([row, col])
        self.cells[board_locations[:, 0], board_locations[:, 1]] = 1

    def can_place_piece(self, row: int, col: int, piece: Piece) -> bool:
        filled_cells = np.argwhere(piece.layout)
        board_locations = filled_cells + np.array([row, col])
        rows_in_bounds = np.all(board_locations[:, 0] < self.cells.shape[0])
        cols_in_bounds = np.all(board_locations[:, 1] < self.cells.shape[1])
        if not rows_in_bounds or not cols_in_bounds:
            return False

        cells_empty = np.all(self.cells[board_locations[:, 0], board_locations[:, 1]] == 0)

        return cells_empty

    def __repr__(self):
        return f"cells: {self.cells}"
