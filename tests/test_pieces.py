import kanoodle.game.pieces as pieces
import numpy as np

def test_rotations_j_piece():
    original = pieces.Piece(np.array([[1, 1],
                       [1, 0],
                       [1, 0]]))

    ninety = pieces.Piece(np.array([[1, 1, 1],
                       [0, 0, 1]]))

    one_eighty = pieces.Piece(np.array([[0, 1],
                           [0, 1],
                           [1, 1]]))

    two_seventy = pieces.Piece(np.array([[1, 0, 0],
                            [1, 1, 1]]))

    original_mirrored = pieces.Piece(np.array([[1, 1],
                                [0, 1],
                                [0, 1]]))

    ninety_mirrored = pieces.Piece(np.array([[1, 1, 1],
                                [1, 0, 0]]))

    one_eighty_mirrored = pieces.Piece(np.array([[1, 0],
                                    [1, 0],
                                    [1, 1]]))

    two_seventy_mirrored = pieces.Piece(np.array([[0, 0, 1],
                                     [1, 1, 1]]))

    piece = original
    assert piece.rotate_piece(pieces.Rotation.Zero) ==  original
    assert piece.rotate_piece(pieces.Rotation.Ninety) ==  ninety
    assert piece.rotate_piece(pieces.Rotation.OneEighty) ==  one_eighty
    assert piece.rotate_piece(pieces.Rotation.TwoSeventy) ==  two_seventy
    assert piece.rotate_piece(pieces.Rotation.ZeroMirroed) ==  original_mirrored
    assert piece.rotate_piece(pieces.Rotation.NinetyMirrored) ==  ninety_mirrored
    assert piece.rotate_piece(pieces.Rotation.OneEightyMirrored) ==  one_eighty_mirrored
    assert piece.rotate_piece(pieces.Rotation.TwoSeventyMirrored) ==  two_seventy_mirrored

    all_rotations_expected = [original, original_mirrored, ninety, ninety_mirrored, one_eighty, one_eighty_mirrored, two_seventy, two_seventy_mirrored]
    all_rotations_actual = piece.get_all_rotations()

    assert len(all_rotations_expected) == len(all_rotations_actual)
    for r_expected, r_actual in zip(all_rotations_expected, all_rotations_actual):
        assert r_expected == r_actual

def test_rotations_plus_piece():
    original = pieces.Piece(np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]))
    piece = original
    assert piece.rotate_piece(pieces.Rotation.Zero) == original
    assert piece.rotate_piece(pieces.Rotation.Ninety) == original
    assert piece.rotate_piece(pieces.Rotation.OneEighty) == original
    assert piece.rotate_piece(pieces.Rotation.TwoSeventy) == original
    assert piece.rotate_piece(pieces.Rotation.ZeroMirroed) == original
    assert piece.rotate_piece(pieces.Rotation.NinetyMirrored) == original
    assert piece.rotate_piece(pieces.Rotation.OneEightyMirrored) == original
    assert piece.rotate_piece(pieces.Rotation.TwoSeventyMirrored) == original

    all_rotations_expected = [original]
    all_rotations_actual = piece.get_all_rotations()
    assert len(all_rotations_expected) == len(all_rotations_actual)
    for r_expected, r_actual in zip(all_rotations_expected, all_rotations_actual):
        assert r_expected == r_actual

def test_rotations_zigzag_piece():
    original = pieces.Piece(np.array([[1, 0, 0],
                       [1, 1, 0],
                       [0, 1, 1]]))

    ninety = pieces.Piece(np.array([[0, 1, 1],
                       [1, 1, 0],
                       [1, 0, 0]]))

    one_eighty = pieces.Piece(np.array([[1, 1, 0],
                           [0, 1, 1],
                           [0, 0, 1]]))

    two_seventy = pieces.Piece(np.array([[0, 0, 1],
                            [0, 1, 1],
                            [1, 1, 0]]))

    original_mirrored = pieces.Piece(np.array([[0, 0, 1],
                                [0, 1, 1],
                                [1, 1, 0]]))

    ninety_mirrored = pieces.Piece(np.array([[1, 1, 0],
                                [0, 1, 1],
                                [0, 0, 1]]))

    one_eighty_mirrored = pieces.Piece(np.array([[0, 1, 1],
                                    [1, 1, 0],
                                    [1, 0, 0]]))

    two_seventy_mirrored = pieces.Piece(np.array([[1, 0, 0],
                                     [1, 1, 0],
                                     [0, 1, 1]]))

    piece = original
    assert piece.rotate_piece(pieces.Rotation.Zero) == original
    assert piece.rotate_piece(pieces.Rotation.Ninety) == ninety
    assert piece.rotate_piece(pieces.Rotation.OneEighty) == one_eighty
    assert piece.rotate_piece(pieces.Rotation.TwoSeventy) == two_seventy
    assert piece.rotate_piece(pieces.Rotation.ZeroMirroed) == original_mirrored
    assert piece.rotate_piece(pieces.Rotation.NinetyMirrored) == ninety_mirrored
    assert piece.rotate_piece(pieces.Rotation.OneEightyMirrored) == one_eighty_mirrored
    assert piece.rotate_piece(pieces.Rotation.TwoSeventyMirrored) == two_seventy_mirrored

    all_rotations_expected = [original, original_mirrored, ninety, ninety_mirrored]
    all_rotations_actual = piece.get_all_rotations()

    assert len(all_rotations_expected) == len(all_rotations_actual)
    for r_expected, r_actual in zip(all_rotations_expected, all_rotations_actual):
        assert r_expected == r_actual

