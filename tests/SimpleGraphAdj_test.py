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


# TODO: multiple edge errors out (same vertex).
# TODO: multiple edge errors out (opposite vertex)

