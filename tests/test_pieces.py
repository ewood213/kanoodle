import kanoodle.game.pieces as pieces
import numpy as np

def test_rotations_j_piece():
    layout = np.array([[1, 1],
                       [1, 0],
                       [1, 0]])

    ninety = np.array([[1, 1, 1],
                       [0, 0, 1]])

    one_eighty = np.array([[0, 1],
                           [0, 1],
                           [1, 1]])

    two_seventy = np.array([[1, 0, 0],
                            [1, 1, 1]])

    layout_mirrored = np.array([[1, 1],
                                [0, 1],
                                [0, 1]])

    ninety_mirrored = np.array([[1, 1, 1],
                                [1, 0, 0]])

    one_eighty_mirrored = np.array([[1, 0],
                                    [1, 0],
                                    [1, 1]])

    two_seventy_mirrored = np.array([[0, 0, 1],
                                     [1, 1, 1]])

    piece = pieces.Piece(layout)
    assert np.array_equal(piece.get_layout(pieces.Rotation.Zero), layout)
    assert np.array_equal(piece.get_layout(pieces.Rotation.Ninety), ninety)
    assert np.array_equal(piece.get_layout(pieces.Rotation.OneEighty), one_eighty)
    assert np.array_equal(piece.get_layout(pieces.Rotation.TwoSeventy), two_seventy)
    assert np.array_equal(piece.get_layout(pieces.Rotation.ZeroMirroed), layout_mirrored)
    assert np.array_equal(piece.get_layout(pieces.Rotation.NinetyMirrored), ninety_mirrored)
    assert np.array_equal(piece.get_layout(pieces.Rotation.OneEightyMirrored), one_eighty_mirrored)
    assert np.array_equal(piece.get_layout(pieces.Rotation.TwoSeventyMirrored), two_seventy_mirrored)

    all_rotations_expected = [layout, layout_mirrored, ninety, ninety_mirrored, one_eighty, one_eighty_mirrored, two_seventy, two_seventy_mirrored]
    all_rotations_actual = piece.get_all_rotations()

    assert len(all_rotations_expected) == len(all_rotations_actual)
    for r_expected, r_actual in zip(all_rotations_expected, all_rotations_actual):
        assert np.array_equal(r_expected, r_actual)

def test_rotations_plus_piece():
    layout = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    piece = pieces.Piece(layout)
    assert np.array_equal(piece.get_layout(pieces.Rotation.Zero), layout)
    assert np.array_equal(piece.get_layout(pieces.Rotation.Ninety), layout)
    assert np.array_equal(piece.get_layout(pieces.Rotation.OneEighty), layout)
    assert np.array_equal(piece.get_layout(pieces.Rotation.TwoSeventy), layout)
    assert np.array_equal(piece.get_layout(pieces.Rotation.ZeroMirroed), layout)
    assert np.array_equal(piece.get_layout(pieces.Rotation.NinetyMirrored), layout)
    assert np.array_equal(piece.get_layout(pieces.Rotation.OneEightyMirrored), layout)
    assert np.array_equal(piece.get_layout(pieces.Rotation.TwoSeventyMirrored), layout)

    all_rotations_expected = [layout]
    all_rotations_actual = piece.get_all_rotations()
    assert len(all_rotations_expected) == len(all_rotations_actual)
    for r_expected, r_actual in zip(all_rotations_expected, all_rotations_actual):
        assert(np.array_equal(r_expected, r_actual))

def test_rotations_zigzag_piece():
    layout = np.array([[1, 0, 0],
                       [1, 1, 0],
                       [0, 1, 1]])

    ninety = np.array([[0, 1, 1],
                       [1, 1, 0],
                       [1, 0, 0]])

    one_eighty = np.array([[1, 1, 0],
                           [0, 1, 1],
                           [0, 0, 1]])

    two_seventy = np.array([[0, 0, 1],
                            [0, 1, 1],
                            [1, 1, 0]])

    layout_mirrored = np.array([[0, 0, 1],
                                [0, 1, 1],
                                [1, 1, 0]])

    ninety_mirrored = np.array([[1, 1, 0],
                                [0, 1, 1],
                                [0, 0, 1]])

    one_eighty_mirrored = np.array([[0, 1, 1],
                                    [1, 1, 0],
                                    [1, 0, 0]])

    two_seventy_mirrored = np.array([[1, 0, 0],
                                     [1, 1, 0],
                                     [0, 1, 1]])

    piece = pieces.Piece(layout)
    assert np.array_equal(piece.get_layout(pieces.Rotation.Zero), layout)
    assert np.array_equal(piece.get_layout(pieces.Rotation.Ninety), ninety)
    assert np.array_equal(piece.get_layout(pieces.Rotation.OneEighty), one_eighty)
    assert np.array_equal(piece.get_layout(pieces.Rotation.TwoSeventy), two_seventy)
    assert np.array_equal(piece.get_layout(pieces.Rotation.ZeroMirroed), layout_mirrored)
    assert np.array_equal(piece.get_layout(pieces.Rotation.NinetyMirrored), ninety_mirrored)
    assert np.array_equal(piece.get_layout(pieces.Rotation.OneEightyMirrored), one_eighty_mirrored)
    assert np.array_equal(piece.get_layout(pieces.Rotation.TwoSeventyMirrored), two_seventy_mirrored)

    all_rotations_expected = [layout, layout_mirrored, ninety, ninety_mirrored]
    all_rotations_actual = piece.get_all_rotations()

    assert len(all_rotations_expected) == len(all_rotations_actual)
    for r_expected, r_actual in zip(all_rotations_expected, all_rotations_actual):
        assert np.array_equal(r_expected, r_actual)

