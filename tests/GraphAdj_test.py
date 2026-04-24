import pytest
import numpy as np
from grapyte import GraphAdj

"""
Directed tests.
"""

def test_create_GraphAdj():
    newGraph = GraphAdj({'a', 'b', 'c', 'd'}, [('a', 'b',), ('a', 'b'), ('a', 'c'), ('a', 'd')], name = "Example")        
    ####a#b#c#d 
    # a 0 2 1 1
    # b 0 0 0 0
    # c 0 0 0 0
    # d 0 0 0 0
    print(newGraph)
    retArr = np.array([[0, 2, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]])
    

def test_create_GraphAdj_error():
    # should error out 
    with pytest.raises(KeyError):
        newGraph = GraphAdj({'a', 'b', 'c'}, [('a', 'b',), ('a', 'b'), ('a', 'c'), ('a', 'd')], name = "Example")        


def test_add_vertex():
    newGraph = GraphAdj({'a', 'b', 'c', 'd'}, [('a', 'b',), ('a', 'b'), ('a', 'c'), ('a', 'd')], name = "Example")        
    newGraph.add_vertex("z")
    print(newGraph)
    assert "z" in newGraph.VertexToIndex
    assert "z"  == newGraph.IndexToVertex[newGraph.VertexToIndex["z"]]
    # assert z is added as last
    assert 4 == newGraph.VertexToIndex["z"]
    
    # test whether there in fact is a zeroed row/col in the array
    print(newGraph.adjMatrix[:, 4])
    print(newGraph.adjMatrix[:, 1])
    # column-wise assertion
    assert (newGraph.adjMatrix[:, 4] == np.zeros(5)).all()
    # row-wise assertion
    assert (newGraph.adjMatrix[4, :] == np.zeros((1, 5))).all()
    # assert the old matrix is unchanged 
    # TODO:    


#
#newGraph.add_edge(("b", "z"))
#print(newGraph)
#
#
## Directed tests
#newGraph = GraphAdj({'a', 'b'}, [('a', 'b',), ('a', 'b')], name = "Example")        
#print(newGraph)
#
#newGraph = GraphAdj({'a', 'b', 'c', 'd'}, [('a', 'b',), ('a', 'b'), ('a', 'c'), ('a', 'd')], name = "Example")        
#print(newGraph)
#
## should error out
#newGraph = GraphAdj({'a', 'b', 'c'}, [('a', 'b',), ('a', 'b'), ('a', 'c'), ('a', 'd')], name = "Example")        
#print(newGraph)
#
#newGraph.add_vertex("z")
#print(newGraph)
#
#newGraph.add_edge(("b", "z"))
#print(newGraph)
