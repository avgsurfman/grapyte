import pytest
import numpy as np
from grapyte import SimpleGraph

"""
This section includes basic instantiation tests as
most methods are inherited.
"""

def test_create_SimpleGraph():
    """
    Test whether the constructor works at all.
    """
    G = SimpleGraph({"a", "b", "c", "d", "e", "f",
                    "g", "h", "i", "j", "k", "l"},
                    [("a", "b"), ("a", "e"), ("e", "i"),("e", "j"), ("i", "j"), 
                    ("c", "d"), ("c", "h"), ("c", "g"), ("g", "h"), ("d", "h"),
                    ("g", "k"), ("h", "k"), ("h", "l")])
    assert G.vertex == {"a", "b", "c", "d", "e", "f",
                       "g", "h", "i", "j", "k", "l"}
    print(G.adjList) 
    assert G.adjList == {'a': ['b', 'e'], 'b': ['a'], 'c': ['d', 'h', 'g'], 'd': ['c', 'h'], 'e': ['a', 'i', 'j'], 'f': [], 'g': ['c', 'h', 'k'], 'h': ['c', 'g', 'd', 'k', 'l'], 'i': ['e', 'j'], 'j': ['e', 'i'], 'k': ['g', 'h'], 'l': ['h']}



def test_SimpleGraph_loop_detection():
    """
    Test whether loop detection works.
    """
    with pytest.raises(ValueError):
        G = SimpleGraph({"a", "b", "c", "d"}, [("a", "b"), ("a", "a")])

 
def test_SimpleGraph_duplicate_detection():
   """
   Test whether duplicate detection works.
   """
   with pytest.raises(ValueError):
        G = SimpleGraph({"a", "b", "c", "d"}, [("a", "b"), ("a", "b")])


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
    #print(test)
    assert(test) == {'a': ['b', 'e'], 'b': [], 'c': ['d'], 'd': ['h'], 'e': ['i'], 
                     'f': [], 'g': ['k'], 'h': ['g', 'l'], 'i': ['j'], 'j': [], 
                     'k': [], 'l': []}
    #raise ValueError("aaaahhh")
# TODO: Loop test in add edge
# TODO: Duplicate test in add_edge
