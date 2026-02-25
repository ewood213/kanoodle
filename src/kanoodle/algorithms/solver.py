import kanoodle.game.board as board
import kanoodle.game.pieces as pieces
import kanoodle.algorithms.algorithm_x as algx
import kanoodle.algorithms.dancing_links as dl
from typing import List
import numpy as np
import copy

class PiecePlacement:
    def __init__(self, row, col, layout):
        self.row = row
        self.col = col
        self.layout = layout

    def __repr__(self):
        return f"Piece Placement: location: ({self.row}, {self.col}) layout: {self.layout}"

class Solver:
    def __init__(self, board: board.Board, pieces: List[pieces.Piece]):
        self.board = board
        self.pieces = pieces
        num_zeros = np.count_nonzero(self.board.cells == 0)
        num_filled_by_pieces = sum([np.count_nonzero(p.layout) for p in pieces])
        assert num_zeros == num_filled_by_pieces

    def create_incidence_matrix(self) -> np.ndarray:
        incidence_matrix = []
        rows = self.board.cells.shape[0]
        cols = self.board.cells.shape[1]

        # Our columns denote which piece, and which cell (i, j) the piece occupies
        row_len = rows * cols + len(self.pieces)
        for i, piece in enumerate(self.pieces):
            for p in piece.get_all_rotations():
                for r in range(rows):
                    for c in range(cols):
                        if self.board.can_place_piece(r, c, p):
                            row = np.zeros(row_len, dtype=np.uint8)
                            row[i] = 1
                            places_filled = np.argwhere(p.layout) + np.array([r, c])
                            for place in places_filled:
                                row_loc = len(self.pieces) + place[0] * cols + place[1]
                                row[row_loc] = 1
                            incidence_matrix.append(row)

        # Add a row that includes all spots used without a piece (must be in solution)
        already_filled = np.argwhere(self.board.cells)
        already_filled_row = np.zeros(row_len, dtype=np.uint8)
        for c in already_filled:
            row_loc = len(self.pieces) + c[0] * cols + c[1]
            already_filled_row[row_loc] = 1
        incidence_matrix.append(already_filled_row)

        return np.array(incidence_matrix, dtype=np.uint8)

    def valid_placement(self, row, column, piece):
        if not self.board.can_place_piece(row, column, piece):
            return False
        placed_board = copy.deepcopy(self.board)
        placed_board.place_piece(row, column, piece)
        return not self.contains_small_holes(placed_board)

    def contains_small_holes(self, board):
        unfilled_cells = np.argwhere(board.cells==0)
        min_hole_size_allowed = min((np.count_nonzero(p.layout) for p in self.pieces))
        found = set()
        for cell in unfilled_cells:
            if tuple(cell) in found:
                return
            stack = [cell]
            found.add(tuple)
            count = 1
            while stack:
                cur = stack.pop()
                for dir in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                    next_loc = np.array([cur[0].astype(int) + dir[0], cur[1].astype(int) + dir[1]])
                    gt_zero = np.all(next_loc >= 0)
                    row_in_bounds = next_loc[0] < board.cells.shape[0]
                    col_in_bounds = next_loc[1] < board.cells.shape[1]
                    if gt_zero and row_in_bounds and col_in_bounds and board.cells[next_loc[0], next_loc[1]] == 0 and not tuple(next_loc) in found:
                        stack.append(next_loc)
                        found.add(tuple(next_loc))
                        count += 1
            if count < min_hole_size_allowed:
                return True
        return False

    def convert_solution_to_piece_placement(self, solution_rows):
        rows = self.board.cells.shape[0]
        cols = self.board.cells.shape[1]

        # Account for the row that is the partially filled board
        if np.any(self.board.cells == 1):
            expected_solution_rows = len(self.pieces) + 1
        else:
            expected_solution_rows = len(self.pieces)


        # Remove the row that contains already filled locations
        pieces_only = np.array([r for r in solution_rows if np.count_nonzero(r[:len(self.pieces)]) == 1])
        assert len(pieces_only) == len(self.pieces) and expected_solution_rows == len(solution_rows)
        ret = [None for _ in range(len(self.pieces))]

        # Construct and return piece placements from our solution
        for p in pieces_only:
            p_index = np.argwhere(p[:len(self.pieces)]).reshape(1)
            board_loc = p[len(self.pieces):].reshape(rows, cols)
            p_location = np.argwhere(board_loc)
            top_left_location = np.array([np.min(p_location[:, 0]), np.min(p_location[:, 1])])
            bottom_right_location = np.array([np.max(p_location[:, 0]), np.max(p_location[:, 1])])
            layout = board_loc[top_left_location[0]:bottom_right_location[0]+1, top_left_location[1]:bottom_right_location[1]+1]
            ret[p_index[0]] = PiecePlacement(top_left_location[0], top_left_location[1], layout)
        return ret


    def solve_algx(self) -> List[PiecePlacement]:
        incidence_matrix = self.create_incidence_matrix()
        row_idxs_used = algx.exact_cover(self.create_incidence_matrix())
        if row_idxs_used is None:
            return None
        solution_rows = np.array([incidence_matrix[r] for r in row_idxs_used])
        return self.convert_solution_to_piece_placement(solution_rows)


    def solve_dancing_links(self) -> List[PiecePlacement]:
        incidence_matrix = self.create_incidence_matrix()
        solution_rows = dl.solve_using_dancing_links(incidence_matrix)
        if solution_rows is None:
            return None
        return self.convert_solution_to_piece_placement(solution_rows)
