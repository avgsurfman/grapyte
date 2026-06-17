import pytest
import numpy as np
from grapyte import SimpleGraph

"""
This section includes basic instantiation tests as
most methods are inherited.
"""

def test_is_tree_dfs():
    """
    Test the isTree implementation against a simple search tree.
    Guards against regression.
    Should probably be renamed to "istree".
    """
    search_tree = [('a', 'b'), ('a', 'e'), ('e', 'i'), ('i', 'j')]
    K = SimpleGraph({'a', 'b', 'e', 'i', 'j'}, search_tree)
    assert K.is_tree_dfs()
