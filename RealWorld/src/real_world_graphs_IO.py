#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 14:46:40 2021

@author: erikhormann
"""

import mygraph as myg
import matplotlib.pyplot as plt
import os
import networkx as nx

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

#%% Reading networka

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
    [n, ns, nw] = myg.FindIO_lenght(G)
    e = G.number_of_edges()
    N.append(n)
    E.append(e)
    Nsources.append(ns)
    Nwells.append(nw)
 
#%% Plotting   
 
# fig = plt.figure()
# plt.scatter(N, Nwells, marker = 'o', label = "Outputs", c = wells_colors)
# plt.scatter(N, Nsources, marker = 'x', label = "Inputs", c = source_colors)
# plt.legend()
# plt.xlabel("Total number of vertices")
# plt.ylabel("Number of vertices in ergodic sets")
# plt.show()
#
# fig = plt.figure()
# plt.yscale('log')
# plt.scatter(N, Nwells, marker = 'o', label = "Outputs", c = wells_colors)
# plt.scatter(N, Nsources, marker = 'x', label = "Inputs", c = source_colors)
# plt.legend()
# plt.xlabel("Total number of vertices")
# plt.ylabel("Number of vertices in ergodic sets")
# plt.show()
#
# fig = plt.figure()
# plt.xscale('log')
# plt.scatter(N, Nwells, marker = 'o', label = "Outputs", c = wells_colors)
# plt.scatter(N, Nsources, marker = 'x', label = "Inputs", c = source_colors)
# plt.legend()
# plt.xlabel("Total number of vertices")
# plt.ylabel("Number of vertices in ergodic sets")
# plt.show()

fig = plt.figure()
plt.xscale('log')
plt.yscale('log')
plt.scatter(N, Nwells, marker = 'o', label = "Outputs", c = wells_colors)
plt.scatter(N, Nsources, marker = 'x', label = "Inputs", c = source_colors)
plt.legend()
plt.xlabel("Total number of vertices")
plt.ylabel("Number of vertices in ergodic sets")
plt.show()

fig = plt.figure()
plt.xscale('log')
plt.yscale('log')
plt.scatter(E, Nwells, marker = 'o', label = "Outputs", c = wells_colors)
plt.scatter(E, Nsources, marker = 'x', label = "Inputs", c = source_colors)
plt.legend()
plt.xlabel("Total number of edges")
plt.ylabel("Number of vertices in ergodic sets")
plt.show()