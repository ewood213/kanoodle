from __future__ import annotations
from enum import Enum
import numpy as np
from typing import List

# The mirrored cases are always one above the "normal" ones
class Rotation(Enum):
    Zero = 0
    ZeroMirroed = 1
    Ninety = 2
    NinetyMirrored = 3
    OneEighty = 4
    OneEightyMirrored = 5
    TwoSeventy = 6
    TwoSeventyMirrored = 7

class Piece:
    def __init__(self, layout: np.ndarray):
        self.layout = layout

    def rotate_piece(self, rotation: Rotation) -> Piece:
        # Handle unmirrored cases
        if rotation == Rotation.Zero:
            return Piece(self.layout)
        elif rotation == Rotation.Ninety:
            return Piece(self.layout[::-1].T)
        elif rotation == Rotation.OneEighty:
            return Piece(self.layout[::-1, ::-1])
        elif rotation == Rotation.TwoSeventy:
            return Piece(self.layout[:, ::-1].T)
        else:
            # Handle the mirrored cases (we can assume they are always one below the unmirroed ones)
            normal_rotation = Rotation(rotation.value - 1)
            return Piece(self.rotate_piece(normal_rotation).layout[:, ::-1])

    def get_all_rotations(self) -> List[Piece]:
        ret = []
        for rotation in Rotation:
            rotated_piece = self.rotate_piece(rotation)
            if not any([piece == rotated_piece for piece in ret]):
                ret.append(rotated_piece)
        return ret
    
    def __eq__(self, other: Piece) -> bool:
        return np.array_equal(self.layout, other.layout)
    
    def __repr__(self):
        return f"layout: {self.layout}"


