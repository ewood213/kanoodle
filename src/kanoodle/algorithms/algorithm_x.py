import numpy as np
from typing import Optional, Set
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def _exact_cover_inner(incidence_matrix: np.ndarray, partial_solution: Set[int], row_indices: np.ndarray, col_indices: np.ndarray) -> Optional[Set[int]]:
    logger.debug(f"Current incidence matrix {incidence_matrix}")
    logger.debug(f"Partial Solution {partial_solution}")
    # See if we are done
    if col_indices.size == 0:
        return partial_solution

    # Sort by column of least zeros
    column_count = np.sum(incidence_matrix, axis=0)
    sorted_column_count_idx = np.argsort(column_count)
    if column_count[sorted_column_count_idx[0]] == 0:
        logger.debug("Sending back none")
        return None
    for column_idx in sorted_column_count_idx:
        min_ones_column = incidence_matrix[:, column_idx]
        rows_with_one = np.argwhere(min_ones_column)

        # Go through rows with one in column
        for row_idx in rows_with_one:
            cur_row = incidence_matrix[row_idx].reshape(-1)
            rows_to_remove = []
            # Remove rows and columns that share a one
            for i, row in enumerate(incidence_matrix):
                if np.any(cur_row & row):
                    rows_to_remove.append(i)
            cols_to_remove = np.argwhere(cur_row)
            new_ar = np.delete(incidence_matrix, rows_to_remove, axis=0)
            new_ar = np.delete(new_ar, cols_to_remove, axis=1)
            new_row_indices = np.delete(row_indices, rows_to_remove)
            new_col_indices = np.delete(col_indices, cols_to_remove)

            # Recurse!
            to_add = set([int(row_indices[row_idx][0])])
            ret = _exact_cover_inner(new_ar, partial_solution.union(to_add), new_row_indices, new_col_indices)
            if ret is not None:
                return ret
    return None



def exact_cover(incidence_matrix: np.ndarray) -> Optional[Set[int]]:
    return _exact_cover_inner(incidence_matrix, set(), np.arange(incidence_matrix.shape[0]), np.arange(incidence_matrix.shape[1]))

