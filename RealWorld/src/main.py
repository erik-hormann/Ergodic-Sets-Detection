#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 09:58:05 2021

@author: erikhormann

This program calculates the correlation between four inputs and four outputs
as a function of p/p_c, where p is the parameter of the ER(N,p) core of the graph, 
to which the four synthetic inputs and outputs are attached.
"""
import igraph
import mygraph as myg
import numpy as np
import matplotlib.pyplot as plt
import pickle

#%% Graph generation parameters

std_sources = [[100], [101], [102], [103]]
flat_sources = [item for source in std_sources for item in source]
std_wells = [[104], [105], [106], [107]]
flat_wells = [item for well in std_wells for item in well]

P = [0.015, 0.016, 0.017, 0.018, 0.019, 0.02, 0.022, 0.024, 0.026, 0.028, 0.03, 0.04, 0.05, 0.06]
#
samples = 100

reduced_transmision = np.zeros([len(std_sources), len(std_wells)])

# accumulatore
A_red = np.zeros([len(P),len(std_sources),len(std_wells)])
counts = np.zeros(len(std_sources))

#%% RW for different core connectivities

for k in range(len(P)):
    for j in range(samples):
        p = P[k]
        G = myg.GenerateER_IO(100, p)
        N = G.vcount()
        d = G.diameter()
        # finding the strongly connected components
        [sources, wells, gcc] = myg.FindIO(G)
        
        A = G.get_adjacency()
        A = np.array(A.data)
        A = A + 1e-6*np.eye(G.vcount())
        A = A/A.sum(axis=1)[:,None]  # creating a stochastic matrix
        A = np.linalg.matrix_power(A,100*d)
        
        for i in range(len(std_sources)):
            # initialising x0 as the 1 vector over a source (nput)
            x = np.zeros([G.vcount()])
            x[std_sources[i]] = 1
            # iterating the dynamics
            x = np.matmul(x,A)
            # finding the weight of vector over each well (output)
            if (np.sum(x[flat_wells])!=0):
                x[flat_wells] = x[flat_wells] / np.sum(x[flat_wells])
                A_red[k,i,:] = A_red[k,i,:] + x[flat_wells]
            # no need to sum over vertices i the same output because the planted
            # outputs are all singletons ( to be added here for general case)
            
            #PREVIOUS METHOD
            #if (x[flat_wells]!=0).all():
            #    x[flat_wells] = x[flat_wells] / np.sum(x[flat_wells])
            #    A_red[k,i,:] = A_red[k,i,:] + x[flat_wells]
    A_red[k,:,:] = A_red[k,:,:]/A_red[k,:,:].sum(axis=1)[:,None]

pickle.dump(A_red, open('../data/A_red.dat','wb'))
# myg.GraphPrint(G)

#%% Analyising the reduced matrix

# all unordered correlations pairs
correlations = np.zeros( [ len(P), int( len(std_sources)*(len(sources)-1)/2) ] )

for k in range(len(P)):
    ind = 0
    for j in range(len(std_sources)):
        for i in range(j):
            correlations[k,ind] = np.dot(A_red[k,i,:],A_red[k,j,:]) / np.linalg.norm(A_red[k,i,:]) / np.linalg.norm(A_red[k,j,:]) 
            ind +=1
            
pickle.dump(correlations, open('../data/correlations.dat','wb'))
            
#%% printing
correlations = pickle.load(open('../data/correlations.dat','rb'))
correlations = correlations.transpose()

plt.semilogx(P,np.sum(correlations,axis=0)/6)

#CORRECT, BUT CHECK THE LEGNTH OF correlations ALONG THE FIRST AXIS
#plt.loglog(P,np.sum(correlations,axis=0)/np.shape(correlations)[0])

# PREVIOUS METHOD
#for k in range(len(P)):
#    plt.loglog(P,correlations[k,:],label=str(P[k]))
#plt.legend()

plt.show()
    
    
    
    
    
    