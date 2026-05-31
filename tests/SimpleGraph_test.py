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


def test_add_edge():
   """
   Does edge addition actually work after overriding?
   """
   G = SimpleGraph({"a", "b", "c"}, [("a", "b"),])
   G.add_edge(("a", "c"))
   assert G.adjList == {'a': ['b', 'c'], 'b': ['a'], 'c': ['a']}


def test_add_edge_empty_graph():
    """
    Does edge addition actually work after overriding?
    """
    G = SimpleGraph({"a", "b"}, [])
    G.add_edge(("a", "b"))
    assert G.adjList == {'a': ['b'], 'b': ['a']}


def test_add_duplicate_edge():
   """
   Edge addition should also validate if a duplicate edge exists.
   """
   G = SimpleGraph({"a", "b", "c"}, [("a", "b"),("a", "c")])
   with pytest.raises(ValueError):
       G.add_edge(("a", "c")) # here pycharm autocomplete was disabled
       # Rest in Piss 2026
       # "Tried to triplicate my edges! What an asshat!"


def test_add_loop_edge():
   """
   ... or if the edge loops back to the same vertex...
   """
   G = SimpleGraph({"a", "b", "c"}, [("a", "b"),("a", "c")])
   with pytest.raises(ValueError):
       G.add_edge(("a", "a"))


def test_add_nonexistent_vertex():
   """
   ... or if the vertex DNE in graph.
   """
   G = SimpleGraph({"a", "b", "c"}, [("a", "b"),("a", "c")])
   with pytest.raises(KeyError):
       G.add_edge(("a", "d"))


def test_tuples_as_ints():
   """
   Test whether int edge tuples like (1,4) are accepted and converted to ("1", "4")
   """
   G = SimpleGraph({1, 2, 3}, [(1, 2),(2, 3)])
   assert G.adjList == {"1": ["2"], "2": ["1", "3"], "3": ["2"]}


def test_shorter_notation():
   """
   For a SimpleGraph, it should be sufficient to supply an edge list.
   The set should be optional in case the user would like a subgraph.
   The set should absolutely be required if the user supplies an edge-less graph.
   """
   raise NotImplementedError("TODO")


