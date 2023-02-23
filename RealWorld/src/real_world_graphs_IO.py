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
models_folder = '../real_world_networks/'
allfiles = [f for f in os.listdir(models_folder) if os.path.isfile(os.path.join(models_folder, f))]
fileslist = list(set(allfiles) - set(['.DS_Store']))

#%% Creating color dictionary
graph_colors = {
    'W_': 'green',
    'T_': 'blue',
    'P_': 'red'
    }

#%% Reading networka

N = []
Nwells = []
Nsources = []
source_colors = []
wells_colors = []

for file in fileslist:
    filepath = models_folder+file
    pointer = filepath.find('orks/')
    color = graph_colors[filepath[pointer+5:pointer+7]]
    source_colors.append(color)
    wells_colors.append('dark'+color)
    G = myg.import_graph(filepath)
    [n, ns, nw] = myg.FindIO_lenght(G)
    N.append(n)
    Nsources.append(ns)
    Nwells.append(nw)
 
#%% Plotting   
 
fig = plt.figure()
plt.scatter(N, Nwells, marker = 'o', label = "Web", c = wells_colors)
plt.scatter(N, Nsources, marker = 'x', label = "Web", c = source_colors)
plt.legend()
plt.xlabel("Total number of vertices")
plt.ylabel("Number of vertices in ergodic sets")

fig = plt.figure()
plt.yscale('log')
plt.scatter(N, Nwells, marker = 'o', label = "Web", c = wells_colors)
plt.scatter(N, Nsources, marker = 'x', label = "Web", c = source_colors)
plt.legend()
plt.xlabel("Total number of vertices")
plt.ylabel("Number of vertices in ergodic sets")


fig = plt.figure()
plt.xscale('log')
plt.scatter(N, Nwells, marker = 'o', label = "Web", c = wells_colors)
plt.scatter(N, Nsources, marker = 'x', label = "Web", c = source_colors)
plt.legend()
plt.xlabel("Total number of vertices")
plt.ylabel("Number of vertices in ergodic sets")


fig = plt.figure()
plt.xscale('log')
plt.yscale('log')
plt.scatter(N, Nwells, marker = 'o', label = "Web", c = wells_colors)
plt.scatter(N, Nsources, marker = 'x', label = "Web", c = source_colors)
plt.legend()
plt.xlabel("Total number of vertices")
plt.ylabel("Number of vertices in ergodic sets")
