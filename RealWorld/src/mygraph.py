#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 09:52:33 2021

@author: erikhormann
"""

import igraph
import pickle
import numpy as np
import networkx as nx


def ig2nx(G):
    Adj = np.array(G.get_adjacency().data)

    H = nx.from_numpy_array(Adj)

    return H

def GenerateER_IO(N0, p):
    G = nx.erdos_renyi_graph(N0, p, directed=True)
    
    #adding I/O
    N = N0 + 8
    G.add_nodes_from([N0+1,N0+2,N0+3,N0+4,N0+5,N0+6,N0+7])

    edges = [(N0, 0), (N0+1, 1), (N0+2, 2), (N0+3, 3), #inputs
             (4, N0+4), (5, N0+5), (6, N0+6), (7, N0+7)]
    G.add_edges_from(edges)
    
    return G

def GraphPrint(G):
    my_layout = G.layout("lgl")
    N = G.number_of_nodes()
    visual_style = {"bbox": (1000, 1000), "vertex_size": 20, "vertex_label": list(range(N)),
                "edge_arrow_width": 1, "vertex_color": "white", "edge_width": 2, "layout": my_layout}
    nx.draw(G, **visual_style)
    plt.show()
    
    return

def FindIO(G):
    # diam = G.diameter(directed ='TRUE')

    A = nx.adjacency_matrix(G)
    A = A.toarray()

    wells = []
    sources = []
    gcc = []
    unconnected = []
    
    clusters = nx.strongly_connected_components(G)
    clusters = list(clusters)
    
    all_indices = list(range(G.number_of_nodes()))
    
    for cl in clusters:
        clist = list(cl)
        clist = list(map(int, clist))
        #test for output
        others = [item for item in all_indices if item not in clist]
        outgoing_links = A[np.ix_(clist, others)]
        incoming_links = A[np.ix_(others, clist)]
        if (outgoing_links != 0).any() and (incoming_links == 0).all():
            sources.append(clist)
        elif (outgoing_links == 0).all() and (incoming_links != 0).any():
            wells.append(clist)
        elif (outgoing_links != 0).any() and (incoming_links != 0).any():
            gcc.append(clist)
        elif (outgoing_links == 0).all() and (incoming_links == 0).all():
            unconnected.append(clist)
        else:
            raise ValueError("Error with the splitting of the graph in Strongly Connected Components")

    # sources = [el for subl in sources for el in subl]
    # wells = [el for subl in wells for el in subl]
    gcc = [el for subl in gcc for el in subl]

    return sources, wells, gcc, unconnected

def flatten(xss):
    return [x for xs in xss for x in xs]

def FindIO_lenght(G):
    A = nx.adjacency_matrix(G)
    A = A.toarray()

    wells = []
    sources = []
    gcc = []
    unconnected = []

    clusters = nx.strongly_connected_components(G)
    clusters = list(clusters)

    all_indices = list(range(G.number_of_nodes()))

    for cl in clusters:
        clist = list(cl)
        clist = list(map(int, clist))
        # test for output
        others = [item for item in all_indices if item not in clist]
        outgoing_links = A[np.ix_(clist, others)]
        incoming_links = A[np.ix_(others, clist)]
        if (outgoing_links != 0).any() and (incoming_links == 0).all():
            sources.append(clist)
        elif (outgoing_links == 0).all() and (incoming_links != 0).any():
            wells.append(clist)
        elif (outgoing_links != 0).any() and (incoming_links != 0).any():
            gcc.append(clist)
        elif (outgoing_links == 0).all() and (incoming_links == 0).all():
            unconnected.append(clist)
        else:
            raise ValueError("Error with the splitting of the graph in Strongly Connected Components")


    sources = [el for subl in sources for el in subl]
    wells = [el for subl in wells for el in subl]
    gcc = [el for subl in gcc for el in subl]
    unconnected = [el for subl in unconnected for el in subl]

    
    return len(sources),len(wells), len(gcc), len(unconnected)

def import_graph(filename):

    if filename.endswith('.xml'):
        G = igraph.Graph.Read_GraphML(filename)
        return G

    elif filename.endswith('.gml'):
        G = nx.DiGraph()
        G = nx.read_gml(filename)
        #G = nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute=None)
    
    elif filename.endswith('.csv'):
        file = open(filename, "r")
        Graphtype = nx.DiGraph()

        G = nx.parse_edgelist(file, comments='t', delimiter=',', create_using=nx.DiGraph,)
        G = nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute=None)
        return G
    
    elif filename.endswith('.el'):
        G = nx.DiGraph()
        G = nx.read_edgelist(filename, create_using=nx.DiGraph)
        G = nx.convert_node_labels_to_integers(G)
        return G
    
    elif filename.endswith(".mat"):
        G = nx.DiGraph()
        A = np.loadtxt(filename)
        G = nx.from_numpy_matrix(A, create_using=nx.DiGraph)
        G = nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute=None)
        return G
    
    elif filename.endswith(".adj"):
        G = nx.DiGraph()
        G = nx.read_adjlist(filename, create_using=nx.DiGraph())
        G = nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute=None)
        return G

    else:
        print("error: filename " + filename + " has invalid extension")

    return G







