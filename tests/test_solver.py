import kanoodle.game.pieces as pieces
from kanoodle.game.board import Board
from kanoodle.algorithms.solver import Solver
import numpy as np

def test_4x4_puzzle_algx():
    fat_piece = pieces.Piece(np.array([[1, 1], [1, 1], [1, 0]]))
    squiggle_piece = pieces.Piece(np.array([[0, 1, 1], [1, 1, 0]]))
    square_piece = pieces.Piece(np.ones((2, 2)))
    bracket_piece = pieces.Piece(np.array([[0, 1], [1, 1]]))

    board = Board(4, 4)
    board.place_piece(0, 0, fat_piece)

    solver = Solver(board, [squiggle_piece, square_piece, bracket_piece])
    solution = solver.solve_algx()
    assert len(solution) == 3
    squiggle_solution, square_solution, bracket_solution = solution
    assert np.array_equal(squiggle_solution.layout, squiggle_piece.layout)
    assert (squiggle_solution.row, squiggle_solution.col) == (2, 0)
    assert np.array_equal(square_solution.layout, square_piece.layout)
    assert (square_solution.row, square_solution.col) == (0, 2)
    assert np.array_equal(bracket_solution.layout, bracket_piece.layout)
    assert (bracket_solution.row, bracket_solution.col) == (2, 2)

    for placement in solution:
        piece = pieces.Piece(placement.layout)
        board.place_piece(placement.row, placement.col, piece)
    assert np.count_nonzero(board.cells) == board.cells.size

def test_4x4_puzzle_dl():
    fat_piece = pieces.Piece(np.array([[1, 1], [1, 1], [1, 0]]))
    squiggle_piece = pieces.Piece(np.array([[0, 1, 1], [1, 1, 0]]))
    square_piece = pieces.Piece(np.ones((2, 2)))
    bracket_piece = pieces.Piece(np.array([[0, 1], [1, 1]]))

    board = Board(4, 4)
    board.place_piece(0, 0, fat_piece)

    solver = Solver(board, [squiggle_piece, square_piece, bracket_piece])
    solution = solver.solve_dancing_links()
    assert len(solution) == 3
    squiggle_solution, square_solution, bracket_solution = solution
    assert np.array_equal(squiggle_solution.layout, squiggle_piece.layout)
    assert (squiggle_solution.row, squiggle_solution.col) == (2, 0)
    assert np.array_equal(square_solution.layout, square_piece.layout)
    assert (square_solution.row, square_solution.col) == (0, 2)
    assert np.array_equal(bracket_solution.layout, bracket_piece.layout)
    assert (bracket_solution.row, bracket_solution.col) == (2, 2)

    for placement in solution:
        piece = pieces.Piece(placement.layout)
        board.place_piece(placement.row, placement.col, piece)
    assert np.count_nonzero(board.cells) == board.cells.size

def test_kanoodle_puzzle_algx():
    p1 = pieces.Piece(np.array([[1, 1], [0, 1]]))
    p2 = pieces.Piece(np.array([[1, 0, 0], [1, 0, 0], [1, 1, 1]]))
    p3 = pieces.Piece(np.array([[1, 1, 1, 1]]))
    p4 = pieces.Piece(np.array([[1, 1, 1, 1], [1, 0, 0, 0]]))
    p5 = pieces.Piece(np.array([[0, 0, 1, 1], [1, 1, 1, 0]]))
    p6 = pieces.Piece(np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]))
    p7 = pieces.Piece(np.array([[1, 1], [1, 1]]))
    p8 = pieces.Piece(np.array([[0, 1, 0, 0], [1, 1, 1, 1]]))
    p9 = pieces.Piece(np.array([[1, 1, 0], [0, 1, 1], [0, 0, 1]]))
    p10 = pieces.Piece(np.array([[1, 0, 1], [1, 1, 1]]))
    p11 = pieces.Piece(np.array([[1, 1, 1], [0, 1, 1]]))
    p12 = pieces.Piece(np.array([[0, 1], [0, 1], [1, 1]]))

    board = Board(5, 11)
    board.place_piece(0, 0, p1)
    board.place_piece(1, 0, p2)
    board.place_piece(4, 0, p3)
    board.place_piece(0, 2, p4)
    solver = Solver(board, [p5, p6, p7, p8, p9, p10, p11, p12])
    solution = solver.solve_dancing_links()

    for placement in solution:
        piece = pieces.Piece(placement.layout)
        board.place_piece(placement.row, placement.col, piece)
    assert np.count_nonzero(board.cells) == board.cells.size

def test_kanoodle_puzzle_dl():
    p1 = pieces.Piece(np.array([[1, 1], [0, 1]]))
    p2 = pieces.Piece(np.array([[1, 0, 0], [1, 0, 0], [1, 1, 1]]))
    p3 = pieces.Piece(np.array([[1, 1, 1, 1]]))
    p4 = pieces.Piece(np.array([[1, 1, 1, 1], [1, 0, 0, 0]]))
    p5 = pieces.Piece(np.array([[0, 0, 1, 1], [1, 1, 1, 0]]))
    p6 = pieces.Piece(np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]))
    p7 = pieces.Piece(np.array([[1, 1], [1, 1]]))
    p8 = pieces.Piece(np.array([[0, 1, 0, 0], [1, 1, 1, 1]]))
    p9 = pieces.Piece(np.array([[1, 1, 0], [0, 1, 1], [0, 0, 1]]))
    p10 = pieces.Piece(np.array([[1, 0, 1], [1, 1, 1]]))
    p11 = pieces.Piece(np.array([[1, 1, 1], [0, 1, 1]]))
    p12 = pieces.Piece(np.array([[0, 1], [0, 1], [1, 1]]))

    board = Board(5, 11)
    board.place_piece(0, 0, p1)
    board.place_piece(1, 0, p2)
    board.place_piece(4, 0, p3)
    board.place_piece(0, 2, p4)
    solver = Solver(board, [p5, p6, p7, p8, p9, p10, p11, p12])
    solution = solver.solve_dancing_links()

    for placement in solution:
        piece = pieces.Piece(placement.layout)
        board.place_piece(placement.row, placement.col, piece)
    assert np.count_nonzero(board.cells) == board.cells.size

def test_no_solution_puzzle_algx():
    fat_piece = pieces.Piece(np.array([[1, 1], [1, 1], [1, 0]]))
    squiggle_piece = pieces.Piece(np.array([[0, 1, 1], [1, 1, 0]]))
    square_piece = pieces.Piece(np.ones((2, 2)))
    bracket_piece = pieces.Piece(np.array([[0, 1], [1, 1]]))

    board = Board(4, 4)
    board.place_piece(0, 0, fat_piece.rotate_piece(pieces.Rotation.OneEighty))

    solver = Solver(board, [squiggle_piece, square_piece, bracket_piece])
    solution = solver.solve_algx()
    assert solution is None

def test_no_solution_puzzle_dl():
    fat_piece = pieces.Piece(np.array([[1, 1], [1, 1], [1, 0]]))
    squiggle_piece = pieces.Piece(np.array([[0, 1, 1], [1, 1, 0]]))
    square_piece = pieces.Piece(np.ones((2, 2)))
    bracket_piece = pieces.Piece(np.array([[0, 1], [1, 1]]))

    board = Board(4, 4)
    board.place_piece(0, 0, fat_piece.rotate_piece(pieces.Rotation.OneEighty))

    solver = Solver(board, [squiggle_piece, square_piece, bracket_piece])
    solution = solver.solve_dancing_links()
    assert solution is None