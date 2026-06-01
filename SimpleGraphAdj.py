# CC FRANCISZEK MOSZCZUK 2026

import io
import random
import re

# required dep
from collections import deque
from functools import reduce

import numpy as np

# local imports
import grapyte.GraphAdj as GraphAdj


class SimpleGraphAdj(GraphAdj):
    """
    Simple Matrix-based Unlooped, Undirected/directed graphs.
    Should be called a SG (akin to Directed Acyclic Graph).
    """
    
    def __init__(self, 
                 vertex: set[str] | None = None, 
                 edges: list[tuple[str, str]] | None = None, 
                 name: "Name of the graph" = "Unnamed", 
                 array = None, vti = None, itv = None, 
                 directed: bool = False):

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

    def add_edge(self, edge: tuple[str, str]):
        """
        Adds an edge. Checks whether the edge is valid, then inserts.
        Does not allow duplicate edges nor self-loops.
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
           if c == d:
              raise ValueError(f"Loop: {edge}")
           else:
              #if not self.directed:
              self.adjMatrix[c, d] += 1
              self.adjMatrix[d, c] += 1
        else:
           raise TypeError(f"Bad Type: Edge is a {edge}! Expected a tuple...")

         
    """
    Getters
    """

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

    def get_deg(self, vertex: str | int)-> int:
        """
        Gets the degree deg(v) of a vertex.
        Also is the reason why we require Python 3.10+.
        https://peps.python.org/pep-0604/
        """
        # Loops v -> v are counted twice, 2*a+b+c... = sum(row) + a
        # Simple graphs don't have loops idiot
        if isinstance(vertex, str): 
            pos = self.VertexToIndex[vertex]
            return self.adjMatrix[pos].sum() 
        elif isinstance(vertex, int):
            return self.adjMatrix[vertex].sum()
        else:
            raise TypeError(f"get_deg requires an int | str, not {type(vertex)}") 


    def get_H(self) -> int:
        """
        Return the H index, the inverse of potential.
        """
        return NotImplemented
    

    def get_P(self) -> int:
        """
        Return the Potential of the graph P(G).

        Usecase:
           P(G) + 1 is a good upper bound approximation of the chromatic number.
        """
        
        degs = sorted([self.get_p(v) for v in self.VertexToIndex])
        return max(degs)
            

    # MODS HE POSTED 'P
    def get_p(self, vertex: str) -> int:
        """
        Return the potential of a vertex p(v). 
        """
        i = self.VertexToIndex[vertex]
        # neighbors : apply a function s.t:
        # f(x) { sum(j) if arr[i][j] = 1
        #      { null  otherwise
        # then, to get potential, apply f(x) to the whole matrix, then
        # p(v) = k where k is the number of increments
        # neighbors = np.fromiter(self.itv f)
        #print(f"Iterating over row {self.adjMatrix[i]}")
        iterable =  (self.adjMatrix[j].sum() for j in np.nonzero(self.adjMatrix[i])[0])
        neighbors = sorted(np.array(np.fromiter(iterable, int))) 
        #print(neighbors)
        max_p = 1
        neighbor_max = neighbors[0]

        for neighbor in neighbors:
            if neighbor > neighbor_max:
                max_p += 1
                neighbor_max = neighbor
        
        return max_p


    def get_chromatic_upper_bound(self):
        """
        Gets the upper chromatic upper bound with sqrt(2*m) + 1.
        """
        return np.sqrt(2*self.count_vertex()) + 1   


    def get_chromatic_lower_bound(self):
        """
        Gets the lower chromatic upper bound with n^2/(n^2 - 2*m)
        """   
        # ISTG this method SUCKS and will sooner or later make me cry 
        # TODO: Chopping block: len(self.IndexToVertex * 3
        # TODO: Chopping block: len(self.VertexToIndex
        n = len(self.IndexToVertex)
        return n**2/(n**2 - 2*self.count_vertex())

    """
    Setters 
    TODO:
    """


    """
    from methods (g6, dimacs)
    """

    @classmethod 
    def from_dimacs(cls, data: str = None, path: str = "") -> np.ndarray:
        """
        Reads the DIMACS graph format.
        Reads from path file first if present.
        Path can be either a system path or a fd.
        If both data and path are entry, throws a ValueError.
        This one ensures that there's just one edge for each connection.
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
            the output of the FSM.
            3) This is a minimal DIMACS 2nd ed parser. x parameter description 
            and v params are not supported, as I don't know how to draw graphs in GUI.
            This also isn't 1st ed, 3rd ed or any other ed as the multigraph 
            class doesn't support weighted edges, or nodes description (n ID param).
 
            Grammar for each regex:
            - comment line is accepting the words: *c*. In other words,
            comments can appear anywhere in the file.
            - problem line is accepting words: !entered_problem & problem_line
            - edge line is accepting words: p & edge_line OR e & edge_line
            - Every other sequence ends up in an error state, which raises 
            an exception.
            
            # finish on file end on edge line or comment; 
            # if not in acceptor state, throw 
            # if the comment/problem/edges perl re capture doesn't match, also throw
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
                    # Notice the = 1 (not += like in GraphAdj).
                    if u != v:
                        matrix[u, v] = 1
                        matrix[v, u] = 1
                        edges_cnt += 1
                    else:
                       raise ValueError(f"[DIMACS 2nd Parser] Node Loop detected {line}")
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
    Coloring
    """    
 
    def color_greedy(self, init_list = None, return_coloring: bool = False) -> int | tuple[int, dict]:
        """
        Returns approximation of the chromatic number using the greedy algorithm.
        Also known as Random Sequential.
        c is bounded by the Grundy number.

        More info: 
        https://people.cs.uchicago.edu/~laci/HANDOUTS/greedycoloring.pdf
        """
        
        # color(num# vertex) -> int
        coloring = dict() 
        if not init_list: 
            # shuffle indexes (improves coloring a bit)
            # pi -> {v2, v4, ...} [Borowiecki]
            rand_list = list(self.IndexToVertex)
            random.shuffle(rand_list)
            # print(f"Randlist: {rand_list}")
        else:
            # Initialization list. Not type-checked.
            # Consists of indicies from ITV.
            rand_list = init_list
            # print(f"Randlist provided: {rand_list}")

        # Initial coloring num
        c = 0
        for v in rand_list:
            adj_colors = []
            # numpy iterator for convenience (external_loop doesn't work)
            neighbors = np.nditer(self.adjMatrix[v], flags=['f_index'])
            for neighbor in neighbors:
                # an edge actually exists
                # could be improved with np.nonzero instead
                if neighbor > 0:
                   # 1) neighbor is colored
                   # print(f"Found an edge! {neighbors.index}")
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
            #print(coloring) 
        # reindexing as colors go from 0 to χ-1
        c = c+1
        if return_coloring:
           return c, coloring 
        else:
           return c

        #Calling convention: either G.color_greedy() or G.color_RS(), same thing.
    color_RS = color_greedy


    def color_greedy_exp(self) -> int:
        """
        Experimental Greedy variation, backtraces one layer back to color
        the vertex.
        """
 
        coloring = dict()
        bucket = list(self.IndexToVertex)

        c = 0 
        # if there's uncolored vertex v in G
        while bucket:
            # take item from bucket
            item = random.choice(bucket)
              
            # returns the indicies
            neighbors = np.nonzero(self.adjMatrix[item])[0]
            origin_adj_colors = []
            
            for neighbor in neighbors:
                # skip the central
                if neighbor == item:
                    continue
                elif neighbor in coloring:
                    continue
                else:
                    adj_colors = []
                    # Column-wise iteration over the neighbor
                    #print(f"Multi-index: {neighbor, neighbors}")
                    # Evil fucking double iter
                    evil_iter = np.nonzero(self.adjMatrix[neighbor])[0]
                    for neighbor_of_neighbor in evil_iter:
                        #print(f"Current neighbor2nd: {neighbor_of_neighbor}")
                        if neighbor_of_neighbor in coloring:
                           adj_colors.append(coloring[neighbor_of_neighbor])
                           #print(f"Colors: {adj_colors}")
                    k = 0
                    while k in adj_colors:
                        k += 1
                    coloring[neighbor] = k
                    # delete v from bucket once colored 
                    bucket.remove(neighbor)
                    #print(f"color bucket : {bucket}")
                    # append to centerpiece
                    origin_adj_colors.append(k)
                    # update c
                    if k > c:
                       c = k
            # do the same for the central vertex (IF it's uncolored colored)
            if item not in coloring:
                k = 0
                while k in origin_adj_colors:
                    k += 1
                coloring[item] = k
                # delete v from bucket once colored 
                bucket.remove(item)
                print(f"Outside color bucket: {bucket}")
                if k > c:
                   c = k
            else:
                continue
        #print(f"Final coloring: {coloring}") 
        #     for every u adj to v
        #         for every z adj to u
        #             color u
        #     color v
        # skip colored (empty bucket -> remove colored from set)
        return c + 1


    def color_LF(self, return_coloring: bool = False) -> int | tuple[int, dict]:
        """
        Returns the Largest-first coloring approximation of the chromatic number.
        Essentially greedy but with some ordering based on degrees.
        Let π be an ordering of Vertexes of Graph V = {V_1 ... V_n}.
        
        RS (Random Sequential) summons a random order.
        LF returns the ordering s.t {deg(v_i) >= deg(v_i+1)}.

        Originally developed by [Welsh and Powell 1967], thus also the name
        (Welsh Powell Algorithm (WP) 
        """ 
        degs_dict = {vertex: self.get_deg(vertex) for vertex in self.IndexToVertex}
        LF = dict(sorted(degs_dict.items(), reverse=True, key=lambda item: item[1]))
        # print(LF)
        # χ  
        if return_coloring:
           return self.color_greedy(init_list=list(LF), return_coloring=True)
        else:
           return self.color_greedy(init_list=list(LF))
    color_WP = color_LF
         

    def color_SL(self, return_coloring: bool = False) -> int | tuple[int, dict]:
        """
        Returns the Smallest Last coloring approximation of the chromatic number.
        This, surprisingly, is also greedy. 
        Originally developed by [Matula 1968], code is based on the COLPACK graph suite.
        DOI 10.1145/0000000.0000000
        """
        # There is also the opposite: forward_degree - used in Dynamic LF
        # not to be confused with Distributed Largest First 
        back_degree = {vertex: self.get_deg(vertex) for vertex in self.IndexToVertex}
        SL = deque()

        while back_degree:
            # get min, reduce the array
            smallest = min(back_degree, key=back_degree.get)
            #print(f"New smallest: {smallest}, {back_degree}")
            SL.appendleft(smallest)
            del back_degree[smallest]
            neighbors = np.nonzero(self.adjMatrix[smallest])[0]
            #print(neighbors)
            # decrease neighbors by one
            for neighbor in neighbors:
                try:
                    back_degree[neighbor] -= 1
                except KeyError:
                    pass
            #print(f"Updated dict: {back_degree} and {SL}")

        # χ  
        if return_coloring:
            return self.color_greedy(init_list=list(SL), return_coloring=True)
        else:
            return self.color_greedy(init_list=list(SL))


    def color_SLF(self) -> int:
        """
        [Brélaz 1979] DSATUR algorithm.
        https://doi.org/10.1145%2F359094.359101

        Oops! All Greedy!
        """
        # while not uncolored: 
        #     calculate_satur
        #     choose the smallest vertex with satur
        #     color with the smallest color available (simple loop from greedy)
        # χ  
        # return c
        return NotImplemented
    color_DSTATUR = color_SLF
   
    
    """
    AAAAAAH Search Algorithms.
    TODO: Implement for both adj Matrix and List.
    """
    # TODO: add params:
    # depth
    # d : int = None
    # preorder, postorder display
    # ASCII art
    def DFS(self):
        """
        Depth-first search. Returns the Search Tree as a new List/Matrix
        """
        def search_dfs(v):
            """
            Unlike in DFS for lists, v is the row index of the array, instead of a string.
            """
            print(f"search dfs {v}")
            # PRE-VISIT
            visited[v] = True
            neighbors = np.nditer(self.adjMatrix[v], flags=['f_index'])
            for neighbor in neighbors:
                # if there's an edge at all
                if neighbor:
                    index = neighbors.index
                    if visited[index] is False:
                        print(f"{v} -> {index}")
                        #T[v].append(index)
                        M[v, index] = 1 
                        search_dfs(index)
                # else do nothing
        
        # visited<vertex> -> bool
        
        # Thankfully we do not need to sort the ITV dict again like in the case
        # of sets
        # this should return a Tree (or a DAG) type in the future
        visited = {vertex:False for vertex in self.IndexToVertex.keys()}
        
        # easier to verify
        #T = {vertex:[] for vertex in sorted(self.IndexToVertex.keys())}        
        a = len(self.IndexToVertex)
        M = np.zeros((a, a), dtype=np.int_)
         
        print(visited)  
        for vertex, flag in visited.items():
            print(f"Current vertex: {vertex}")
            if not visited[vertex]: 
               # find first unvisited root node
               search_dfs(vertex)
        #print(T)
        print(M) 
        return M


    def BFS(self):
        """
        Breadth-first search. Returns the Search Tree as both a new adjacency matrix,
        as well as a list (to show the solutions)?
        """
        def search_bfs(v):
            visited[v] = True
            bfs_queue = deque([v])
            # print(f"bfs called: {bfs_queue}")
            # dequeue and iterate over child nodes
            while bfs_queue:
                #print(f"Current queue: {bfs_queue}")
                vertex = bfs_queue.popleft()
                neighbors = np.nditer(self.adjMatrix[vertex], flags=['f_index'])
                for neighbor in neighbors:
                    if neighbor:
                        index = neighbors.index
                        print(f"u:{self.IndexToVertex[index]} (index {index}) in neighborhood of \
{self.IndexToVertex[vertex]}(index {vertex}...")
                        if visited[index] is False:
                            visited[index] = True
                            # add vertex to the current tree
                            M[vertex, index] = 1
                            bfs_queue.append(index)


        visited = {vertex:False for vertex in self.IndexToVertex.keys()}
        a = len(self.IndexToVertex)
        M = np.zeros((a, a), dtype=np.int_)
         
        print(visited)  
        for vertex, flag in visited.items():
            #print(f"Current vertex: {vertex}")
            if not visited[vertex]: 
               # find first unvisited root node
               search_bfs(vertex)
         
        return M

    
    #def isTree(self):
    #    """
    #    Is the graph a tree?
    #    Two criteria
    #    NOT a forest
    #    no vertex is disjoint from graph
    #    |V| = E
    #    orrrr via DFS
    #    """
    #    if 

    #def cycles_from_vertex()
    #    """
    #    Get cycles from vertex with DFS.
    #    """


    #def is_acyclic()
    #    Does acycic calculation
