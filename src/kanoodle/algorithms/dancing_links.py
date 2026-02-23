import numpy as np

class Node:
    def __init__(self, left, right, up, down, column, name):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.column = column
        self.name = name

class Column:
    def __init__(self, left, right, up, down, column, size, name):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.column = column
        self.size = size
        self.name = name


def add_column_headers(root, incidence_matrix):
    num_cols = incidence_matrix.shape[1]
    cur_node = root
    for i in range(num_cols):
        size = np.count_nonzero(incidence_matrix[:, i])
        new_column = Column(cur_node, None, None, None, None, size, i)
        new_column.up = new_column
        new_column.down = new_column
        new_column.column = new_column
        cur_node.right = new_column
        cur_node = new_column
    cur_node.right = root
    root.left = cur_node


def create_links_from_mat(incidence_matrix):
    root = Column(None, None, None, None, None, None, -1)
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
            new_node = Node(last_node, None, cur_col.up, cur_col, cur_col, [i, one_location])

            # Insert node into up down list
            cur_col.up.down = new_node
            cur_col.up = new_node

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

def get_smallest_col(root):
    cur = root.right
    ret = cur
    smallest_size = cur.size
    while cur is not root:
        if cur.size < smallest_size:
            ret = cur
            smallest_size = cur.size
        cur = cur.right
    return ret

def cover_column(c):
    # Remove column
    c.right.left = c.left
    c.left.right = c.right

    # Remove column elements that share ones
    i = c.down
    while i is not c:
        j = i.right
        while j is not i:
            j.down.up = j.up
            j.up.down = j.down
            j.column.size -= 1
            j = j.right
        i = i.down

def uncover_column(c):
    # Restore column elements that share ones
    i = c.up
    while i is not c:
        j = i.left
        while j is not i:
            j.column.size += 1
            j.down.up = j
            j.up.down = j
            j = j.left
        i = i.up

    # Restore column
    c.right.left = c
    c.left.right = c

def _search(root, cur_sol):
    if root.right == root:
        return cur_sol
    c = get_smallest_col(root)
    if c.size == 0:
        return None

    # Remove column and add first row in column as solution
    cover_column(c)
    r = c.down
    cur_sol.append(None)
    while r is not c:
        cur_sol[-1] = r
        j = r.right

        # Remove columns that are also contained in row
        while j is not r:
            cover_column(j.column)
            j = j.right

        # Recurse to find solution
        ret = _search(root, cur_sol)
        if ret is not None:
            return ret

        # Now begin restoring...
        c = r.column
        j = r.left
        while j is not r:
            uncover_column(j.column)
            j = j.left
        r = r.down

    # Make sure our unused solution doesn't stick around
    cur_sol.pop()
    uncover_column(c)


def search(root):
    solution = _search(root, [])
    if solution is None:
        return None
    ret = []
    for r in [s for s in solution if s is not None]:
        row = []
        row.append(r.column.name)
        j = r.right
        while j is not r:
            row.append(j.column.name)
            j = j.right
        ret.append(row)
    return ret

def solve_using_dancing_links(incidence_matrix):
    root = create_links_from_mat(incidence_matrix)
    solution = search(root)
    if solution is None:
        return None
    ret = np.zeros((len(solution), incidence_matrix.shape[1]), dtype=np.uint8)
    for i in range(len(solution)):
        for j in solution[i]:
            ret[i][j] = 1
    return ret

