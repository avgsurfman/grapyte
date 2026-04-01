class GraphEdge:
    """
    Edge Multigraph class. Uses an edge list.
    This was a starter template for other classes (like Graph adjacency).
     
    CC Franciszek Moszczuk
    """

    
    def __init__(self, vertex: set, edges: list, name = "Unnamed"):
        """
        Uses tuples by default because the graph isn't the same after it's modified,
        therefore it makes sense to make edges a list of tuples
        """
        # adjacency list is like a dict with a tuple list actually
        
        # sort set
        # assumes only strings for now
        templist = sorted(vertex)
        self.vertex = set(templist)
        self.edges = []
            
        for u, v in edges:
            if u not in self.vertex or v not in self.vertex:
               print(f"{u} or {v} not in set, skipping...")
            else:
               self.edges.append((u, v))
        self.name = name
 

    def __str__(self):
        return f"Edge Multigraph {self.name} with the following params:\n \
               Vertex: {self.vertex}, Edges tuple: {self.edges}"

    def add_vertex(self, vertex: str):
        """
        Adds a vertex to the graph. Assumed a UTF-8 character (Python default)
        """
        self.vertex.add(vertex)

    def remove_vertex(self, vertex: str):
        """
        Deletes a vertex. Deletes all edges O(V)
        """
        if vertex not in self.vertex:
           raise KeyError("Vertex not in set")
        else:
           self.edges = [tup for tup in self.edges if not vertex in tup]
           self.vertex.remove(vertex)

    def add_edge(self, edge: tuple):
        """
        Adds an edge. Checks whether there are vertexes in a graph, then inserts an additional edge.
        """
        # Check whether this is a tuple
        if type(edge) is tuple:
           a, b = edge
           if a not in self.vertex or b not in self.vertex:
              raise KeyError("Not in the list of verticies")
           self.edges.append(edge)
        else:
           raise TypeError(f"Bad Type: {edge} is", edge)


    def remove_edge(self, edge: tuple):
        """
        Removes an edge. Throws an error if there is no such edge.
        """
        self.edges.remove(edge)

    def to_Graph(self):
        """
        Simple Graph call since this interface is backwards compatible.
        """
        return Graph(self.vertex, self.edges)
        

    def to_GraphAdj(self):
        """
        Simple Graph call since this interface is backwards compatible.
        """
        return GraphAdj(self.vertex, self.edges)


newGraph = GraphEdge({'a', 'b'}, [('a', 'b',), ('a', 'b')], name = "Example")        
print(newGraph)
newGraph.add_vertex("z")
print(newGraph)
newGraph.add_edge(("b", "z"))
print(newGraph)
#newGraph.add_edge(("z", "y")) #errors out on purpose
newGraph.remove_edge(("a", "b"))
print(newGraph)
newGraph.remove_vertex("b")
# newGraph.remove_vertex("p") # key not in set
print(newGraph)
