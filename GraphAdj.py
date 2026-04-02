# required dep
import io
import numpy as np

class GraphAdj:
    """
    Directed Multigraph class. Uses adjacency matrix.
     
    CC Franciszek Moszczuk
    """

    
    def __init__(self, vertex: set = None, edges: list = None, name = "Unnamed", directed = True, 
                 array = None, vti = None, itv = None):
        """
        Uses tuples by default because the graph isn't the same after it's modified,
        therefore it makes sense to make edges a list of tuples

        WAYS OF ENTRY:
        1) Edge list constructor
        2) "Back entry" through the factory method (fromGraph, from_graph6)
        
        1)
        1. Sort the set (remains of the edge list graph) 
        2. Append numbers to vertex 
        # {a, c, 1, c, ...} --> {0: a, 1: c, } etc 
        TODO: BENCHMARK THIS
        # IndexToVertex === ITV
        # VertexToIndex === VTI
        3. Create matrix
       
        
        """
        # set basic params
        self.directed = directed
        self.name = name
        
        if array is None:
            # sort set
            # assumes only strings for now
            templist = sorted(vertex)
             
            # technically those two should be linked somehow but they arent
            # THIS SHOULD BE A SEPARATE CLASS!!! CAN AND WILL GET DESYNCED
            self.IndexToVertex = {}
            self.VertexToIndex = {}
            for index, key in enumerate(templist):
                self.IndexToVertex[index] = key
                self.VertexToIndex[key] = index

            # Deprecated
            #self.IndexToVertex = dict(enumerate(templist))
            #self.VertexToIndex = {v: k for k, v in self.IndexToVertex.items()}
            # create a numpy array of the size dict
            a = len(self.VertexToIndex)
            self.adjMatrix = np.zeros((a, a), dtype=np.int_)
            # convert each edge to adjacency matrix
            for u, v in edges:
                try:
                    self.adjMatrix[self.VertexToIndex[u], self.VertexToIndex[v]] += 1
                    if not self.directed and (u != v):
                        # avoids loop duplication 
                        self.adjMatrix[self.VertexToIndex[v], self.VertexToIndex[u]] += 1
                except KeyError:
                    print(f"Vertex {u} or {v} is missing from set, skipping")
        else: 
            self.adjMatrix = array
            self.VertexToIndex = vti
            self.IndexToVertex = itv
           

 
    def __str__(self):
        rtrnString = f"{'Directed' if self.directed else 'Undirected'}\
 Matrix Multigraph {self.name} with the following params:\
\nVertex: {self.IndexToVertex}\nMatrix: \n"
        # thanks Stackoverflow
        rtrnString += ',    '.join(key for key in self.VertexToIndex.keys())
        rtrnString += '\n'
        for row_label, row in zip(self.VertexToIndex.keys(), self.adjMatrix):
            rtrnString += '%s [%s]\n' % (row_label, ' '.join('%03s' % i for i in row))
        # this is probably why java has a string builder class (no wonder)
        return rtrnString

    def add_vertex(self, vertex: str):
        """
        Adds a vertex to the graph. Assumed a UTF-8 character (Python default).
           Resizes the numpy array.
           We're not bothering with resorting as you can't use bisect on a dictionary and
           no way I'm doing binary search (log2 overhead is still overhead)
        """
        # add two vertexes in both dicts, resize numpy
        if (vertex) in self.VertexToIndex:
           print(f"Vertex {vertex} already in set")
           return False     
        # probably should insert at last pos 
        lastIndex = len(self.VertexToIndex)
        self.IndexToVertex[lastIndex] = vertex
        self.VertexToIndex[vertex] = lastIndex
        self.adjMatrix = np.insert(self.adjMatrix, lastIndex, 0, axis=0)
        self.adjMatrix = np.insert(self.adjMatrix, lastIndex, 0, axis=1) 
        # entries are sorted
        
        # (add in lexical order)


    def remove_vertex(self, vertex: str):
        """
        Deletes a vertex. Drops col and row containing the vertex, 
           then updates the dicts by dropping the i -> v key first, then the i -> v()
        """

        # find the vertex (errors out if not found)
        pos = self.VertexToIndex[vertex]
        # modify in place
        self.adjMatrix = np.delete(self.adjMatrix, pos, 0)  # delete third row of B
        self.adjMatrix = np.delete(self.adjMatrix, pos, 1)  # delete third col of B
        # drop the dict keys, then reindex
        
        del self.VertexToIndex[vertex]
        del self.IndexToVertex[pos]
        

    def add_edge(self, edge: tuple):
        """
        Adds an edge. Checks whether the edge is valid, then inserts.
        """
        # Check whether this is a tuple
        if type(edge) is tuple:
           # the above should have own method for clarity but this will do
           a, b = edge
           if a not in self.VertexToIndex or b not in self.VertexToIndex:
              raise KeyError(f"{a} or {b} is not in the list of vertexes")
           c, d = self.VertexToIndex[a], self.VertexToIndex[b]
           self.adjMatrix[c, d] += 1
           if not self.directed:
              self.adjMatrix[d, c] += 1
        else:
           raise TypeError(f"Bad Type: Edge is a {edge}")


    def remove_edge(self, edge: tuple):
        """
        Removes an edge. Throws an error if there is no such edge or 
            there are no such edges (0).
        """
        #try:
        a, b  = edge
        c, d  = self.VertexToIndex[a], self.VertexToIndex[b]
        if (self.adjMatrix[c, d] > 0):
           self.adjMatrix[c, d] -= 1
           if not self.directed:
              self.adjMatrix[d, c] -= 1
        else:
              raise KeyError(f"Edge {edge} doesn't exist.")
        
       

    def count_nCycles(self, edge:tuple, n:int) -> int:
        """
        Count Cycles in a graph. Does matrix multiplication M^num.
        """
        # Slight error checking before an expensive $$$ operation
        a, b = edge
        if a not in self.VertexToIndex or b not in self.VertexToIndex:
            raise KeyError(f"{a} or {b} is not in the list of vertexes")
        c, d = self.VertexToIndex[a], self.VertexToIndex[b]
        
        # ^ this abcd appears in code 3 or four times... 
        # maybe create a private method?
        temp = np.linalg.matrix_power(self.adjMatrix, n);
        #print(temp)
        return temp[c, d]

    
    def get_deg(vertex: str)-> int:
        """
        Gets the degree of a vertex.
        """
        return NotImplemented



    def get_Annihilation(vertex: str)-> int:
        """
        Gets the annihilation number of a vertex.
        Uses get_deg.
        """

        return NotImplemented



    def to_Graph(self):
        """
        Creates a new list Graph based on the current Matrix.
        O(V^2)
        """
        # return a class by just calling the GraphAdj()
        # constructor (via a factory method)
        # this way we are keeping the classes isolated (parser for Graph
        # Adj is defined in the Graph (Adjecency) class as it should be)
        return Graph.from_GraphAdj(self.adjMatrix, self.IndexToVertex)
        

    @classmethod
    def from_Graph(cls, adjList: dict, name: str = ""):
        """ 
        Creates an adjacency matrix based on the adjacency list.
        O(V^2)
        """
        # create an empty matrix of ints
        a = len(adjList)
        adjMatrix = np.zeros((a, a), dtype=np.int_)
        # sort then assign itv and vti
        retrieve = sorted(adjList.keys())
        itv = {}
        vti = {}
        # This is faster by around 1/16 s for 1000 iteration
        # than the initial initialization method!
        for index, key in enumerate(retrieve):
            # populate each row 
            vti[key] = index
            itv[index] = key
                   
        #print(f"vti {vti}, itv {itv}")
        
        for key in retrieve:
            for val in adjList[key]:
                #print(vti[key], vti[val])
                adjMatrix[vti[key], vti[val]] += 1
        #TODO: replace with logging module
        #print(adjMatrix)
        return cls(array=adjMatrix, itv=itv, vti=vti)
        

    def to_graph6(self, path=""):
        """ If path is none returns a string, or writes to file
        the graph in EITHER g6 or d6 format based on whether the graph is
        directed or not."""
        if self.directed:
            res = self.__to_d6()
        else:
            res = self.__to_g6()
        
        return res



    @classmethod
    def from_graph6(cls, text: str = None, path=""):
        """ 
            Read graph6. 
            Yes, it imports a whole file to memory.
        """
        if path:
            # read from file
            raise NotImplementedError
        elif text:
            # TODO: strip header
            # if data.startswith(">>graph6<<")
            # read from a string with string buffer
            arr = np.frombuffer(bytes(text, encoding="ascii"), dtype=np.uint8)
            # if the first sign ISN'T 38 '&' -> d6
            first = arr[0]
            if first < 63:
               raise ValueError(f"Unknown format. {c} is smaller than 63, aborting...")
            elif first > 125:
               raise NotImplementedError("No way I'm implementing this...") 
            else:
                arr = arr - 63
                # N(n)
                n = arr[0]
                retArrd = np.zeros((n, n), dtype=np.int_)
                
                # R(x)
                # FUN FACT OF THE DAY!
                # Did you know that the graph6 spec is outright wrong?
                # The spec says to consider the upper triangle, while
                # LITERALLY listing the lower triangle in an example
                # and in an incomprehensible notation at that!
                # See more: 
                # https://stackoverflow.com/questions/44532492/how-does-graph6-format-work
                bits = np.unpackbits(arr[1:], bitorder='big') 
                print(bits)                

                
                # skip two first bits
                idx = 2
                for i in range(1, n):
                    # skip every 2 characters in front for every 6 characters read
                    for j in range(i):
                        #print((j, i), idx, bits[idx]) #UNCOMMENT FOR SPEC ORDER
                        retArrd[i, j] = bits[idx]
                        retArrd[j, i] = bits[idx]
                        idx += 1 
                        if (idx % 8 == 0):
                            #print("skipping pos", idx)
                            idx += 2
                            

                print(retArrd)
                # assign a default dict
                vti = {}
                itv = {}
                for i in range(n):
                    vti[i] = i;
                    itv[i] = i;
            return cls(array=retArrd, itv=itv, vti=vti)
        else:
            return NotImplemented
     

    @classmethod
    def from_digraph6(self, text: str = None, path=""):
        """ 
            Read digraph6. Yes it also imports a whole file to memory.
        """
        if path:
            # read from file
            raise NotImplementedError
        elif text is not None:
            arr = np.frombuffer(bytes(text, encoding="ascii"), dtype=np.uint8)
            # if the first sign ISN'T 38 '&' -> throw an error
            first = arr[0]
            if (first != 38):
                raise ValueError("Not a proper D6 graph, & missing...")
        else:
            raise NotImplemented


    """
    Are you looking at my privates or are you just happy to see me?
    """
    def __to_g6(self, path=""):
        """ Invoked when graph is undirected."""
        # we are using array's size just in case the helper
        # dicts go wrong
        size = self.adjMatrix.shape(0)
        for i in range(size):
            continue
        #return res


    def __to_d6(self, path=""):
        """ Invoked when graph is undirected."""
        return NotImplemented


    @staticmethod
    def __n_decode(n: int) -> int:
        """
        Helper private static method to help with n decoding.
        """
        if (n <= 125 and n >= 63):
            return n-63;
        elif ( n <= 258047):
            raise NotImplementedError("No way I'm implementing this")
        elif ( n <= 68719476735):
            raise NotImplementedError("No way I'm implementing this")
        else:
            raise ValueError("Invalid n value")
     
    @staticmethod
    def __n_encode(n: int) -> int:
        """
        Helper private static method to help with n encoding.
        """
        if (n <= 62 and n >= 0):
            return n+63;
        elif ( n <= 258047):
            raise NotImplementedError("No way I'm implementing this")
        elif ( n <= 68719476735):
            raise NotImplementedError("No way I'm implementing this")
        else:
            raise ValueError("Invalid n value")


# Directed tests
newGraph = GraphAdj({'a', 'b'}, [('a', 'b',), ('a', 'b')], name = "Example")        
print(newGraph)

newGraph = GraphAdj({'a', 'b', 'c', 'd'}, [('a', 'b',), ('a', 'b'), ('a', 'c'), ('a', 'd')], name = "Example")        
print(newGraph)

# should error out
newGraph = GraphAdj({'a', 'b', 'c'}, [('a', 'b',), ('a', 'b'), ('a', 'c'), ('a', 'd')], name = "Example")        
print(newGraph)

newGraph.add_vertex("z")
print(newGraph)

newGraph.add_edge(("b", "z"))
print(newGraph)


# Undirected tests

newGraph = GraphAdj({'a', 'b'}, [('a', 'b',), ('a', 'b')], name = "Example", directed=False)        
print(newGraph)
newGraph = GraphAdj({'a', 'b', 'c', 'd'}, [('a', 'b',), ('a', 'b'), ('a', 'c'), ('a', 'd')], name = "Example", directed=False)        
print(newGraph)

newGraph.add_vertex("z")
print(newGraph)

newGraph.add_edge(("b", "z"))
print(newGraph)

newGraph.remove_edge(("a", "b"))
print(newGraph)

newGraph.remove_vertex("b")
print(newGraph)

# At this point I should be using pytest...
# lecture example

M = GraphAdj({'a', 'b', 'c', 'd'}, [('a', 'b',), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('c', 'd')], name = "Lecture", directed=False)        
print(M)
assert M.count_nCycles(('a', 'c'), 2) == 2, "Should be 2"
assert M.count_nCycles(('a', 'c'), 3) == 5, "Should be 5"


# List test
#List = Graph({'a', 'b', 'c', 'd'}, [('a', 'b',), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('c', 'd')], name = "Conversion test")
#print(List)
#print(List.to_GraphAdj())

#newGraph.add_edge(("z", "y")) #errors out on purpose
#newGraph.remove_edge(("a", "b"))
#print(newGraph)
#newGraph.remove_vertex("b")
# newGraph.remove_vertex("p") # key not in set
# print(newGraph)


# GRAPH6 TEST
graph6 = GraphAdj.from_graph6("DQc")
