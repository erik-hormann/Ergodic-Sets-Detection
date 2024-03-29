#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 14:46:40 2021

@author: erikhormann

This code takes all the files in the folder "real_world_graphs"
and performs the calculations of the ergodic sets. It plots the
logarithmic plot of the wells and sources in each of the
networks, including the trivial one-node ergodic sets.
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

#%% Creating color dictionary
graph_colors = {
    'W_': 'blue',
    'T_': 'red',
    'E_': 'orange',
    'B_': 'green'
    }

# checking if sims exist
sims_exist = False
sims_path = "../results/"

if os.path.exists(sims_path + "N.dat") and os.path.exists(sims_path + "E.dat") and os.path.exists(sims_path + "Nsources.dat")  and  os.path.exists(sims_path + "wells_colors.dat") and  os.path.exists(sims_path + "source_colors.dat"):
    sims_exist = True

#%% Reading network


if not sims_exist:

    N = []
    E = []
    Nwells = []
    Nsources = []
    source_colors = []
    wells_colors = []

    for file in fileslist:
        filepath = models_folder+file
        pointer = filepath.find('orks/')
        # following line to use only in tests, for graphs in the main folder
        # color = graph_colors[filepath[pointer + 5:pointer + 7]]
        # following line to use for running, for graphs in the validated folder
        color = graph_colors[filepath[pointer+15:pointer+17]]
        source_colors.append(color)
        wells_colors.append('dark'+color)
        G = myg.import_graph(filepath)
        [ns, nw, n, un] = myg.FindIO_lenght(G)
        if ns+nw+n+un != G.number_of_nodes():
            warnings.warn("Not all nodes accounted for in file" + str(file) + "\nNodes = " + str(G.number_of_nodes()) + "\n ES + GCC = " + str(n+ns+nw))
        nn = G.number_of_nodes()
        e = G.number_of_edges()
        N.append(nn)
        E.append(e)
        Nsources.append(ns)
        Nwells.append(nw)

if sims_exist:
    N = pickle.load(open("../results/N.dat", "rb"))
    E = pickle.load(open("../results/E.dat", "rb"))
    Nsources = pickle.load(open("../results/Nsources.dat", "rb"))
    Nwells = pickle.load(open("../results/Nwells.dat", "rb"))
    wells_colors = pickle.load(open("../results/wells_colors.dat", "rb"))
    source_colors = pickle.load(open("../results/source_colors.dat", "rb"))
    ns = pickle.load(open("../results/ns.dat", "rb"))
#%% Plotting

line = [0.1*min(N), max(N)*10]

fig = plt.figure()
plt.xscale('log')
plt.yscale('log')
plt.ylim((2, 6000))
plt.xlim((8/10*min(N),max(N)*10/8))
plt.scatter(N, Nwells, marker = 'o', label = "Outputs", c = wells_colors)
plt.scatter(N, Nsources, marker = 'x', label = "Inputs", c = source_colors)
plt.plot(line, line, 'k--')
plt.title("Input/outputs in original networks")
plt.xlabel("Total number of vertices")
plt.ylabel("Number of vertices in ergodic sets")
plt.savefig('../figures/realWorldLogLog.png', format='png', dpi=300)
plt.savefig('../figures/realWorldLogLog.svg', format='svg')
plt.savefig('../figures/realWorldLogLog.eps', format='eps')
plt.show()

#%% Saving

pickle.dump(N, open("../results/N.dat", "wb"))
pickle.dump(E, open("../results/E.dat", "wb"))
pickle.dump(Nsources, open("../results/Nsources.dat", "wb"))
pickle.dump(Nwells, open("../results/Nwells.dat", "wb"))
pickle.dump(wells_colors, open("../results/wells_colors.dat", "wb"))
pickle.dump(source_colors, open("../results/source_colors.dat", "wb"))
pickle.dump(ns, open("../results/ns.dat", "wb"))