import pytest
from grapyte import Graph

def test_add_vertex():
    """
    Adds a new vertex z to the graph.
    """
    newGraph = Graph({'a', 'b'}, [('a', 'b',), ('a', 'b')], name = "Example")        
    newGraph.add_vertex("z")
    print(newGraph)
    assert "z" in newGraph.vertex


def test_add_edge():
    """
    Add edge to an Adjacency list.
    This test can be easily generalized, swap "z" for every vertex.
    """ 
    newGraph = Graph({'a', 'b'}, [('a', 'b',), ('a', 'b')], name = "Example")        
    newGraph.add_vertex("z")
    newGraph.add_edge(("b", "z"))
    print(newGraph)
    assert "z" in newGraph.adjList["b"]


def test_add_edge_error():
    """
    Check whether we error out on a vertex that is not in the Graph.
    """ 
    newGraph = Graph({'a', 'b'}, [('a', 'b',), ('a', 'b')], name = "Example")        
    newGraph.add_vertex("z")
    with pytest.raises(KeyError):
        newGraph.add_edge(("z", "y")) #errors out on purpose


def test_remove_edge():
    """
    Remove edge from an Adjacency list.
    This test can be easily generalized, swap "a" for every vertex.
    """ 
    newGraph = Graph({'a', 'b'}, [('a', 'b',), ('a', 'b')], name = "Example")        
    newGraph.remove_edge(("a", "b"))
    # assert is once
    assert newGraph.adjList["a"].count("b") == 1

def test_remove_vertex():
    """
    This test can be easily generalized, swap "a" for every vertex.
    """ 
    newGraph = Graph({'a', 'b'}, [('a', 'b',), ('a', 'b')], name = "Example")        
    print(newGraph.adjList)
    newGraph.remove_vertex("b")
    print(newGraph.adjList)
    assert "b" not in newGraph.adjList["a"]
    print(newGraph.vertex)
    # this test case actually fixed an error!
    assert "b" not in newGraph.vertex


## newGraph.remove_vertex("p") # key not in set
#print(newGraph)

