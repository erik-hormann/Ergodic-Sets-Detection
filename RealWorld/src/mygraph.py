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

def GenerateER_IO(N0,p):
    G = igraph.Graph.Erdos_Renyi(N0, p, directed=True, loops=False)
    
    #adding I/O
    N = N0 + 8
    G.add_vertices(8)
    
    edges = [(N0, 0), (N0+1, 1), (N0+2, 2), (N0+3, 3), #inputs
             (4, N0+4), (5, N0+5), (6, N0+6), (7, N0+7)]
    G.add_edges(edges)
    
    return G

def GraphPrint(G):
    my_layout = G.layout("lgl")
    N = G.vcount()
    visual_style = {"bbox": (1000, 1000), "vertex_size": 20, "vertex_label": list(range(N)),
                "edge_arrow_width": 1, "vertex_color": "white", "edge_width": 2, "layout": my_layout}
    igraph.plot(G, **visual_style).show()
    
    return

def FindIO(G):
    # diam = G.diameter(directed ='TRUE')
    
    A = nx.adjacency_matrix(G)
    A = A.toarray()
    
    
    wells = []
    sources = []
    gcc = []
    
    clusters = nx.strongly_connected_components(G)
    clusters = list(clusters)
    
    all_indices = list(range(G.number_of_nodes()))
    
    for cl in clusters:
        clist = list(cl)
        clist = list(map(int, clist))
        #test for output
        outbound = [item for item in all_indices if item not in clist]
        inbound  = [item for item in all_indices if item not in clist]
        A_out = A[np.ix_(clist,outbound)]
        if (A_out != 0).any():
            sources.append(clist)
            
        A_in = A[np.ix_(inbound, clist)]
        if (A_in != 0).any():
            wells.append(clist)
    
    # for cl in clusters:
    #     for v in cl:
    #         if A[v,:].any() != 0:
    #             sources.append(cl)
    #             break
    #     for v in cl:
    #         if A[:,v].any() != 0:
    #             wells.append(cl)
    #             break
    
    # deleting sets which are both inputs and outputs and putting them in the GCC
    check = True
    while check:
        check = False
        for i in wells:
            if i in sources:
              wells.remove(i)
              sources.remove(i)
              gcc.append(i)
              check = True
    
    # accounting for when there is only one GCC
    if len(gcc) == 1:
        if len(gcc[0]) == G.vcount():
            gcc[0] = gcc[0].tolist()
            
    return sources, wells, gcc

def FindIO_lenght(G):
    # diam = G.diameter(directed ='TRUE')
    
    A = nx.adjacency_matrix(G)
    A = A.toarray()
    
    
    wells = []
    sources = []
    gcc = []
    
    clusters = nx.strongly_connected_components(G)
    clusters = list(clusters)
    
    all_indices = list(range(G.number_of_nodes()))
    
    for cl in clusters:
        clist = list(cl)
        clist = list(map(int, clist))
        #test for output
        outbound = [item for item in all_indices if item not in clist]
        inbound  = [item for item in all_indices if item not in clist]
        A_out = A[np.ix_(clist,outbound)]
        if (A_out != 0).any():
            sources.append(clist)
            
        A_in = A[np.ix_(inbound, clist)]
        if (A_in != 0).any():
            wells.append(clist)
    
    # for cl in clusters:
    #     for v in cl:
    #         if A[v,:].any() != 0:
    #             sources.append(cl)
    #             break
    #     for v in cl:
    #         if A[:,v].any() != 0:
    #             wells.append(cl)
    #             break
    
    # deleting sets which are both inputs and outputs and putting them in the GCC
    check = True
    while check:
        check = False
        for i in wells:
            if i in sources:
              wells.remove(i)
              sources.remove(i)
              gcc.append(i)
              check = True
    
    # accounting for when there is only one GCC
    if len(gcc) == 1:
        if len(gcc[0]) == G.number_of_nodes():
            gcc[0] = gcc[0].tolist()
            
    N = G.number_of_nodes()
    Nsources = [item for source in sources for item in source]
    Nwells = [item for well in wells for item in well]
    
    return N, len(Nsources),len(Nwells)

def import_graph(filename):
    if filename.endswith('.xml'):
        G = igraph.Graph.Read_GraphML(filename)
        return G
    
    elif filename.endswith('.csv'):
        file = open(filename, "r")
        Graphtype = nx.Graph()

        G = nx.parse_edgelist(file, comments='t', delimiter=',', create_using=nx.DiGraph,
                      data=(('weight', float),))
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
        
    print("Warning: the graph type has not been recognized")
    G = nx.DiGraph()
    return G







