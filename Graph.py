import time

class Graph:
    """
    (Un) Directed Multigraph class. Uses adjacency lists by default.
     
    CC Franciszek Moszczuk & Karol Madraszek
    """

    
    def __init__(self, vertex: set, edges: list, name = "Unnamed", directed = True):
        """
        Uses tuples by default because the graph isn't the same after it's modified,
        therefore it makes sense to make edges a list of tuples
        """
        # adjacency 
        self.directed = directed
        self.name = name
        # sort set
        # assumes only strings for now
        templist = sorted(vertex)
        
        # as it is the case in the adjacency matrix I need a 
        # f(X): int -> vertex 
        #self.IndexToVertex = dict(enumerate(templist))
        self.vertex = vertex
        
        # self.adjList: 
        # f(X): dict<int> -> list<tuple>
        # maybe change this to str? no need to vti
        self.adjList = {}
        for i in range(len(templist)):
            self.adjList[templist[i]] = []
        print(self.adjList)
            
        for u, v in edges:
            if u not in self.vertex or v not in self.vertex:
               print(f"{u} or {v} not in set, skipping...")
            else:
               self.adjList[u].append(v)
               if not self.directed:
                   self.adjList[v].append(u)
        
        print(self.adjList)
 
    def __str__(self):
        return f"Multigraph {self.name} with the following params:\n \
               Vertex: {self.vertex}, Adjacency list: {self.adjList}"

    def add_vertex(self, vertex: str):
        """
        Adds a vertex to the graph. Assumed a UTF-8 character (Python default)
        """
        # make sure it's really a string? 
        if vertex not in self.vertex:
           self.adjList[vertex] = []
           self.vertex.add(vertex)
        else:
           print(f"Vertex {vertex} already in graph!")
              

    def remove_vertex(self, vertex: str):
        """
        Deletes a vertex. Deletes all edges O(V) for undirected and O(V²)
        for indirected graphs.
        """
        if vertex not in self.vertex:
           raise KeyError("Vertex not in set")
        else:
           if self.directed:
              # unfortunately we have to traverse the entire list to check
              # for references
              t1 = time.perf_counter_ns()
              # a simple loop takes only 3-5us - list comp about 5-7 us
              for key in self.adjList:
                  for v in self.adjList[key]:
                      if (v == vertex):
                          self.adjList[key].remove(v)
                  #self.adjList[key] = [v for v in self.adjList[key] if v != vertex]
                  #print(temp)
              t2 = time.perf_counter_ns()
              print(f"time:", t2 - t1)
                      
              del self.adjList[vertex]
           else:
               #loop through all of the edges (u, v) to remove edges from
               # all adjacent vertex v, then remove the final dict
               # this way we are not iterating over the object we are modifying
               # keeping this linear (O(V))
               for u in self.adjList[vertex]:
                   # reverse lookup
                   self.adjList[u].remove(vertex)
               del self.adjList[vertex]
         
        self.vertex.remove(vertex)

    def add_edge(self, edge: tuple):
        """
        Adds an edge. Checks whether there are vertexes in a graph, then inserts an additional edge.
        """
        # Check whether this is a tuple
        if type(edge) is tuple:
            a, b = edge
            if a not in self.vertex or b not in self.vertex:
                raise KeyError(f"{a} or {b} not in the list of verticies")
            self.adjList[a].append(b)
            if not self.directed:
                self.adjList[b].append(a)
        
        else:
           raise TypeError(f"Bad Type: {edge} is", edge)


    def remove_edge(self, edge: tuple):
        """
        Removes an edge. Throws an error if there is no such edge.
        """
        a, b = edge
        self.adjList[a].remove(b)
        if not self.directed:
            self.adjList[b].remove(a)

    def to_GraphAdj(self):
        """
        Either print out an adjecency matrix or create a new graph. 
        """
        # return a class by just calling the GraphAdj()
        # constructor (via a factory method)
        # this way we are keeping the classes isolated (parser for Graph
        # Adj is elsewhere as it should)
        return GraphAdj.from_Graph(self.adjList)
        
    @classmethod
    def from_GraphAdj(cls, matrix, itv):
    """ Creates an adjacency list based on the numpy array
    and the ITV matrix. 
    """
        return NotImplemented


    def to_graph6(self, path=""):
        """ If path is none returns a string, or writes to file
        the graph in graph6 format"""

        return NotImplemented


    @classmethod
    def from_graph6(self):
        """ Alternative constructor for reading graph6."""
        return NotImplemented
     

    


# directed
newGraph = Graph({'a', 'b'}, [('a', 'b',), ('a', 'b')], name = "Example")        
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
