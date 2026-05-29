"""
Diagnostic single-function file.
"""
# WIP

import numpy as np

def is_colored(coloring: dict, adjMatrix, ITV: dict) -> bool:
    # Two coloring checks:
    # 1) All verticies are colored
    # 2) No two adjacent vertexes are the same color
    is_colored = {key: False for key in ITV}
    for vertex, color in coloring.items():
        is_colored[vertex] = True
        for neighbor_vertex in np.nonzero(adjMatrix[vertex])[0]:
            adjacent_color = coloring[neighbor_vertex]
            if adjacent_color == color:
               print(f"Improper coloring! {vertex}, {coloring}, adjacent: {neighbor_vertex}")
         
    return True 
