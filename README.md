# grapyte - a simple graph library, written in Python

Prereqs:

1) Numpy
2) Brain (functions are annotated)
3) Python 3.10+ (Needed for dict sorting, arrow functions and union typehints)

Features:
- Reads g6/d6 format
- Multigraphs!
- Simple Graphs
- Adjacency list graphs
- Matrix graphs
- Edge graphs
- Basic operations on graphs.
- Coloring!
- Greedy coloring.
- More greedy coloring.
- DFS/BFS
- Get potential or degree of a graph.
- Native UTF-8 Support.
- And much more!

Also there is a LaTeX document if you are interested in the spec, I guess...



TODO:
- DSTAUR
- draw graph with tkinter
- better testing w/ pytest
- H-index(?!)
- Operator overrides:
- graph <= (Included/excluded operation)
- graph + operation (add subgraph)
- graph - operation (remove subgraph if possible)
- multigraph can be converted to graph and vice verse
- SG <-> G <-> GA <-> SAG
- SG || SAG -> DAG (MATRIX)?
- graph6, dimacs 2nd write-to

ideas:
https://spidermonkey.dev/blog/2025/10/28/iongraph-web.html
-rewrite this in typescript?
