"""graPyte - a small Python graph library."""
__version__ = "0.0.1"
__author__ = "Franciszek Moszczuk, Karol Mądraszek"
PACKAGE_NAME = "grapyte"

__all__ = ['Graph', 'GraphAdj', 'GraphEdge']

from .Graph import Graph
from .GraphAdj import GraphAdj
from .GraphEdge import GraphEdge
