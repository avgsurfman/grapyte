import pytest
import numpy as np
from grapyte import SimpleGraphAdj

"""
Directed tests.
"""

def test_create_SimpleGraphAdj():
    # does the new constructor work?
    newGraph = SimpleGraphAdj({'a', 'b', 'c', 'd'}, [('a', 'b',), ('a', 'b'), ('a', 'c'), ('a', 'd')], name = "Example")        
    ####a#b#c#d 
    # a 0 2 1 1
    # b 0 0 0 0
    # c 0 0 0 0
    # d 0 0 0 0
    print(newGraph)
    retArr = np.array([[0, 2, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]])


def test_DFS_lecture():
    """
    test the dfs
    """

    G = SimpleGraph({"a", "b", "c", "d", "e", "f",
                   "g", "h", "i", "j", "k", "l"},
                   [("a", "b"), ("a", "e"), ("e", "i"),("e", "j"), ("i", "j"), 
                   ("c", "d"), ("c", "h"), ("c", "g"), ("g", "h"), ("d", "h"),
                   ("g", "k"), ("h", "k"), ("h", "l")])

    test = G.DFS()
    raise NotImplementedError("ahhhhh to do")
    #print(test)
    #assert(test) == {'a': ['b', 'e'], 'b': [], 'c': ['d'], 'd': ['h'], 'e': ['i'], 
    #                 'f': [], 'g': ['k'], 'h': ['g', 'l'], 'i': ['j'], 'j': [], 
    #                 'k': [], 'l': []}

# TODO: multiple edge errors out (same vertex).
# TODO: multiple edge errors out (opposite vertex)

