# CC Franciszek Moszczuk 2026

from collections import deque
import numpy as np
from grapyte import Graph

class SimpleGraph(Graph):
    """
    Simple Adjacency list Unlooped, Undirected/directed graphs.
    Should be called a SG (akin to Directed Acyclic Graph).
    """
    
    def __init__(self,
                 vertex: set | list,
                 edges: list[tuple[str,str]] | list[tuple[int, int]] = [],
                 name = "Unnamed", adjList = None):
        
        self.directed = False
        self.name = name

        # validate set S
        templist = []
        for item in vertex:
            if type(item) is not str:
                templist.append(str(item))
            else:
                templist.append(item)
        self.vertex = set(templist)

        # self.adjList:
        # f(X): dict<str> -> list<str>
        if not adjList:
            self.adjList = {}
            for i in range(len(templist)):
                self.adjList[templist[i]] = []
            for u, v in edges:
                if type(u) is not str:
                    u = str(u)
                if type(v) is not str:
                    v = str(v)
                if u not in self.vertex or v not in self.vertex:
                   print(f"{u} or {v} not in set, skipping...")
                elif v in self.adjList[u] or u in self.adjList[v]:
                # skip duplicated
                   raise ValueError(f"Duplicate edge detected: {u, v}.")
                # skip loops
                elif u == v:
                   raise ValueError(f"Loops not allowed: {u, v}.")
                else:
                   self.adjList[u].append(v)
                   self.adjList[v].append(u)
        else:
           self.adjList = adjList  
        
        print(self.adjList)


    def add_edge(self, edge: tuple[str, str] | tuple[int, int]):
        """
        Adds an edge. Checks whether there are vertexes in a graph, then inserts an additional edge.
        This also prevents duplicate edges.
        """
        # Check whether this is a tuple
        if type(edge) is tuple:
            a, b = edge
            if a not in self.vertex or b not in self.vertex:
                raise KeyError(f"{a} or {b} not in the list of verticies")
            elif b in self.adjList[a]:
                raise ValueError(f"Duplicate edge: {edge}.")
            elif a == b:
                raise ValueError(f"Loops not allowed: {edge}.")
            else:
                # this can fail,but again, it's not my problem
                if type(a) is not str:
                    a = str(a)
                if type(b) is not str:
                    b = str(b)
                self.adjList[a].append(b)
                if not self.directed:
                    self.adjList[b].append(a)
        else:
           raise TypeError(f"Bad Type: {edge} is", edge)


    def DFS(self, depth: int = -1, order: str = "order", disp_ascii=False):
        """
        Depth-first search. Returns the Search Tree as a new adjacency list.
        """
        def search_dfs(v : str):
            print(f"search dfs {v}")
            # PREVISIT ENDS HERE
            visited[v] = True
            # iterating over a list here.
            for neighbor in self.adjList[v]:
                if visited[neighbor] is False:
                    print(f"{v} -> {neighbor}")
                    T[v].append(neighbor)
                    search_dfs(neighbor)
                # else do nothing
        
            # POSTVISIT ENDS HERE


        def search_dfs_depth(v : str, d: int):
            print(f"search dfs {v}")
            # PREVISIT ENDS HERE
            visited[v] = True
            # iterating over a list here.
            for neighbor in self.adjList[v]:
                if (visited[neighbor] is False) and d <= depth:
                    print(f"{v} -> {neighbor}")
                    T[v].append(neighbor)
                    search_dfs(neighbor, d+1)

            # POSTVISIT ENDS HERE
        
        # visited<vertex> -> bool
        
        # the sets have to be resorted because there is some fuckery 
        # with type conversion from set to dict and the
        # resulting dict stops being sorted
        # the results are still valid but have different starting points.
        # sorted makes the resulting trees somewhat predictable 
        #
        # this should return a Tree (or a DAG) type in the future
        visited = {vertex:False for vertex in sorted(self.vertex)}
        T = {vertex:[] for vertex in sorted(self.vertex)}
        print(visited)  
        for vertex, flag in visited.items():
            print(f"Current vertex: {vertex}")
            # find first unvisited root node
            if not visited[vertex]: 
               if depth > -1:
                  search_dfs_depth(vertex, depth)
               else:
                  search_dfs(vertex)
        return T
          

    def DFS_iter(self):
        """
        Iterative version of the DFS algorithm.
        """

        def search_dfs(v : str):
            print(f"Search dfs iter: {v}")
            # N_0 invariant: every base search vertex is marked as 
            # visited
            stack = [v]
            visited[v] = True
            
            # LIFO would alleviate the difference in order but so it stays
            while stack:
                # N_n: For each N vertex, put each on stack and pop
                # and mark as visited
                print(f"Current stack: {stack}")
                vertex = stack.pop()
                print(f"Current vertex: {vertex}")
                for neighbor in self.adjList[vertex]:
                    # N_n+1 for each unvisited neighbor v,
                    # mark visited, add to search stack,
                    # add to search tree
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        T[vertex].append(neighbor)
                        stack.append(neighbor)
                    

        visited = {vertex:False for vertex in sorted(self.vertex)}
        T = {vertex:[] for vertex in sorted(self.vertex)}
        print(f"{visited, T}")  
        for vertex, flag in visited.items():
            print(f"Search tree exhausted, new vertex: {vertex}:{flag}")
            if not visited[vertex]: 
               search_dfs(vertex)

        return T 


    def BFS(self):
        """
        Breadth-first search. Returns the Search Tree as a new adjacency list.
        """
        def search_bfs(v):
            visited[v] = True
            bfs_queue = deque(v)
            # print(f"bfs called: {bfs_queue}")
            # while item in bfs.queue
            # dequeue and iterate over child nodes
            while bfs_queue:
                #print(f"Current queue: {bfs_queue}")
                vertex = bfs_queue.popleft()
                for u in self.adjList[vertex]:
                    #print(f"u {u} in neighborhood of {vertex}...")
                    if visited[u] is False:
                        visited[u] = True
                        # add vertex to the current tree
                        T[vertex].append(u)
                        bfs_queue.append(u)


        visited = {vertex:False for vertex in sorted(self.vertex)}
        T = {vertex:[] for vertex in sorted(self.vertex)}        
         
        # print(visited)  
        for vertex, flag in visited.items():
            #print(f"Current vertex: {vertex}")
            if not visited[vertex]: 
               # find first unvisited root node
               search_bfs(vertex)
         
        return T


    #def isTree(self):
    #    """
    #    Is the graph a tree?
    #    Two criteria
    #    NOT a forest -> No 0000 columns
    #    \_> no vertex is disjoint from graph
    #    |V| = E
    #    orrrr via DFS (somehow)
    #    """
    #    if 

    def get_cycles(self, vertex: str):
        """
        Get cycles for a given vertex. Not optimal.
        """
        #            target_vertex current_vertex local_dict               tuple path
        def dfs_cycles(current: str, parent: str, visited: dict[str, bool], path: tuple[str]):
            visited[current] = True
            print(path)
            print(f"Current vertex: {parent}")
            print(f"local? visited: {visited}")
            for neighbor in self.adjList[current]:
                if not visited[neighbor]:
                    # shallow copy works here thanks to immutable elements and non-vars
                    dfs_cycles(neighbor, current, visited.copy(), path + (neighbor,))
                elif neighbor == parent:
                    # parent == neighbor => backedge, ignore
                    continue
                elif neighbor == vertex:
                    print(f"neigh {neighbor} par {parent} vertex {vertex}")
                    # add to cycle list
                    cycles_list.append(path)
                
        visited = {vertex:False for vertex in sorted(self.vertex)}
        cycles_list = []        
        dfs_cycles(vertex, vertex, visited, (vertex,)) 

        return cycles_list 
            

    def get_cycles_st(self):
        """
        Get cycles from vertex with DFS w/ that st paths paper.

        """
        return NotImplemented 

    def get_cycle_bases(self):
        """
        Get simple cycles using the Paton's algorithm.
        """
        return NotImplemented


    """
    https://stackoverflow.com/questions/20556802/determining-whether-or-not-a-directed-or-undirected-graph-is-a-tree
    
    This is also based on a lemma from Cormen et al. ItA.
    - A (directed) graph is acyclic if and only if DFS yield no backedges. (20.11 p.573)
    - Undirected Graphs have only tree edges and back edges. (20.10 p. 570)
    """
   
    def __search_dfs_cycles(self, v: str, parent: str, visited: dict[str,bool]) -> bool:
        """
        Private (protected) method for checking acylicity.
        """ 
        # From each vertex, we search edge and mark visited vertices
        # if we encounter the same vertex from an unvisited edge,
        # we have a cycle.
                  
        visited[v] = True
        for neighbor in self.adjList[v]:
            if not visited[neighbor]:
                print(f"{v} -> {neighbor}")
                # bubble up the result negative result
                if not self.__search_dfs_cycles(neighbor, v, visited):
                    return False
            elif neighbor != parent: 
                print(f"Cycle discovered! {neighbor, parent}")
                return False
            else:
                print(f"Back edge: {neighbor, parent}")
                # loops do count as back edges
                # see: Cormen et al. ItA
                continue

        return True                    


    def is_acyclic(self):
        """
        Does the graph contain a cycle?
        Based on modified DFS.
        """
        visited = {vertex:False for vertex in sorted(self.vertex)}

        # unlike in is_tree we traverse the whole graph
        # even if its disjoint
        for vertex, flag in visited.items():
            print(f"Search tree exhausted, new vertex: {vertex}:{flag}")
            if not visited[vertex]: 
               if not self.__search_dfs_cycles(vertex, vertex, visited):
                   return False
        return True
        


    def is_tree_dfs(self):
        """
        Technically a faster way to do it in O(v) would to check for empty
        vertices and to check the count of edges (n-1).
        However, lists aren't that fast (as numpy matrices are).
        Alternative solution would be to simply
        sum = 0
        for v in adjList:
            if not v:
                return False
            sum += len(adjList[v])
        if (edges - 1) == len(vertex):
            return True
        return False 
        Based on modified DFS.
        """
        # cycle has different edges and verticies
        #def search_dfs(v : str) -> bool:
        #    print(f"Search dfs for cyles: {v}")
        #    # From each vertex, we search edge and mark visited vertices
        #    # if we encounter the same vertex from an unvisited edge,
        #    # we have a cycle.
        #              
        #    visited[v] = True
        #    for neighbor in self.adjList[v]:
        #        # preconstruct an edge
        #        current_edge = (v, neighbor)
        #        reverse_edge = (neighbor, v)
        #        if visited[neighbor] is False:
        #            print(f"{v} -> {neighbor}")
        #            edges.append(current_edge)
        #            print(f"{edges}")
        #            # bubble up the result negative result
        #            if not search_dfs(neighbor):
        #                return False
        #        elif (current_edge not in edges) and (reverse_edge not in edges):
        #            print(f"Cycle discovered! {current_edge} not in {edges}")
        #            return False
        #        else:
        #            print(f"Edge already discovered: {current_edge}")
        #            continue

        #    return True                    


        visited = {vertex:False for vertex in sorted(self.vertex)}
        # edges = []

        # pick any vertex, here we pick first
        vertex = next(iter(visited))
        if not self.__search_dfs_cycles(vertex, vertex, visited):
            return False
        
        # after traversal, make sure every edge was discovered
        return all(visited.values()) 

