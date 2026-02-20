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

    def get_layout(self, rotation: Rotation) -> np.ndarray:
        # Handle unmirrored cases
        if rotation == Rotation.Zero:
            return self.layout
        elif rotation == Rotation.Ninety:
            return self.layout[::-1].T
        elif rotation == Rotation.OneEighty:
            return self.layout[::-1, ::-1]
        elif rotation == Rotation.TwoSeventy:
            return self.layout[:, ::-1].T
        else:
            # Handle the mirrored cases (we can assume they are always one below the unmirroed ones)
            normal_rotation = Rotation(rotation.value - 1)
            return self.get_layout(normal_rotation)[:, ::-1]

    def get_all_rotations(self) -> List[np.ndarray]:
        ret = []
        for rotation in Rotation:
            new_layout = self.get_layout(rotation)
            if not any([np.array_equal(arr, new_layout) for arr in ret]):
                ret.append(new_layout)
        return ret

