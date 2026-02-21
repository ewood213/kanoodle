import numpy as np
import kanoodle.algorithms.algorithm_x as algx

def test_wikipedia_solution():
    array = np.array([[1, 0, 0, 1, 0, 0, 1],
                      [1, 0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 1],
                      [0, 0, 1, 0, 1, 1, 0],
                      [0, 1, 1, 0, 0, 1, 1],
                      [0, 1, 0, 0, 0, 0, 1]])
    assert algx.exact_cover(array) == set([1, 3, 5])

def test_no_solution1():
    array = np.array([[1, 0, 0, 1, 0, 0, 0],
                  [1, 0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 1, 1, 0, 1],
                  [0, 0, 1, 0, 1, 1, 0],
                  [0, 1, 1, 0, 0, 1, 1],
                  [0, 1, 0, 0, 0, 0, 0]])
    assert algx.exact_cover(array) == None

def test_no_solution2():
    array = np.array([[1, 0]])
    assert algx.exact_cover(array) == None