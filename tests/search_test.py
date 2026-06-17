import pytest
import numpy as np

from grapyte import SimpleGraph, SimpleGraphAdj

"""
Numerous search tests, both for Adjacency matricies as well as
Adjacency lists.
"""

def test_DFS_lecture():
    """
    Test Depth-first Search based on the lecture example.
    """

    G = SimpleGraph({"a", "b", "c", "d", "e", "f",
                   "g", "h", "i", "j", "k", "l"},
                   [("a", "b"), ("a", "e"), ("e", "i"),("e", "j"), ("i", "j"), 
                   ("c", "d"), ("c", "h"), ("c", "g"), ("g", "h"), ("d", "h"),
                   ("g", "k"), ("h", "k"), ("h", "l")])

    test = G.DFS()
    #print(test)
    assert(test) == {'a': ['b', 'e'], 'b': [], 'c': ['d'], 'd': ['h'], 'e': ['i'], 
                     'f': [], 'g': ['k'], 'h': ['g', 'l'], 'i': ['j'], 'j': [], 
                     'k': [], 'l': []}


def test_DFS_iter_lecture():
    """
    Test whether stack-based Depth-first Search behaves the same way
    as the recursive DFS. 
    """

    G = SimpleGraph({"a", "b", "c", "d", "e", "f",
                   "g", "h", "i", "j", "k", "l"},
                   [("a", "b"), ("a", "e"), ("e", "i"),("e", "j"), ("i", "j"), 
                   ("c", "d"), ("c", "h"), ("c", "g"), ("g", "h"), ("d", "h"),
                   ("g", "k"), ("h", "k"), ("h", "l")])

    test = G.DFS_iter()
    #print(test)
    assert(test) == {'a': ['b', 'e'], 'b': [], 'c': ['d', 'h', 'g'],
                     'd': [], 'e': ['i', 'j'],
                     'f': [], 'g': ['k'], 'h': ['l'], 'i': [], 'j': [],
                     'k': [], 'l': []}


def test_BFS_lecture():
    G = SimpleGraph({"1", "2", "3", "4", "5", "6",
                     "7", "8", "9", "10", "11"},
                    [("1", "2"), ("1", "3"), ("2", "5"), ("2", "4"), ("3", "4"),
                    ("3", "8"), ("4", "7"), ("5", "6"), ("6", "7"), ("6", "9"),
                     ("7", "9"), ("7", "8"), ("8", "10"), ("9", "10"), ("10", "11"),
                     ])
    test = G.BFS()
    # Original search list is as follows:
    # 1: 2, 3
    # 2: -3-, 5, 4 (3 was visited)
    # 3: -5, 4-, 8
    # 5: -4, 8,- 6
    # 4: - 8, 6- , 7
    # 8: -6, 7-, 10
    assert(test) == {'1': ['2', '3'], '2': ['5', '4'], '3': ['8'], '5': ['6'],
                     '4': ['7'], '8': ['10'], '6': ['9'], '7': [], '10': ['11'],
                     '9': [], '11': [] }


"""
SimpleGraphAdj
"""


def test_DFS_lecture_Adj():
    """
    Test whether DFS works the same as on adjacency lists.
    """
    # numpy array
    G = np.zeros((12, 12))
    # declared so for readability
    # [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,]
    # a -> b, e
    G[0][1] = 1
    G[0][4] = 1
    # c
    G[2][3] = 1
    # d
    G[3][7] = 1
    # e -> i
    G[4][8] = 1
    # g -> k
    G[6][10] = 1
    # h -> g, l
    G[7][6] = 1
    G[7][11] = 1
    # i -> j
    G[8][9] = 1
    
    K = SimpleGraphAdj({"a", "b", "c", "d", "e", "f",
                   "g", "h", "i", "j", "k", "l"},
                   [("a", "b"), ("a", "e"), ("e", "i"),("e", "j"), ("i", "j"), 
                   ("c", "d"), ("c", "h"), ("c", "g"), ("g", "h"), ("d", "h"),
                   ("g", "k"), ("h", "k"), ("h", "l")])

    test = K.DFS()
    print(test)
    print(K) 
    assert (test == G).all() 
