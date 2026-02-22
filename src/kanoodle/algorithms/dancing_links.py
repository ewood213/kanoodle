import numpy as np
class Node:
    def __init__(self, left, right, up, down, column, first_obj, name):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.column = column
        self.first_obj = first_obj
        self.name = name

class Column:
    def __init__(self, left, right, up, down, first_obj, size, name):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.first_obj = first_obj
        self.size = size
        self.name = name


def add_column_headers(root, incidence_matrix):
    num_cols = incidence_matrix.shape[1]
    cur_node = root
    for i in range(num_cols):
        size = np.count_nonzero(incidence_matrix[:, i])
        new_column = Column(cur_node, None, None, None, None, size, f"{i+1}")
        new_column.up = new_column
        new_column.down = new_column
        cur_node.right = new_column
        cur_node = new_column
    cur_node.right = root
    root.left = cur_node


def create_links_from_mat(incidence_matrix):
    root = Column(None, None, None, None, None, None, "0")
    add_column_headers(root, incidence_matrix)
    for i, row in enumerate(incidence_matrix):
        one_locations = np.argwhere(row).reshape(-1)
        cur_col = root.right
        cur_col_num = 0
        last_node = None
        first_node = None

        # Begin creating nodes for our ones
        for one_location in one_locations:

            # Iterate to the appropriate column header
            while cur_col_num != one_location:
                cur_col_num += 1
                cur_col = cur_col.right

            # Create our node, and set its left, up and down parameters
            new_node = Node(last_node, None, cur_col.up, cur_col, cur_col, None, [i, one_location])

            # Insert node into up down list
            cur_col.up.down = new_node
            cur_col.up = new_node

            # Set the first obj
            if cur_col.first_obj is None:
                cur_col.first_obj = new_node
                new_node.first_obj = new_node
            else:
                new_node.first_obj = cur_col.first_obj

            # Set right node
            if last_node is not None:
                last_node.right = new_node

            # keep track of our last and first processed node
            last_node = new_node
            if first_node is None:
                first_node = new_node

        # Set first and last nodes right and left pointers
        if first_node is not None:
            first_node.left = last_node
            last_node.right = first_node

    # Phew!
    return root


