class SimpleGraph(GraphAdj):
    """
    Simple Matrix-based Unlooped, Undirected/directed graphs.
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
        Return the Potential.

        Usecase:
           P(G) + 1 is a good approximation of coloring.
        """
