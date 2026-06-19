# CC Franciszek Moszczuk 2026

import heapq

from collections import deque

from grapyte import DiGraph
from grapyte.utils.GraphError import GraphError

"""
Edge-Weighted (so not node-weighted) DiGraph class.
"""
class WeightedEdgeDiGraph(DiGraph):

    def __init__(self,
                 vertex: set | list,
                 edges: list[tuple[str,str, int]] | list[tuple[int, int, int]] = [],
                 name = "Unnamed Edge-Weighted DiGraph", 
                 adjList = None):
        
        # Triggers the correct behaviour in DiGraph, SimpleGraph and Graph
        self.directed = True
        self.name = name
                
        # validate set S
        templist = []
        for item in vertex:
            if not isinstance(item, str):
                templist.append(str(item))
            else:
                templist.append(item)
        self.vertex = set(templist)

        # for backwards compatibility, we use a separate dict for weights. 
        self.weight = {}        

        # self.adjList:
        # f(X): dict<str> -> list<str>
        if not adjList:
            self.adjList = {}
            for i in range(len(templist)):
                self.adjList[templist[i]] = []
            for u, v, edge_weight in edges:
                if not isinstance(u, str):
                    u = str(u)
                if not isinstance(v, str):
                    v = str(v)

                if u not in self.vertex or v not in self.vertex:
                   print(f"{u} or {v} not in set, skipping...")
                # u, v is not the same as v, u and thus is allowed
                elif v in self.adjList[u]:
                # skip duplicated
                   raise ValueError(f"Duplicate edge detected: {u, v}.")
                # loops are actually allowed in DiGraphs.
                else:
                   self.adjList[u].append(v)
                   # default weights are set to zero...?
                   self.weight[(u,v)] = edge_weight

        else:
           # TODO: some type checking required....
           self.adjList = adjList  
        print(edge_weight) 


    def __str__(self):
        return f"Weighted Graph {self.name} with the following params:\nVertex:\
{self.vertex}, Adjacency list: {self.adjList}, Edge Weights: {self.weight}"
    

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
            for key in self.adjList:
                update_list = []
                for v in self.adjList[key]:
                    if v != vertex:
                        update_list.append(v)
                    else:
                        del self.weight[(key, v)]
                self.adjList[key] = update_list
     
                #self.adjList[key] = [v for v in self.adjList[key] if v != vertex]
            del self.adjList[vertex]
         
        self.vertex.remove(vertex)



    def add_edge(self, edge: tuple[str, str, int] | tuple[int, int, int]):
        """
        Adds an edge. Checks whether there are vertexes in a graph, then inserts an additional edge.
        Graphs are of 3-lenght tuple (vertex, vertex, weight).
        This was ALSO the original form of the vertex graph.
        Unfortunately this was changed due to some arguments made with AI by the
        other team member. ~fm
        """
        # Check whether this is a tuple
        if isinstance(edge, tuple):
            a, b, weight = edge
            if not isinstance(a, str):
                a = str(a)
            if not isinstance(b, str):
                b = str(b)

            if a not in self.vertex or b not in self.vertex:
                raise KeyError(f"{a} or {b} not in the list of verticies")
            self.adjList[a].append(b)
            self.weight[(a,b)] = weight
        
        else:
           raise TypeError(f"Bad Type: {edge} is", type(edge))


    def remove_edge(self, edge: tuple[str, str, int] | tuple[int, int, int]):
        """
        Removes an edge. Throws an error if there is no such edge.
        """
        if isinstance(edge, tuple):
            a, b, weight = edge
            if not isinstance(a, str):
                a = str(a)
            if not isinstance(b, str):
                b = str(b)

        try:
            self.adjList[a].remove(b)
        except KeyError:
            raise KeyError(f"The vertex {a} or {b} you are refering to is not"
                           f"in the adjacency list.") from None
        except ValueError as err:
            raise KeyError(f"No such edge! {edge}") from None
        try:
            del self.weight[(a, b)]
        except KeyError as err:
            fail_msg = (f"If you are reading this, "
                        f"chances are you corrupted your Adjacency List.\n"
                        f"Good luck.\n"
                        f"Edge that caused the exception: {edge}\n"
                        f"Vertex Set: {self.vertex}\n"
                        f"Adj. List: {self.adjList}\n"
                        f"Edge Weights: {self.weight}")

            raise GraphError(fail_msg) from err

   
   # TODO: override vertex methods, too.

   # TODO: Djikstra
   # TODO: A*

    def SSP_Djikstra(self, vertex: str | int):
        """
        Find the Single-source Shortest Path using Djikstra's algorithm.
        """

        if not isinstance(vertex, str):
            vertex = str(vertex)

        def relax(u: str, v: str):
            """
            Relax the path. Unlike in the pseudocode, we don't actually
            have to pass the weight parameter as it is stored elsewhere.
            """
            w = self.weight[(u, v)]
            new_cost = d[u] + w
            if new_cost < d[v]:
                d[v] = new_cost
                prev[v] = u


        # Initialize (See: CRLS-ITA)
        d     = {v:math.inf for v in self.vertex}
        prev  = {v:None for v in self.vertex}
        d[vertex] = 0
        # the path s
        path = [vertex, ]
       
        # heap heap
        # array!
        #vertex_heap= [(v, d[v]) for v in self.vertex]
        #heapq.heapify(vertex_heap)
        vertex_list = [v for v in self.vertex]
       
        while vertex_list:
            # find min
            lowest = min(vertex_list, key=d.get)
            path.append(lowest)
            vertex_list.remove(lowest)
            for neighbor in self.adjList[lowest]:
                # preconstruct a tuple
                relax(lowest, neighbor)

       

    def SSP_BellmanFord(self, vertex: str):
        """
        Unlike Djikstra, Bellman Ford allows negative edge weights, but 
        *not* negative cycles.
        """
        return NotImplemented
    
