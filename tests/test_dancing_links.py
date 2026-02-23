import numpy as np
import kanoodle.algorithms.dancing_links as dl
def test_header_creation():
    test_matrix = np.array([[0, 0, 1, 0, 1, 1, 0],
                            [1, 0, 0, 1, 0, 0, 1],
                            [0, 1, 1, 0, 0, 1, 0],
                            [1, 0, 0, 1, 0, 0, 0],
                            [0, 1, 0, 0, 0, 0, 1],
                            [0, 0, 0, 1, 1, 0, 1]])

    root = dl.Column(None, None, None, None, None, None, None)
    dl.add_column_headers(root, test_matrix)
    column_size = [2, 2, 2, 3, 2, 2, 3]
    start = root.right
    i = 0
    while start is not root:
        assert start.name == i
        assert start.size == column_size[i]
        assert start.up == start.down == start
        start = start.right
        i+=1
    assert i == 7
    start = root.left

    i = 6
    while start is not root:
        assert start.name == i
        assert start.size == column_size[i]
        start = start.left
        i-=1
    assert i == -1

def test_create_links():
    test_matrix = np.array([[0, 1, 0], [1, 1, 0], [1, 1, 0]])
    root = dl.create_links_from_mat(test_matrix)

    # test column headers
    assert root.right.name == 0
    assert root.right.size == 2
    assert root.right.right.name == 1
    assert root.right.right.size == 3
    assert root.right.right.right.name == 2
    assert root.right.right.right.size == 0
    assert root.right.right.right.right == root
    assert root.left.name == 2
    assert root.left.left.name == 1
    assert root.left.left.left.name == 0
    assert root.left.left.left.left == root

    # test first col
    first_col_start = root.right.down
    assert first_col_start.name == [1, 0]
    assert first_col_start.column == root.right
    assert first_col_start.down.name == [2, 0]
    assert first_col_start.down.down.name == 0
    assert first_col_start.up.name == 0
    assert first_col_start.down.column == root.right

    # test second col
    second_col_start = root.right.right.down
    assert second_col_start.name == [0, 1]
    assert second_col_start.column == root.right.right
    assert second_col_start.down.name == [1, 1]
    assert second_col_start.down.column == root.right.right
    assert second_col_start.down.down.name == [2, 1]
    assert second_col_start.down.down.column == root.right.right
    assert second_col_start.down.down.down.name == 1
    assert second_col_start.up.name == 1
    assert second_col_start.up.up.name == [2, 1]
    assert second_col_start.up.up.up.name == [1, 1]
    assert second_col_start.up.up.up.up == second_col_start

    # test third column
    third_column_start = root.left.up
    assert third_column_start.name == 2
    assert third_column_start.up == third_column_start.down == third_column_start
    assert third_column_start.column == third_column_start

    # test first row
    first_row_start = second_col_start
    assert first_row_start.right == first_row_start.left == first_row_start

    # test second row
    second_row_start = first_col_start
    assert second_row_start.left.name == [1, 1]
    assert second_row_start.right.name == [1, 1]
    assert second_row_start.left.left == second_row_start
    assert second_row_start.right.right == second_row_start

    # test third row
    third_row_start = root.right.up
    assert third_row_start.name == [2, 0]
    assert third_row_start.right.name == [2, 1]
    assert third_row_start.right.right == third_row_start
    assert third_row_start.left.name == [2, 1]
    assert third_row_start.left.left == third_row_start

def test_solve_dancing_links():
    test_matrix = np.array([[0, 0, 1, 0, 1, 1, 0],
                                [1, 0, 0, 1, 0, 0, 1],
                                [0, 1, 1, 0, 0, 1, 0],
                                [1, 0, 0, 1, 0, 0, 0],
                                [0, 1, 0, 0, 0, 0, 1],
                                [0, 0, 0, 1, 1, 0, 1]])
    expected_solution = np.zeros((3, 7), dtype=np.uint8)
    expected_solution[0] = test_matrix[3]
    expected_solution[1] = test_matrix[0]
    expected_solution[2] = test_matrix[4]
    assert np.array_equal(dl.solve_using_dancing_links(test_matrix), expected_solution)

def test_wikipedia_solution():
    array = np.array([[1, 0, 0, 1, 0, 0, 1],
                      [1, 0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 1],
                      [0, 0, 1, 0, 1, 1, 0],
                      [0, 1, 1, 0, 0, 1, 1],
                      [0, 1, 0, 0, 0, 0, 1]])
    expected_solution = np.zeros((3, 7), dtype=np.uint8)
    expected_solution[0] = array[1]
    expected_solution[1] = array[3]
    expected_solution[2] = array[5]

    assert np.array_equal(dl.solve_using_dancing_links(array), expected_solution)

def test_no_solution():
    array = np.array([[0, 0, 0, 1, 0, 0, 1],
                      [0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 1],
                      [0, 0, 1, 0, 1, 1, 0],
                      [0, 1, 1, 0, 0, 1, 1],
                      [0, 1, 0, 0, 0, 0, 1]])

    assert dl.solve_using_dancing_links(array) == None

def test_extra_sol_dl():
    # setup test array so it has to pop a solution from its solution set
    array = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 1],
                     [0, 0, 1, 1],
                     [0, 1, 1, 0],
                     [1, 1, 1, 1]])
    solution = dl.solve_using_dancing_links(array)
    assert len(solution) == 1
    assert np.array_equal(solution[0], np.array([1, 1, 1, 1]))