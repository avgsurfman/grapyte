# required dep
from functools import reduce

import re
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
        # TODO: Make this private.
        self.directed = directed
        self.name = name
        
        if array is None:
            # sort set
            # Assumes strings.
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
                except KeyError as err:
                    raise KeyError(f"Vertex {u} or {v} is missing from set: {vertex}") from err
        else: 
            self.adjMatrix = array
            self.VertexToIndex = vti
            self.IndexToVertex = itv
           


    """
    Overloaded "dunder" methods go here.
    """

 
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


    """
    Basic methods (adding, removing a vertex, edge...) 
    """


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
        
        size = self.adjMatrix.shape[0]
        for i in range(pos, size):
            # start with the offending position, look onto next,
            # swap, update the indicies
            # Omega(2*(V - pos))
            temp = self.IndexToVertex[i+1]
            self.VertexToIndex[temp] = i
            self.IndexToVertex[pos] = temp
            # delete the item with the wrong position ( should be done at the end)
        del self.IndexToVertex[size]
        

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
           raise TypeError(f"Bad Type: Edge is a {edge}! Expected a tuple...")


    def remove_edge(self, edge: tuple):
        """
        Removes an edge. Throws an error if there is no such edge or 
            there are no such edges (0).
        """
        a, b  = edge
        c, d  = self.VertexToIndex[a], self.VertexToIndex[b]
        if (self.adjMatrix[c, d] > 0):
           self.adjMatrix[c, d] -= 1
           if not self.directed:
              self.adjMatrix[d, c] -= 1
        else:
              raise KeyError(f"Edge {edge} doesn't exist.")
    


    """
    Cycle counting, n-Walks...
    """


 
    # TODO: this works for graphs, not sure about n-graphs
    # maybe check w the naive algorithm?
    #    
    def count_3Cycles(self) -> int:
        """
        Count 3-Cycles in a graph. Does matrix multiplication M^3.
        """
        # ngl not sure if this works
        temp = np.linalg.matrix_power(self.adjMatrix, 3);
        return np.trace(temp) // 6



    def count_nWalks(self, edge: tuple, n: int) -> int:
        """
        Count nWalks in a graph for a specific edge. Does matrix multiplication M^n.
        Previously (incorrectly) called count_nCycles.
        """
        a, b = edge
        if a not in self.VertexToIndex or b not in self.VertexToIndex:
            raise KeyError(f"{a} or {b} is not in the list of vertexes")
        c, d = self.VertexToIndex[a], self.VertexToIndex[b]
        # ^ this abcd validation appears in code 3 or four times, 
        # should be its own setter 
        temp = np.linalg.matrix_power(self.adjMatrix, n);
        return temp[c, d]


    def count_edges(self)-> int:
        """
        Gets the amount of edges in a graph.
        """
        if self.directed:
            return self.adjMatrix.sum()
        else:
            return self.adjMatrix.sum() // 2

    def count_vertexes(self)-> int:
        """
        Returns the amount # of vertex in a graph.
        """
        return self.adjMatrix.shape(0)
        

    def get_deg(self, vertex: str | int)-> int:
        """
        Gets the degree deg(v) of a vertex.
        Also is the reason why we require Python 3.10+.
        https://peps.python.org/pep-0604/
        """
        # Loops v -> v are counted twice, 
        # therefore 2*a+b+c... = sum(row) + a
        if isinstance(vertex, str): 
            pos = self.VertexToIndex[vertex]
            return self.adjMatrix[pos].sum() + self.adjMatrix[pos, pos] 
        elif isinstance(vertex, int):
            return self.adjMatrix[vertex].sum()
        else:
            raise TypeError(f"get_deg requires an int | str, not {type(vertex)}") 
    

    #def get_max_deg_numpy(self) -> int:
    #    """
    #    Returns the maximum degree of a graph, s.t.
    #    ∆(G) = max{deg(v) | v ∈ V (G)}
    #    SOMEHOW SLOWER THAN THE PYTHON METHOD! WTF
    #    """
    #    # again this should be its own function
    #    degs = np.fromiter((self.get_deg(v) for v in self.VertexToIndex.keys()), 
    #                       dtype=int)
    #    return int(np.max(degs))
         
         
    def get_max_deg(self) -> int:
        """
        Returns the maximum degree of a graph, s.t.
        ∆(G) = max{deg(v) | v ∈ V (G)}
        """
        # again this should be its own function
        degs = sorted([self.get_deg(v) for v in self.VertexToIndex.keys()])
        return max(degs)


    def get_min_deg(self) -> int:
    
        """
        Returns the minimum degree of a graph, s.t.
        δ(G) = min{deg(v) | v ∈ V (G)}
        """
        # again this should be its own function
        degs = sorted([self.get_deg(v) for v in self.VertexToIndex.keys()])
        return min(degs)


    def get_annihilation(self)-> int:
        """
        Gets the annihilation number of a Graph.
        Uses get_deg.
        """
        #todo: replace with numpy cumsum
        degs = sorted([self.get_deg(v) for v in self.VertexToIndex.keys()])
        edges = self.count_edges() # not using the "handshake" lemma as
        # our graphs can be both directed and undirected.
        d_sum = 0
        i = 0 
        while (d_sum <= edges):
            d_sum += degs[i] 
            i += 1
        return i - 1
        """
        The only AI-gen piece of code but then again
        AI can only steal 
        I suppose the code for this is in NetworkX     
        
        degs = np.sort(self.adjMatrix.sum(axis=1) + np.diag(self.adjMatrix))
        edges = self.count_edges()
        return int(np.searchsorted(np.cumsum(degs), edges, side='right'))
        """

    """
    🏭️ FACTORY METHODS
    """

    def to_Graph(self):
        """
        Creates a new list Graph based on the current Matrix.
        O(V^2)
        """
        # return a class by just calling the GraphAdj()
        # constructor (via a factory method)
        # this way we are keeping the classes isolated and self-referencing
        # https://stackoverflow.com/questions/744373/what-happens-when-using-mutual-or-circular-cyclic-imports
        import grapyte.Graph as Graph
        return Graph.from_GraphAdj(self.adjMatrix, self.IndexToVertex,
                                   self.VertexToIndex, self.directed)
        

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
        
    """
    GRAPH6/DIGRAPH6 Parsing
    """


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
    def from_graph6(cls, data: str | bytes = None, path="") -> np.ndarray:
        """ 
            Read graph6. 
            Yes, it imports a whole file to memory.
            path replaces data if present.
        """
        if path:
            # read from file
            raise NotImplementedError
        elif data:
             """
             Community fix by Fred Bill on Stackoverflow. Thanks!
             """
             if isinstance(data, str):
                 data = data.encode("ascii")
             # not technically needed
             #data = data.rstrip(b"\n")
             if data.startswith(b">>graph6<<"):
                 data = data[10:]

             raw = np.frombuffer(data, dtype=np.uint8)
             if raw.size == 0 or np.any((raw < 63) | (raw > 126)):
                 raise ValueError("invalid graph6 data")
             raw = raw - 63
             # cls hack and validation
             n, offset = cls.__decode_graph6_n(raw)
             m = n * (n - 1) // 2  # number of edges in the upper triangle of the adjacency matrix
             nd = (m + 5) // 6  # i.e. ceil(m / 6)
             if raw.size != offset + nd:
                 raise ValueError("invalid graph6 data")
                  
             # bit array hacks
             payload = raw[offset:]
             print(payload)
             bits = np.unpackbits(payload[:, np.newaxis], axis=1, bitorder="big")
             print(f"unpack bits: {bits}")
             bits = bits[:, 2:].ravel()[:m]  # skip the first 2 bits of each 8 bits and then flatten
             print(f"bit skip: {bits}")

             # uint8, this is bound to cause problems...
             A = np.zeros((n, n), dtype=np.uint8)
             j, i = np.tril_indices(n, k=-1)  # i: 0,0,1,0,1,2,0,1,2,3,...; j: 1,2,2,3,3,3,4,4,4,4...
             A[i, j] = bits
             A[j, i] = bits
             # assign a default dict
             vti = {}
             itv = {}
             for i in range(n):
                 # cache the lookup, as adviced by jerome richard
                 lookup = str(i)
                 vti[lookup] = i;
                 itv[i] = lookup;
             return cls(array=A, itv=itv, vti=vti, directed=False)
        else:
            return NotImplemented
     

    @classmethod
    def from_digraph6(cls, data: str | bytes = None, path="") -> np.ndarray:
        """ 
            Read digraph6. Yes it also imports a whole file to memory.
            TODO: OPTIMIZE THIS!!!
        """
        if path:
            # read from file
            raise NotImplementedError
        elif data is not None:
            if isinstance(data, str):
                data = data.encode("ascii")
            data = data.rstrip(b"\n")
            if data.startswith(b">>digraph6<<"):
                data = data[12:]

            arr = np.frombuffer(data, dtype=np.uint8)
            # if the first sign ISN'T 38 '&' -> throw an error
            first = arr[0]
            second = arr[1]
            if (first != 38):
                raise ValueError("Not a proper d6 digraph, & missing...")
            # TODO: rewrite!
            if second < 63:
                raise ValueError(f"Unknown format. {c} is smaller than 63, aborting...")
            elif second > 125:
                raise NotImplementedError("No way I'm implementing this...") 
            else:
                # N(n)
                arr = arr - 63
                # TODO:get dimensions from the helper function
                n = arr[1]
                retArrd = np.zeros((n, n), dtype=np.int_)
                
                # R(x)
                # again technically we would be better off writing our own numpy
                # extension because all of the functions just suck and can't avoid 
                # adding padding
                # A C extension would be nice
                bits = np.unpackbits(arr[2:], bitorder='big') 
                 
                # TODO: replace with np indicies 
                idx = 2
                for i in range(n):
                    # skip every 2 characters in front for every 6 characters read
                    for j in range(n):
                        retArrd[i, j] = bits[idx]
                        idx += 1 
                        if (idx % 8 == 0):
                            #print("skipping pos", idx)
                            idx += 2

                
                vti = {}
                itv = {}
                for i in range(n):
                    lookup = str(i)
                    vti[lookup] = i
                    itv[i] = lookup
            return cls(array=retArrd, itv=itv, vti=vti, directed=True)

        else:
            raise NotImplementedError("Not implemented")


    @classmethod 
    def from_dimacs(cls, data: str = None, path="") -> np.ndarray:
        """
        Reads the DIMACS graph format.
        Reads from path file first if present.
        Path can be either a system path or a fd.
        If both data and path are entry, throws a ValueError.
        """
        def read_fd(fd):
            """
            Helper routine that parses fd and pseuso-fd objects (stringio).
            More Info:
            https://lcs.ios.ac.cn/~caisw/Resource/about_DIMACS_graph_format.txt
            """


            # init the finite state machine states:
            # start => 0 
            # comment line => 1 (c)
            # problem line => 2 (p)
            # edge_line => 3    (e)
            # entered can be seen as a factored out Moore FSM
            # that just remembers whether a p line has occured
            state = 0    
            entered_problem = 0          
  
            """
            Some preface is needed for this section:
            1) Single letters (tokens) denote detectors.
            2) This is a Mealy FSM, meaning the state and the inputs affect
            the state.
            3) This is a minimal DIMACS 2nd ed parse. x parameter description 
            and v params are not supported, as I don't know how to draw graphs in GUI.
            This also isn't 1st ed, 3rd ed or any other ed as the multigraph 
            class doesn't support weighted edges, or nodes (n ID param).
 
            Grammar for each regex:
            - comment line is accepting the words: *c*. In other words,
            comments can appear anywhere in the file.
            - problem line is accepting words: !entered_problem & problem_line
            - edge line is accepting words: p & edge_line OR e & edge_line
            - Every other sequence gets an error
            
            # finish on file end on edge line or comment; 
            # if not in acceptor state, throw 
            # if the edges perl re capture doesn't match, also throw
            """
            comment_detector = re.compile("^c( |$)")
            problem_detector = re.compile("^p edge (?P<n>[0-9]+) (?P<edges>[0-9]+)")
            edge_detector = re.compile("^e (?P<u>[0-9]+) (?P<v>[0-9]+)")
            
            # Graph variables
            n = 0
            edges = 0
            edges_cnt = 0
            matrix = None
            # always_ff@(posedge line) 

            for line in fd:
                # always_comb
                if comment_detector.match(line):
                    state = 1
                elif (res := problem_detector.match(line)) and not entered_problem:
                    state = 2 
                    n = int(res['n']) 
                    edges = int(res['edges'])
                    # initialize the numpy array at this point
                    matrix = np.zeros((n, n), dtype=np.int_)
                elif (res := edge_detector.match(line)) and state:
                    u = int(res['u']) - 1
                    v = int(res['v']) - 1
                    # Multigraphs bby
                    matrix[u, v] += 1
                    matrix[v, u] += 1
                    edges_cnt += 1
                else:
                    raise ValueError(f"[DIMACS 2nd Parser] Unacceptable line: {line}")
            # validation segment
            if not len(matrix):
               raise TypeError("[DIMACS 2nd Parser] Matrix is 'None'.")
            elif edges != edges_cnt:
               raise ValueError(f"[DIMACS 2nd Parser] Edges count mismatch!\
\nPlease check the source file. \nEdges, edges_cnt: {edges, edges_cnt}")
                                       
            else:
               return matrix, n


        if path:
            with open(path, encoding="ascii") as fd:
                retArrd, n = read_fd(fd)
                vti = {}
                itv = {}
                for i in range(n):
                    lookup = str(i)
                    vti[lookup] = i
                    itv[i] = lookup
                return cls(array=retArrd, itv=itv, vti=vti, directed=False)
        elif data:
            # convert data to a io stringio
            string_buffer = io.StringIO(data)
            retArrd,n  = read_fd(string_buffer)
            vti = {}
            itv = {}
            for i in range(n):
                lookup = str(i)
                vti[lookup] = i
                itv[i] = lookup
            return cls(array=retArrd, itv=itv, vti=vti, directed=False)
        else:
            raise ValueError("[DIMACS 2nd Parser] No arguments were provided.")


    """
    Are you looking at my privates or are you just happy to see me?
    """
    def __to_g6(self, path=""):
        """ Invoked when graph is undirected."""
        # we are using array's size just in case the helper
        # dicts go wrong
        size = self.adjMatrix.shape(0)
        # tril indicies to iterate over the upper matrix
        # append the 126 bytes if the array is large enough
        # Encode size, flatten the array
        # 
        # validate if np.any isn't greater than 1
        
        # also we need a fast string buffer method

        
        for i in range(size):
            continue
        #return res


    def __to_d6(self, path=""):
        """ Invoked when graph is undirected."""
        size = self.adjMatrix.shape(0)
        # prepare the numpy array prepending 38 and N(n)
        # temp = np.
        # apply __nencode on each term temp[1:]
        # Convert to string
        return NotImplemented


    @staticmethod 
    def __decode_graph6_n(raw: np.ndarray) -> tuple[int, int]:
        """
        Helper private static method to help with n decoding.
        """
        func = lambda accumulator, byte: (accumulator << 6) | int(byte)
        if raw[0] <= 62:
            return int(raw[0]), 1
        # single 126(~) w/ 3 graph6 chars (18b) 
        elif raw.size >= 4 and raw[1] <= 62:
            return reduce(func, raw[1:4], 0), 4
	# double 126(~) w/ 6 graph6 chars (36b) 
        elif raw.size >= 8:
            return reduce(func, raw[2:8], 0), 8
        raise ValueError("invalid graph6 data")
      
    #@staticmethod
    #def __encode_graph6_n() -> np.ndarray
    #    """ 
    #    TODO
    #    """
    #    func = 
    
    #@staticmethod
    #def __n_decode(n: int) -> int:
    #    if (n <= 125 and n >= 63):
    #        return n-63;
    #    elif ( n <= 258047):
    #        raise NotImplementedError("No way I'm implementing this")
    #    elif ( n <= 68719476735):
    #        raise NotImplementedError("No way I'm implementing this")
    #    else:
    #        raise ValueError("Invalid n value")
    # 
    #@staticmethod
    #def __n_encode(n: int) -> int:
    #    """
    #    Helper private static method to help with n encoding.
    #    Currently not used.
    #    """
    #    if (n <= 62 and n >= 0):
    #        return n+63;
    #    elif ( n <= 258047):
    #        # single 126 w/ 3 graph6 chars (18b) 
    #        raise NotImplementedError("No way I'm implementing this")
    #    elif ( n <= 68719476735):
    #        # double 126 w/ 6 graph6 chars (36b) 
    #        raise NotImplementedError("No way I'm implementing this")
    #    else:
    #        raise ValueError("Invalid n value")


"""
 (The) Finest selection of tests 
 Usage examples
"""

# Directed tests

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

# Undirected tests

#newGraph = GraphAdj({'a', 'b'}, [('a', 'b',), ('a', 'b')], name = "Example", directed=False)        
#print(newGraph)
#newGraph = GraphAdj({'a', 'b', 'c', 'd'}, [('a', 'b',), ('a', 'b'), ('a', 'c'), ('a', 'd')], name = "Example", directed=False)        
#print(newGraph)
#
#newGraph.add_vertex("z")
#print(newGraph)
#
#newGraph.add_edge(("b", "z"))
#print(newGraph)
#
#newGraph.remove_edge(("a", "b"))
#print(newGraph)
#
#newGraph.remove_vertex("b")
#print(newGraph)

# At this point I should be using pytest...
# lecture example

#M = GraphAdj({'a', 'b', 'c', 'd'}, [('a', 'b',), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('c', 'd')], name = "Lecture", directed=False)        
#print(M)
#assert M.count_nWalks(('a', 'c'), 2) == 2, "Should be 2"
#assert M.count_nWalks(('a', 'c'), 3) == 5, "Should be 5"
#print(f"M 3-Cycles: {M.count_3Cycles()}")


# List test
#List = Graph({'a', 'b', 'c', 'd'}, [('a', 'b',), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('c', 'd')], name = "Conversion test")
#print(List)
#print(List.to_GraphAdj())


# Error testing
#newGraph.add_edge(("z", "y")) #errors out on purpose
#newGraph.remove_edge(("a", "b"))
#print(newGraph)
#newGraph.remove_vertex("b")
# newGraph.remove_vertex("p") # key not in set
# print(newGraph)


# GRAPH6 TEST
graph6 = GraphAdj.from_graph6("DQc")
diff = GraphAdj.from_graph6("G}l~~{")
print(diff)

# DIGRAPH6 Test

digraph6 = GraphAdj.from_digraph6("&DI?AO?")
print(digraph6)
# required dep
