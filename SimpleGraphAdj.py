class SimpleGraphAdj(GraphAdj):
    """
    Simple Matrix-based Unlooped, Undirected/directed graphs.
    Should be called a SG (akin to Directed Acyclic Graph).
    """
    
    def __init__(self, vertex: set, edges: list = [], name = "Unnamed", adjList = None):
        # disable directed matrices from the get-go
        directed = False
        # TODO: copy paste old constructor.
        # TODO: Override some methods that are faster for simple graphs.
 
        #super(GraphAdj, self).__init__(vertex, edge, name, directed, adjList)
        
        # post-parsing
       
        # what to do next...
    

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
        Gets the degree of a vertex.
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
        # Overall algorithm:
        # 1)See what v connects to; O(n) 
        # 2)Get deg for each neighbor (selective sum of each arr row) O(N)
        # 3)Do the while loop where you increase the pv 
        # 4) searchsorted through the results for each pv 
        # OPT: Use threading 
        # some of the code will go to pv

        # new algo:
        # get all sums for each row matrix, equivalent to getting all degs of a graph
        # sort the degs
        # create all deg combinations
        #degs = sorted([self.get_deg(v) for v in neighbors])

    
     
    def get_p(self, vertex) -> int:
        """
        Return the potential of a vertex p(v). 
        """
        i = self.VertexToIndex(vertex)
        # neighbors : apply a function s.t:
        # f(x) { sum(j) if arr[i][j] = 1
        #      { null  otherwise
        # then, to get potential, apply f(x) to the whole matrix,
        # p(v) = k where k is the number of increments
        # neighbors = np.fromiter(self.itv f)
        # get all the neighbors, get their degrees
        # THIS BEGS FOR A HEURESTIC, hoping numpy is somewhat fast
        # Can be O(n)/O(n^2) depending on the implementation 
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

 
    def color_greedy(self) -> int:
        """
        Returns the greedy coloring approximation of the chromatic number.
        """
        return NotImplemented 
         
    def color_SL(self) -> int:
        """
        Returns the Smallest Last coloring approximation of the chromatic number.
        """
        return NotImplemented

    def color_LF(self) -> int:
        """
        Returns the Largest-first coloring approximation of the chromatic number.
        """ 
        return NotImplemented
   
