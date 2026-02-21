import numpy as np
from kanoodle.game.board import Board
from kanoodle.game.pieces import Piece, Rotation
import pytest

def test_can_place_bracket():
    piece = Piece(np.array([[1, 1], [1, 0]]))
    board = Board(2, 3)

    assert board.can_place_piece(0, 0, piece)
    assert board.can_place_piece(0, 1, piece)
    assert not board.can_place_piece(0, 2, piece)
    assert not board.can_place_piece(1, 0, piece)

def test_place_bracket():
    piece = Piece(np.array([[1, 1], [1, 0]]))
    board = Board(4, 2)
    assert np.array_equal(board.cells, np.zeros((4, 2), dtype=np.uint8))
    board.place_piece(0, 0, piece)
    expected_cells = np.array([[1, 1], [1, 0], [0, 0], [0, 0]])
    assert np.array_equal(board.cells, expected_cells)
    assert not board.can_place_piece(0, 0, piece)
    assert not board.can_place_piece(1, 0, piece)

    with pytest.raises(Exception):
        board.place_piece(1, 0, piece)
    
    board.place_piece(1, 0, piece.rotate_piece(Rotation.OneEighty))
    expected_cells = np.array([[1, 1], [1, 1], [1, 1], [0, 0]])
    assert np.array_equal(board.cells, expected_cells)
    