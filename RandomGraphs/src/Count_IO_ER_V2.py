#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jun 10 10:08:18 2021

@author: erikhormann

This program counts the number of inputs/outputs in a synthetic Erdos-Renyi graph
The graphs are created in the ER(N,p) form. 
Many values of the probabilty p around the critical probability p_c are tested
and many samples of ER graphs are created for each instance of p. The number of
inputs and outputs are then averaged across the samples for each value of p.
"""
#%% Importing packages
import igraph
# import mygraph_library as mygraph

import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
import scipy.optimize

import pickle

#%% Setting up

# checking for igraph to be installed correctly
print("igraph running... version: " + igraph.__version__)

N = 100
p0 = 1/N

samples = 1000  # number of graphs at each parameters
probabilities = p0 * np.arange(0.01, 10, .4)

p_bar = tqdm(total = samples*len(probabilities), position=0, leave=True)

results = np.zeros([len(probabilities),9])
# Results:
    # results[:,0] --> probability p/pc
    # results[:,1] --> number of inmput
    # results[:,2] --> std of #imputs
    # results[:,3] --> number of outputs
    # results[:,4] --> std od #outputs
    # results[:,5] --> #vertices in input sets
    # results[:,6] --> #vertices in output sets
    # results[:,7] --> #vertices in he single largest output set
    # results[:,8] --> #vertices in he single largest output set

for j in range(len(probabilities)):
    p = probabilities[j]
    
    temp_res = {}
    temp_res[0] = []
    temp_res[1] = []
    temp_res[2] = []
    temp_res[3] = []
    temp_res[4] = []
    temp_res[5] = []
    
    for i in range(samples):
        p_bar.update()
        G = igraph.Graph.Erdos_Renyi(N,p, directed='TRUE')
            
            
        # Plotting graph
        #my_layout = G.layout("lgl")
        #visual_style = {"bbox": (1000, 1000), "vertex_size": 20, "vertex_label": list(range(N)), "edge_arrow_width": 1, "vertex_color": "white", "edge_width": 2, "layout": my_layout}
        #igraph.plot(G, **visual_style).show()
        
        
        #%% Finiding the inputs and outputs
        
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
                if np.array_equal(end_clus, start_clus):
                    continue
                if A_diam[np.ix_(list(end_clus),list(start_clus))].any() != 0:
                    source = False                
            if source:
                sources.append(start_clus)
                
        temp_res[0].append(len(sources))
        temp_res[2].append( sum( [len(source) for source in sources] ) )
        temp_res[4].append( max( [len(source) for source in sources] ) )
        
        # verify if each element is a well
        for end_clus in cl:
            well = True
            for start_clus in cl:
                if np.array_equal(end_clus, start_clus):
                    continue
                if A_diam[np.ix_(list(end_clus),list(start_clus))].any() != 0:
                    well = False
            if well:
                wells.append(end_clus)
        
        temp_res[1].append(len(wells))
        temp_res[3].append( sum( [len(well) for well in wells] ) )
        temp_res[5].append( max( [len(well) for well in wells] ) )
        
    results[j][0] = p/p0
    results[j][1] = np.average(temp_res[0])
    results[j][2] = np.std(temp_res[0])
    results[j][3] = np.average(temp_res[1])
    results[j][4] = np.std(temp_res[1])
    results[j][5] = np.average(temp_res[2])
    results[j][6] = np.average(temp_res[3])
    results[j][7] = np.average(temp_res[4])
    results[j][8] = np.average(temp_res[5])
    
    
p_bar.close()
savefile = "../data/Count_IO_ER"+str(N)+".dat"
pickle.dump(results,open(savefile,'wb'))

#%% Plotting
savefile = "../data/Count_IO_ER"+str(N)+".dat"
results = pickle.load(open(savefile,'rb'))

figname = "../figures/ER_N"+str(N)

#PLOT 1 - number of ergodic sets

plt.semilogy(results[:,0],results[:,1]/N, label='inputs')
plt.title("Average number of ergodic sets for Erdös-Renyi graphs")
plt.xlabel('p/p_c')
plt.semilogy(results[:,0],results[:,3]/N, label='outputs')

x = results[:,0]
y = results[:,1]

# fitting
# objective function
def f(x, a, b, c):
	return a*np.exp(-b*x) + c

[a,b,c] = scipy.optimize.curve_fit(f, x, y, p0=[1,1,10])[0]
yf = f(x,a,b,c)
plt.semilogy(x,yf/N,'--',label='fit')
plt.legend()

stringtext = "N="+str(N)+"\nFit function: a * exp(-bx) + c\nFit values:\na=" + f'{a:6.2f}' + "\nb=" + f'{b:6.2f}' + "\nc=" + f'{c:6.2f}'


plt.text(results[0,0],results[-1,1]/N,stringtext)
plt.tight_layout()
plt.savefig(figname+"_Nsets.svg")
plt.show()

# PLOT 2 - total number of vertices in ergodic sets

plt.plot(results[:,0],results[:,5]/N, label='inputs')
plt.plot(results[:,0],results[:,6]/N, label='outputs')
plt.title("Total number of vertices in ergodic sets [ER model] for N="+ str(N))
plt.legend()
plt.xlabel('p/p_c')
plt.tight_layout()
plt.savefig(figname+"_ESvertices.svg")
plt.show()

# PLOT 3 - number of vertices in largest ergodic sets

plt.plot(results[:,0],results[:,7]/N, label='inputs')
plt.plot(results[:,0],results[:,8]/N, label='outputs')
plt.title("Propotion of vertices in the largest ergodic sets [ER model] for N="+ str(N))
plt.legend()
plt.xlabel('p/p_c')
plt.tight_layout()
plt.savefig(figname+"_gcc.svg")
plt.show()
