#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 10:12:06 2021

@author: erikhormann

This program loads the data of all the simulations created by the 
<Count_IO_ER> code, plot them together [number of vertices in an E.S vs p/pc]
and calculate the minimum of such distribution as a function of the number of 
vertices of the graph.
"""

import glob
import pickle
import matplotlib.pyplot as plt
import re #for searching strings
import numpy as np
import scipy.optimize

# Results:
    # results[:,0] --> probability p/pc
    # results[:,1] --> number of inmput
    # results[:,2] --> std of #imputs
    # results[:,3] --> number of outputs
    # results[:,4] --> std od #outputs
    # results[:,5] --> #vertices in input sets
    # results[:,6] --> #vertices in output sets
    # results[:,7] --> #vertices in the single largest input set
    # results[:,8] --> #vertices in the single largest output set

graphtype = 'SBM'
files_directory  = "../data_step_Mac/Count_IO_" + graphtype + "*"
files = glob.glob(files_directory)
files.sort()

def tot_vertices(x, c1, c2, c3):
    return np.exp(-c1*x) + 1/( 1 + np.exp(-c3*(x-c2)) ) 

def gcc(x, d, e, g):
    return 1/(1 + np.exp(-e*(x-d)))**g
    
fig1 = plt.figure(1)
plt.title("Average number of ergodic sets for " + graphtype + " graphs")
fig2 = plt.figure(2)
plt.title("Total number of vertices in ergodic sets [" + graphtype + " model]")
fig3 = plt.figure(3)
plt.title("Proportion of vertices in the largest ergodic sets [" + graphtype + " model]")

for f in files:
    data = pickle.load(open(f,'rb'))
    N = int(re.findall(r'\d+', f)[0])
    
    # First figure
    plt.figure(1)
    plt.semilogy(data[:,0],data[:,1]/N, label=N)
    plt.xlabel('p/p_c')
    plt.legend()
    
    [a,b,c] = scipy.optimize.curve_fit(tot_vertices, data[:,0], data[:,5]/N, p0=[1,7,1])[0]
    yf = tot_vertices(data[:,0],a,b,c)
    
    # Second figure
    plt.figure(2)
    plt.semilogy(data[:,0],data[:,5]/N, label=N)
    plt.legend()
    plt.xlabel('p/p_c')
    plt.tight_layout()
    plt.semilogy(data[:,0],yf, '--o')
    
    # Third figure
    plt.figure(3)
    plt.plot(data[:,0],data[:,7]/N, label=N)
    plt.xlabel('p/p_c')
    plt.tight_layout()
    
    baseline = 1/N * np.ones(len(data[:,7]))
    excursion = np.absolute(np.subtract(data[:,7]/N,baseline))
    plateau = list( np.where(excursion <= 1/N/2)[0] )
    growth = list( np.where(excursion > 1/N/2)[0] )
    
    [d,e,g] = scipy.optimize.curve_fit(gcc, data[growth,0], data[growth,7]/N, p0=[plateau[-1],5,10])[0]
    yf_plateau = 1/N * np.ones(len(plateau))
    yf_growth = gcc(data[growth,0], d, e, g)
    yf = np.concatenate((yf_plateau,yf_growth))
    plt.plot(data[:,0],yf, '--o', label = "fit_"+str(N))
    plt.legend()
   
plt.show()