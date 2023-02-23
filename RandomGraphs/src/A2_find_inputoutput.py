#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 10:49:52 2021

@author: erikhormann
"""

import pickle
import igraph
import numpy as np

G = pickle.load(open("../temp/G.dat",'rb'))
diam = G.diameter(directed ='TRUE')
A = G.get_adjacency()
A = np.array(A.data)

# contains all the possible paths of lenght less than or equal to the diameter
A_diam = A
for i in range(1,diam+1):
    A_diam = A_diam + A_diam*A
    A_diam[A_diam > 0] = 1

cl = G.clusters(mode='STRONG')
cl = np.asarray(cl, dtype='object')

wells = []
sources = []

# verify if each element is a source
for start_clus in cl:
    source = True
    for end_clus in cl:
        if end_clus == start_clus:
            continue
        if A_diam[np.ix_(end_clus,start_clus)].any() != 0:
            source = False
    if source:
        sources.append(start_clus)
        
# verify if each element is a well
for end_clus in cl:
    well = True
    for start_clus in cl:
        if end_clus == start_clus:
            continue
        if A_diam[np.ix_(end_clus,start_clus)].any() != 0:
            well = False
    if well:
        wells.append(end_clus)

pickle.dump(wells, open("../temp/wells.dat",'wb'))
pickle.dump(sources, open("../temp/sources.dat",'wb'))