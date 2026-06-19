import numpy as np
import time

from grapyte.utils.GraphError import GraphError

class Graph:
    """
    (Un) Directed Multigraph class. Uses adjacency lists.
     
    CC Franciszek Moszczuk & Karol Madraszek
    """

    
    def __init__(self,
                 vertex: set | list,
                 edges: list[tuple[str,str]] | list[tuple[int, int]] = [],
                 name = "Unnamed", directed = True, adjList = None):
        """
        Uses tuples by default because of their immutability,
        and also because that was the first implementation.
        """
        # TODO: make this private
        self.directed = directed
        self.name = name

        # validate set S
        templist = []
        for item in vertex:
            if not isinstance(item, str):
                templist.append(str(item))
            else:
                templist.append(item)
        self.vertex = set(templist)

        # self.adjList: 
        # f(X): dict<str> -> list<str>
        # honestly this would be much better in TypeScript
        if not adjList:
            self.adjList = {}
            for i in range(len(templist)):
                self.adjList[templist[i]] = []
            for u, v in edges:
                if not isinstance(u, str):
                    u = str(u)
                if not isinstance(v, str):
                    v = str(v)
                # easily subgraph a graph
                if u not in self.vertex or v not in self.vertex:
                   print(f"{u} or {v} not in set, skipping...")
                else:
                   self.adjList[u].append(v)
                   if not self.directed:
                       self.adjList[v].append(u)
        else:
           # YOLO no type checking
           self.adjList = adjList  
        
        # todo: maybe add logging?
        #print(self.adjList)
 

    def __str__(self):
        return f"Multigraph {self.name} with the following params:\nVertex:\
{self.vertex}, Adjacency list: {self.adjList}"


    def add_vertex(self, vertex: str | int):
        """
        Adds a vertex to the graph. Assumed a UTF-8 character (Python default)
        """
        if not isinstance(vertex, str):
            vertex = str(vertex)

        if vertex not in self.vertex:
            self.adjList[vertex] = []
            self.vertex.add(vertex)
        else:
           print(f"Vertex {vertex} already in graph!")
              

    def remove_vertex(self, vertex: str | int):
        """
        Deletes a vertex. Deletes all edges O(V) for undirected and O(V²)
        for indirected graphs.
        """
        if not isinstance(vertex, str):
            vertex = str(vertex)

        if vertex not in self.vertex:
           raise KeyError("Vertex not in set")
        else:
           if self.directed:
              # unfortunately we have to traverse the entire list to check
              # for references O(V*E[V] time)
              # t1 = time.perf_counter_ns()
              # update_dict = {}
              for key in self.adjList:
                  # I fucking hate this but it has to stay, I think.
                  # 2 us slower than the original but also 4 faster than reverse iter
                  # Method 1
                  self.adjList[key] = [v for v in self.adjList[key] if v != vertex]
                  """ Previous methods:
                  #Method 2 ( loud buzzer incorrect)
                  neighbors  = self.adjList[key] # pocket reference
                  for v in neighbors:
                      if (v == vertex):
                          self.adjList[key].remove(v) 
                  #Method 3
                  for i in range(len(neighbors) -1, -1, -1):
                      if neighbors[i] == vertex:
                          del neighbors[i]
                  """
              # t2 = time.perf_counter_ns()
              # print(f"time:", t2 - t1)
                      
              del self.adjList[vertex]
           else:
               #loop through all of the edges (u, v) to remove edges from
               # all adjacent vertexes v, then remove the final dict
               # this way we are only iterating over a single list,
               # keeping this linear, O(E[V])
               for u in self.adjList[vertex]:
                   # reverse lookup
                   self.adjList[u].remove(vertex)
               del self.adjList[vertex]
         
        self.vertex.remove(vertex)


    def add_edge(self, edge: tuple[str, str] | tuple[int, int]):
        """
        Adds an edge. Checks whether there are vertexes in a graph, then inserts an additional edge.
        """
        # Check whether this is a tuple
        if type(edge) is tuple:
            a, b = edge
            if not isinstance(a, str):
                a = str(a)
            if not isinstance(b, str):
                b = str(b)
            if a not in self.vertex or b not in self.vertex:
                raise KeyError(f"{a} or {b} not in the list of verticies")
            self.adjList[a].append(b)
            if not self.directed:
                self.adjList[b].append(a)
        
        else:
           raise TypeError(f"Bad Type: {edge} is", type(edge))


    def remove_edge(self, edge: tuple[str, str] | tuple[int, int]):
        """
        Removes an edge. Throws an error if there is no such edge.
        """
        a, b = edge
        if type(edge) is tuple:
            a, b = edge
            if not isinstance(a, str):
                a = str(a)
            if not isinstance(b, str):
                b = str(b)
        try:
            self.adjList[a].remove(b)
        except KeyError:
            raise KeyError(f"The vertex {a} or {b} you are refering to is not"
                           f"in the adjacency list.")
        except ValueError:
            raise KeyError(f"No such edge! {edge}") from None
        try:
            if not self.directed:
                self.adjList[b].remove(a)
        except ValueError as err:
            fail_msg = (f"If you are reading this, "
                        f"chances are you corrupted your Adjacency List.\n"
                        f"Good luck.\n"
                        f"Edges that caused the exception: {edge}\n"
                        f"Vertex Set: {self.vertex}\n"
                        f"Adj. List: {self.adjList}\n"
                        f"Directed: {self.directed}")

            raise GraphError(fail_msg) from err



    def to_GraphAdj(self):
        """
        Convert the Graph into GraphAdj.
        """
        # return a class by just calling the GraphAdj()
        # constructor (via a factory method)
        
        import grapyte.GraphAdj as GraphAdj
        return GraphAdj.from_Graph(self.adjList, self.name)
        

    @classmethod
    def from_GraphAdj(cls, matrix, itv, vti, directed):
        """ Creates an adjacency list based on the numpy array
        and the ITV matrix. 
        """
        
        vertex = set(vti.keys())
        print(vertex)
        adjList = {}
        # create a numpy iterator
        it = np.nditer(matrix, flags=['multi_index'])
        
        for x in it:
            u, v = it.multi_index
            #print("%d <%s>, u=%s v=%s " % (x, it.multi_index, u , v), end=' \n')
            for i in range(x):
                if itv[u] not in adjList:
                    adjList[itv[u]] = []
                adjList[itv[u]].append(itv[v])
        return cls(vertex, directed=directed, adjList=adjList)


    def to_graph6(self, path=""):
        """ If path is none returns a string, or writes to file
        the graph in graph6 format"""

        raise NotImplementedError("Please convert to AdjMatrix to read/write graph6.")


    @classmethod
    def from_graph6(self):
        """ Alternative constructor for reading graph6."""

        raise NotImplementedError("Please convert to AdjMatrix to read/write graph6.")
     



