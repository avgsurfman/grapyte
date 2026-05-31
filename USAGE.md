# (The) Finest selection of tests - Usage examples

## Graph

### Directed
```
newGraph = Graph({'a', 'b'}, [('a', 'b',), ('a', 'b')], name = "Example")        
print(newGraph)
newGraph.add_vertex("z")
print(newGraph)
newGraph.add_edge(("b", "z"))
print(newGraph)
#newGraph.add_edge(("z", "y")) #errors out on purpose
newGraph.remove_edge(("a", "b"))
print(newGraph)
newGraph.remove_vertex("b")
#newGraph.remove_vertex("p") # key not in set
#print(newGraph)
```

### Undirected

```
newGraph = Graph({'a', 'b'}, [('a', 'b',), ('a', 'b')], name = "Example", directed=False)        
```

### Supply verticies as ints

```
newGraph = Graph({1, 2, 3}, [(1, 2,), (2, 3)], name = "Example", directed=False)        
```

## GraphAdj

### Directed tests

```
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
```

### Undirected 

```
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
```

## Count Walks
*Available for GraphAdj and its child classes.*

```
M = GraphAdj({'a', 'b', 'c', 'd'}, [('a', 'b',), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('c', 'd')], name = "Lecture", directed=False)        
print(M)
assert M.count_nWalks(('a', 'c'), 2) == 2, "Should be 2"
assert M.count_nWalks(('a', 'c'), 3) == 5, "Should be 5"
print(f"M 3-Cycles: {M.count_3Cycles()}")
```

## Graph --> GraphAdj conversion (List to Matrix)
```
List = Graph({'a', 'b', 'c', 'd'}, [('a', 'b',), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('c', 'd')], name = "Conversion test")
print(List)
print(List.to_GraphAdj())
```

## Error testing
```
newGraph.add_edge(("z", "y")) #errors out on purpose
newGraph.remove_edge(("a", "b"))
print(newGraph)
newGraph.remove_vertex("b")
newGraph.remove_vertex("p") # key not in set
print(newGraph)
```

## GRAPH6 parsing
```
graph6 = GraphAdj.from_graph6("DQc")
diff = GraphAdj.from_graph6("G}l~~{")
print(diff)
```

# DIGRAPH6 parsing

```
digraph6 = GraphAdj.from_digraph6("&DI?AO?")
print(digraph6)
```

# COLORING
```
G = SimpleGraphAdj.from_dimacs(path="../dimacs/dimacs_small_test.txt")
G.color_RS()
```

