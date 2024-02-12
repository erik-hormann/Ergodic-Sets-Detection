#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 14:46:40 2021

@author: erikhormann

This code takes all the files in the folder "real_world_graphs"
and performs 100 rewiring of the graphs. It plots the size of
the largest ergodic set (wells) in the original graph
and the size of the largest erdgodic sett (wells) in
each of the rewiring.
"""

import mygraph as myg
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
import numpy as np
import pickle
import networkx as nx
import warnings


#%%
models_folder = '../real_world_networks/Validated/'
# models_folder = '../real_world_networks/'
allfiles = [f for f in os.listdir(models_folder) if os.path.isfile(os.path.join(models_folder, f))]
fileslist = list(set(allfiles) - set(['.DS_Store']))

#%% Reading network

for file in fileslist:
    print(file)
    filepath = models_folder+file
    pointer = filepath.find('orks/')
    # following line to use only in tests, for graphs in the main folder
    # color = graph_colors[filepath[pointer + 5:pointer + 7]]
    # following line to use for running, for graphs in the validated folder
    G = myg.import_graph(filepath)
    if G.number_of_nodes() < 2000:
        nRewires = 100
    else:
        nRewires = 20
    in_degree = [d for n, d in G.in_degree()]
    out_degree = [d for n, d in G.out_degree()]
    [ns, nw, n, un] = myg.FindIO(G)
    # plt.hist([len(i) for i in ns])
    # plt.title(file)
    # plt.show()
    plt.plot(np.max([len(i) for i in ns]),'o',color='green')
    maxW = []
    maxS = []
    avgW = []
    avgS = []

    for i in range(nRewires):
        H = nx.directed_configuration_model([i for i in in_degree], [j for j in out_degree])
        [ns, nw, n, un] = myg.FindIO(H)
        maxW.append(np.max([len(i) for i in ns]))
        maxS.append(np.max([len(i) for i in nw]))
        avgW.append(np.mean([len(i) for i in ns]))
        avgS.append(np.mean([len(i) for i in nw]))
    plt.plot(maxW, label=file)
    plt.title(file)
    plt.show()