import networkx as nx
import numpy as np
import math
import time
import tracemalloc

# Zadanie 1c (wewnętrzne)
def create_interval_graph(filepath):
    intervals = {}
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                intervals[parts[0]] = (float(parts[1]), float(parts[2]))

    G = nx.Graph()
    G.add_nodes_from(intervals.keys())
    nodes = list(intervals.keys())

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):                                                          # Not check the same invertals and their pairs twice
            u, v = nodes[i], nodes[j]                                                               # This comment is here because of the picture for the presentation
            if max(intervals[u][0], intervals[v][0]) <= min(intervals[u][1], intervals[v][1]):
                G.add_edge(u, v)
    return G

# Rozpoczęcie pomiarów
tracemalloc.start()
t_start_nx = time.perf_counter()

G_nx = nx.Graph()

# Budowa głównego grafu
edges = [
    (1, 2), (1, 3), (1, 13), (2, 3), (2, 13), (3, 13),
    (4, 5), (4, 6), (4, 14), (5, 6), (5, 14), (6, 14),
    (7, 8), (7, 9), (7, 15), (8, 9), (8, 15), (9, 15),
    (10, 11), (10, 12), (10, 16), (11, 12), (11, 16), (12, 16),
    (13, 17), (14, 17), (15, 17), (16, 17)
]
G_nx.add_edges_from(edges)

print(f"Graf bazowy zbudowany. Liczba krawędzi: {G_nx.number_of_edges()}")

# Zadanie 1a (wewnętrzne)
mat_nx = nx.to_numpy_array(G_nx)
print("Pierwotna macierz sąsiedztwa: ")
for row in mat_nx:
    print(row)
G_nx.add_node(99)
G_nx.add_node(100)
G_nx.add_edge(99, 1)
G_nx.add_edge(99, 100)
mat_nx = nx.to_numpy_array(G_nx)
print("Macierz sąsiedztwa po zmianach: ")
for row in mat_nx:
    print(row)
G_from_mat = nx.from_numpy_array(mat_nx)
adj_list = nx.to_dict_of_lists(G_from_mat)
print(f"Listy sąsiedztw utworzona ze zmodyfikowanej macierzy: {adj_list}")
G_nx.remove_edge(99, 1)
G_nx.remove_edge(99, 100)
G_nx.remove_node(99)
G_nx.remove_node(100)
print(f"Listy sąsiedztw po powrocie do pierwotnego grafu: {adj_list}")
G_from_list = nx.from_dict_of_lists(adj_list)
mat_nx1 = nx.to_numpy_array(G_from_list)
print("Końcowa macierz sąsiedztwa: ")
for row in mat_nx1:
    print(row)
equals = np.all(mat_nx == mat_nx1)
if equals:
    print("Pierwotna i końcowa macierz sąsiedztwa są równe")
else:
    print("Pierwotna i końcowa macierz sąsiedztwa nie są równe")

# Zadanie 1c (wewnętrzne)
with open("intervals_nx.txt", "w") as f:
    f.write("A 1 7\nB 2 4\nC 3 15\nD 6 14\nE 9 11\nF 13 18\nG 17 19\n")
G_int_nx = create_interval_graph("intervals_nx.txt")
adj_l_int = nx.to_dict_of_lists(G_int_nx)
print(f"Listy sąsiedztw dla grafu przecięć przedziałów przed zmianami: {adj_l_int}")
G_int_nx.remove_edge('G', 'F')
G_int_nx.remove_edge('D', 'F')
G_int_nx.remove_node('G')
G_int_nx.remove_node('F')
adj_l_int = nx.to_dict_of_lists(G_int_nx)
print(f"Listy sąsiedztw dla grafu przecięć przedziałów po zmianach: {adj_l_int}")

# Zadanie 1a (zewnętrzne)
nx.write_graph6(G_nx, "test_nx.g6")
loaded_G_nx = nx.read_graph6("test_nx.g6")
print(f"Krawędzi po wczytaniu grafu w formacie GRAPH6: {loaded_G_nx.number_of_edges()}")
with open("test_nx.g6", "r") as f:
    for linia in f:
        print(linia.strip())

# Memory limits of NetworkX implementation:
# - Adjacency matrix:
# F.ex: 100 000 vertexes -> 10^10 elements in adjacency matrix
# 10^10 elements * 8 B = 8E10 B of RAM = 80 GB of RAM
# If this graph has small amount of edges (sparse graphs), it's huge waste of memory for redundant zeros.
# - Adjacency lists:
# For the same situation (100 000 vertexes, 50 edges), it's ca. 80 MB of RAM, it's a massive difference.
# Time limits of NetworkX implementation for list all edges:
# - Adjacency matrix: theta(V^2)
# - Adjacency lists: theta(V+E)

# Zadanie 2b
A = nx.to_numpy_array(G_nx)
A3 = np.linalg.matrix_power(A, 3)
cycles_3 = int(np.trace(A3) // 6)
print(f"Liczba cykli dł. 3: {cycles_3}")

# Zadanie 3a
degrees = sorted([d for n, d in G_nx.degree()])
m = G_nx.number_of_edges()
a_num = 0
curr_sum = 0
for d in degrees:
    if curr_sum + d <= m:
        curr_sum += d
        a_num += 1
    else:
        break
print(f"Liczba anihilacji: {a_num}")

# ZADANIE 3c
abc_idx = sum(math.sqrt((G_nx.degree[u] + G_nx.degree[v] - 2) / (G_nx.degree[u] * G_nx.degree[v]))
              for u, v in G_nx.edges())
print(f"Indeks ABC: {abc_idx:.4f}")

# Zatrzymanie pomiarów
t_end_nx = time.perf_counter()
current_nx, peak_nx = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"\n[NetworkX] Czas całkowity: {t_end_nx - t_start_nx:.6f} s")
print(f"[NetworkX] Szczytowa pamięć: {peak_nx / 1024:.2f} KB (kibibajtów)")