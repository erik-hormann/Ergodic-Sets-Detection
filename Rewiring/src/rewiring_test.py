import mygraph as myg
import numpy as np
import networkx as nx
import walker
import os
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn.preprocessing import normalize
from matplotlib import colormaps

"""
"""


nWalks = 1000
nRewiring = 100

#%% Loading files
models_folder = '../data/'
allfiles = [f for f in os.listdir(models_folder) if os.path.isfile(os.path.join(models_folder, f))]
fileslist = list(set(allfiles) - set(['.DS_Store']))

#%% Analysis of the original graph

for file in fileslist:
    print(file)
    filepath = models_folder + file
    G = myg.import_graph(filepath)
    [ns, nw, gcc, un] = myg.FindIO(G)

    # Considering the subgraph of GCC and nontrivial ESs
    H = nx.subgraph(G,myg.flatten([myg.flatten(ns), myg.flatten(nw), gcc])).copy()
    N = H.number_of_nodes()

    wellsLookup = defaultdict(list)
    for index, sublist in enumerate(nw):
        for item in sublist:
            wellsLookup[item].append(index)


    matrix = np.zeros((len(ns), len(nw)))
    row_counter = 0
    for source in ns:
        #  taking into account different behaviours of [*, *, ..., *] and [*]
        if len(source)>1:
            start = [source[0]]
        else:
            start = source
        #  running the RW
        X = walker.random_walks(H, n_walks=nWalks, walk_len=N, start_nodes=start)
        #  counting the
        matrix_row = np.zeros((1,len(nw)))
        for value in X[:,-1]:
            if value not in myg.flatten(nw):
                print("End point not in wells set. Value " + str(value))
            else:
                arrival_index = wellsLookup[value][0]
                matrix[row_counter,arrival_index] += 1
        row_counter += 1


#  normalising matrix

matrix = normalize(matrix, axis=1)

inDegreesVertices = [val for (node, val) in H.in_degree()]
inDegreesWells = []
for y in nw:
    if len(y) > 1:
        a=1
    subx = nx.subgraph(G, y)
    ind = sum([inDegreesVertices[i] for i in y]) - sum([d for n, d in subx.in_degree()])
    inDegreesWells.append(ind)

endFrequency = np.sum(matrix, axis=0)

#%% Plotting

plt.imshow(matrix, extent = [0, 100, 0, 100])
plt.title("Original core")
plt.colorbar()
plt.set_cmap('YlOrRd')
#plt.savefig("../figures/original_core.png")
plt.show()

plt.plot(endFrequency)
plt.title("End points")
plt.show()


plt.plot(inDegreesWells)
plt.title("Wells in-degree")
plt.show()

plt.loglog([float(i)/sum(endFrequency) for i in endFrequency],inDegreesWells, 'o')
plt.title("Normalised Variation")
plt.show()


#%% Repeat with rewiring

for file in fileslist:
    print(file)
    filepath = models_folder + file
    G = myg.import_graph(filepath)
    [ns, nw, gcc, un] = myg.FindIO(G)

    H = nx.subgraph(G, myg.flatten([myg.flatten(ns), myg.flatten(nw), gcc])).copy()
    N = H.number_of_nodes()

    wellsLookup = defaultdict(list)

    for index, sublist in enumerate(nw):
        for item in sublist:
            wellsLookup[item].append(index)

    #  Rewiring core now

    finalMatrix = np.zeros((len(ns), len(nw)))

    for i in range(nRewiring):
        core = G.subgraph(gcc).copy()
        edges_to_remove = nx.edges(core)
        in_degree = [d for n, d in core.in_degree()]
        out_degree = [d for n, d in core.out_degree()]
        rewired_core = nx.directed_configuration_model([i for i in in_degree], [j for j in out_degree], create_using=nx.DiGraph)

        # making sure the core hasn't unconnected nodes
        [ns2, nw2, gcc2, un2] = myg.FindIO(rewired_core)
        rewired_core.remove_nodes_from(myg.flatten(un2))

        # now graph has unlabelled edges
        node_labels = dict(zip(list(rewired_core.nodes()), list(core.nodes())))
        nx.relabel_nodes(rewired_core, node_labels, copy=False)
        edges_to_add = nx.edges(rewired_core)
        G.remove_edges_from(list(edges_to_remove))
        G.add_edges_from(list(edges_to_add))

        print(nx.is_directed(G))

        row_counter = 0

        for source in ns:
            #  taking into account different behaviours of [*, *, ..., *] and [*]

            if len(source)>1:
                start = [source[0]]
            else:
                start = source

            #  running the RW
            X = walker.random_walks(G, n_walks=nWalks, walk_len=N, start_nodes=start)

            #  counting the ending
            for value in X[:,-1]:
                try:
                    arrival_index = wellsLookup[value][0]
                    finalMatrix[row_counter, arrival_index] += arrival_index
                except:
                    dummy=1
            row_counter += 1

#  normalising matrix

finalMatrix = normalize(finalMatrix, axis=1)

plt.imshow(finalMatrix,extent = [0, 100, 0, 100])
plt.colorbar()
plt.title("Rewired core [rewirings = " +str(nRewiring) + "]")
plt.set_cmap('YlOrRd')
plt.savefig("../figures/rewired_core.png")
plt.show()