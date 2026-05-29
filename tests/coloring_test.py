import pytest
import numpy as np
from grapyte import SimpleGraphAdj
from grapyte.diagnostics.is_colored import is_colored

"""
Basic coloring test.
"""

def test_greedy():
    color_test = SimpleGraphAdj.from_dimacs(path="./dimacs_2nd_ed/flat300_28_0.col.txt")
    c, coloring = color_test.color_RS(return_coloring=True)
    assert c > 29
    assert is_colored(coloring, color_test.adjMatrix, color_test.IndexToVertex)

def test_LF():
    color_test = SimpleGraphAdj.from_dimacs(path="./dimacs_2nd_ed/flat300_28_0.col.txt")
    c, coloring = color_test.color_LF(return_coloring=True)
    assert c == 45
    assert is_colored(coloring, color_test.adjMatrix, color_test.IndexToVertex)

def test_SL():
    color_test = SimpleGraphAdj.from_dimacs(path="./dimacs_2nd_ed/flat300_28_0.col.txt")
    c, coloring = color_test.color_SL(return_coloring=True)
    assert c == 46
    assert is_colored(coloring, color_test.adjMatrix, color_test.IndexToVertex)
