import networkx as nx
import mygraph as myg
import numpy as np
import matplotlib.pyplot as plt
import pickle

N0=100
p = 0.45

G = nx.erdos_renyi_graph(N0, p, directed=True)

#adding I/O
N = N0 + 8
G.add_nodes_from([N0,N0+1,N0+2,N0+3,N0+4,N0+5,N0+6,N0+7])

edges = [(N0, 0), (N0+1, 1), (N0+2, 2), (N0+3, 3), #inputs
         (4, N0+4), (5, N0+5), (6, N0+6), (7, N0+7), (N0+4,N0), (N0-3,N0+3),(N0+5,N0+6)] #outputs
G.add_edges_from(edges)

[sources, wells, gcc] = myg.FindIO(G)

print(sources, wells, gcc)

nx.draw(G)
plt.show()
