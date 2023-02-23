#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 12:46:48 2021

@author: erikhormann
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 16:46:03 2021

@author: erikhormann

This program counts the number of inputs/outputs in a synthetic Barabasi-Albert
graph. The graphs are created in the BA(N,M) form. 
Many values of the probabilty p around the critical probability p_c are tested
and many samples of ER graphs are created for each instance of p. The number of
inputs and outputs are then averaged across the samples for each value of p.
"""

import igraph
# import mygraph_library as mygraph

import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
import scipy.optimize

import pickle

# checking for igraph to be installed correctly
print("igraph running... version: " + igraph.__version__)

N = 500

samples = 30  # number of graphs at each parameters
alphas = [1,2,3,5,6,8,10,12,16,24,32,48,64,81,100,128,256,512,1000]


p_bar = tqdm(total = samples*len(alphas), position=0, leave=True)

results = np.zeros([len(alphas),5])

for j in range(len(alphas)):
    M = alphas[j]
    res = {}
    res[0] = []
    res[1] = []
    
    for i in range(samples):
        p_bar.update()
        G = igraph.Graph.Barabasi(N,M, directed='TRUE')
            
            
        # Plotting graph
        my_layout = G.layout("lgl")
        visual_style = {"bbox": (1000, 1000), "vertex_size": 20, "vertex_label": list(range(N)),
                        "edge_arrow_width": 1, "vertex_color": "white", "edge_width": 2, "layout": my_layout}
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
                
        res[0].append(len(sources))
        
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
        
        res[1].append(len(wells))
    
    results[j][0] = M
    results[j][1] = np.average(res[0])
    results[j][2] = np.std(res[0])
    results[j][3] = np.average(res[1])
    results[j][4] = np.std(res[1])
    
p_bar.close()
savefile = "../data/Count_IO_BA"+str(N)+".dat"
pickle.dump(results,open(savefile,'wb'))

#%% Plotting
savefile = "../data/Count_IO_BA"+str(N)+".dat"
results = pickle.load(open(savefile,'rb'))

plt.semilogx(results[:,0],results[:,1], label='inputs')
plt.title("Average number of ergodic sets for Barabasi-Albert graphs")
plt.xlabel('M/N')
#plt.plot(results[:,0],results[:,3], label='outputs')

x = results[:,0]
y = results[:,1]

# fitting
# objective function
def f(x, a, b, c):
	return a*np.exp(-b*x) + c

#[a,b,c] = scipy.optimize.curve_fit(f, x, y, p0=[1,1,10])[0]
#yf = f(x,a,b,c)
#plt.loglog(x,yf,'--',label='fit')
plt.legend()

# stringtext = "N="+str(N)+"\nFit function: a * exp(-bx) + c\nFit values:\na=" + f'{a:6.2f}' + "\nb=" + f'{b:6.2f}' + "\nc=" + f'{c:6.2f}'

#plt.text(0.1,1,stringtext)
plt.show()