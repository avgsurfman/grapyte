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
           # YOLO no type checking
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

    # TODO: depth param
    def DFS(self):
        """
        Depth-first search. Returns the Search Tree as a new adjacency list.
        """
        def search_dfs(v):
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
            if not visited[vertex]: 
               # find first unvisited root node
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
         
        print(visited)  
        for vertex, flag in visited.items():
            #print(f"Current vertex: {vertex}")
            if not visited[vertex]: 
               # find first unvisited root node
               search_bfs(vertex)
         
        #raise NotImplementedError("Not implemented yet")
        return T
