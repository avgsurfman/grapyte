# CC Franciszek Moszczuk 2026

import numpy as np
import random
import grapyte.GraphAdj as GraphAdj

class SimpleGraphAdj(GraphAdj):
    """
    Simple Matrix-based Unlooped, Undirected/directed graphs.
    Should be called a SG (akin to Directed Acyclic Graph).
    """
    
    def __init__(self, vertex: set = None, edges: list = None, name = "Unnamed", 
                 array = None, vti = None, itv = None, directed = False):
        
        # directed has to be featured because SGA inherits the cls method
        # which also means it should be overridden and
        # I am not rewriting that fucking class method 
        self.directed = False #cockblock
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

            # create a numpy array of the size dict
            a = len(self.VertexToIndex)
            self.adjMatrix = np.zeros((a, a), dtype=np.int_)
            # convert each edge to adjacency matrix
            for u, v in edges:
                try:
                    if (u != v):
                        # avoids loops
                        self.adjMatrix[self.VertexToIndex[v], self.VertexToIndex[u]] += 1
                        self.adjMatrix[self.VertexToIndex[u], self.VertexToIndex[v]] += 1
                    else: 
                        print(f"Loop detected, skipping...")
                except KeyError as err:
                    raise KeyError(f"Vertex {u} or {v} is missing from set: {vertex}") from err
        else: 
            #TODO: typecheck the array.
            self.adjMatrix = array
            self.VertexToIndex = vti
            self.IndexToVertex = itv
           
        # TODO: Override some methods that are faster for simple graphs.


    """
    Overloaded methods.
    """

    def add_edge(self, edge: tuple):
        """
        Adds an edge. Checks whether the edge is valid, then inserts.
        Does not allow duplicate edges.
        """
        # Check whether this is a tuple
        if type(edge) is tuple:
           # the above should have own method for clarity but this will do
           a, b = edge
           if a not in self.VertexToIndex or b not in self.VertexToIndex:
              raise KeyError(f"{a} or {b} is not in the list of vertexes")
           # check for duplicates
           c, d = self.VertexToIndex[a], self.VertexToIndex[b]
           if self.adjMatrix[c, d] >= 1:
              raise ValueError(f"Duplicate edge: {c, d} or {d, c}")
           else:
              #if not self.directed:
              self.adjMatrix[c, d] += 1
              self.adjMatrix[d, c] += 1
        else:
           raise TypeError(f"Bad Type: Edge is a {edge}! Expected a tuple...")

         
    

    def get_annihilation(self)-> int:
        """
        Gets the annihilation number of a Graph.
        Uses get_deg and the handshaking lemma.
        TODO: use the handshake lemma
        """
        #todo: replace with numpy cumsum
        degs = sorted([self.get_deg(v) for v in self.VertexToIndex.keys()])
        edges = self.count_edges() # TODO: use the handshake lemma
        d_sum = 0
        i = 0 
        while (d_sum <= edges):
            d_sum += degs[i] 
            i += 1
        return i - 1
        """
        The only AI-gen piece of code but then again
        AI can only steal, therefore 
        I suppose the code for this is in NetworkX     
        
        degs = np.sort(self.adjMatrix.sum(axis=1) + np.diag(self.adjMatrix))
        edges = self.count_edges()
        return int(np.searchsorted(np.cumsum(degs), edges, side='right'))
        """

    def get_deg(self, vertex: str)-> int:
        """
        Gets the degree deg(v) of a vertex.
        """
        # Loops v -> v are counted twice, 2*a+b+c... = sum(row) + a
        # Simple graphs don't have loops idiot 
        pos = self.VertexToIndex[vertex]
        return self.adjMatrix[pos].sum() 


    def get_H(self) -> int:
        """
        Return the H index, the inverse of potential.
        """
    
    def get_P(self) -> int:
        """
        Return the Potential of the graph P(G).

        Usecase:
           P(G) + 1 is a good upper bound approximation of the chromatic number.
        """
        
        degs = sorted([self.get_p(v) for v in self.IndexToVertex])
        return max(degs)
            

     
    def get_p(self, vertex) -> int:
        """
        Return the potential of a vertex p(v). 
        """
        i = self.VertexToIndex(vertex)
        # neighbors : apply a function s.t:
        # f(x) { sum(j) if arr[i][j] = 1
        #      { null  otherwise
        # then, to get potential, apply f(x) to the whole matrix, then
        # p(v) = k where k is the number of increments
        # neighbors = np.fromiter(self.itv f)
        iterable =  (self.adjMatrix[j].sum() for j in self.adjMatrix[i] if j > 0)
        neighbors = sorted(np.array(fromiter(iterable), int)) 
        max_p = 1
        neighbor_max = neighbors[0]

        for neighbor in neighbors:
            if neighbor > neighbor_max:
                max_p += 1
                neighbor_max = neighbor
        
        return max_p
                
    """
    Coloring
    """    
 
    def color_greedy(self, init_list = None) -> int:
        """
        Returns approximation of the chromatic number using the greedy algorithm.
        Also known as Random Sequential.
        c is bounded by the Grundy number.

        More info: 
        https://people.cs.uchicago.edu/~laci/HANDOUTS/greedycoloring.pdf
        """
        # alf
                       
        #ran[V
        
        # color(num# vertex) -> int
        coloring = dict() 
        if not init_list: 
            # shuffle indexes (improves coloring a bit)
            # pi -> {v2, v4, ...} [Borowiecki]
            rand_list = list(self.IndexToVertex)
            random.shuffle(rand_list)
        else:
            # Initialization list. Not type-checked.
            rand_list = init_list
        print(f"Randlist: {rand_list}")

        # Initial coloring num
        c = 0
        for v in rand_list:
            adj_colors = []
            # numpy iterator for convenience (external_loop doesn't work)
            neighbors = np.nditer(self.adjMatrix[v], flags=['f_index'])
            for neighbor in neighbors:
                # an edge actually exists
                if neighbor > 0:
                   # 1) neighbor is colored
                   print(f"Found an edge! {neighbors.index}")
                   if neighbors.index in coloring:
                      adj_colors.append(coloring[neighbors.index])
                       
                   # 2) else neighbor is uncolored
                   # (Do nothing)
            
            k = 0
            # slow, probably can be improved
            while k in adj_colors:
                k += 1
            coloring[v] = k
            if k > c:
               c = k
            print(coloring) 
        # reindexing as colors go from 0 to χ-1
        return c+1

        #Calling convention: either G.color_greedy() or G.color_RS(), same thing.
    color_RS = color_greedy



    def color_greedy_exp(self) -> int:
        """
        Experimental Greedy variation, backtraces one layer back to color
        the vertex.
        """
        
        coloring = dict()
        bucket = random.shuffle(list(self.IndexToVertex))
        
        c = 0 
        # if there's uncolored vertex v in G
        while item in bucket:
            # row_wise
            neighbors = np.nditer(self.adjMatrix[item], flags=['multi_index'])
            for neighbors in self.adjMatrix[item]:
                # column_wise
                for neighbor in neighbors:
                    continue
                    # copy the coloring code.
                     
        #     for every u adj to v
        #         for every z adj to u
        #             color u
        #     color v
        # skip colored (empty bucket -> remove colored from set)
        return c


    def color_LF(self) -> int:
        """
        Returns the Largest-first coloring approximation of the chromatic number.
        Essentially greedy but with some ordering.
        """ 
        return NotImplemented
         

    def color_SL(self) -> int:
        """
        Returns the Smallest Last coloring approximation of the chromatic number.
        """
        return NotImplemented


    def color_SLF(self) -> int:
        """
        Brélaz (1979) DSATUR algorithm.
        https://doi.org/10.1145%2F359094.359101
        """
        return NotImplemented
    color_DSTATUR = color_SLF
   
    
    """
    AAAAAAH Search Algorithms.
    TODO: Implement for both adj and list.
    """

    def search_DFS(self) -> list:
        """
        DFS  
        """
        search_stack = []
         
        def search():
            pass
        return NotImplemented 
