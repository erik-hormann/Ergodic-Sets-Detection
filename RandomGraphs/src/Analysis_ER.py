#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 19:26:42 2021

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

plt.rc('font', family='serif')

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

graphtype = 'ER'
files_directory  = "../data/Count_IO_" + graphtype + "*"
files = glob.glob(files_directory)
files.sort()


#files.append(files.pop(files.index("../data_step_Mac/Count_IO_"+graphtype+"1000.dat")))

def gcc(x, d, e, g):
    return 1/(1 + np.exp(-e*(x-d)))**g

def tot_vertices(x, c1, c2, c3, c4):
    return np.exp(-c1*x) + 1/(1 + np.exp(-c2*(x-c3)))**c4

fig1 = plt.figure(1)
fig1.set_size_inches(8,6)
plt.title("Average number of ergodic sets for " + graphtype + " graphs")
fig2 = plt.figure(2)
fig2.set_size_inches(8,6)
plt.title("Relative number of vertices in [any] ergodic sets [" + graphtype + " model]")
fig3 = plt.figure(3)
plt.title("Proportion of vertices in the largest ergodic sets [" + graphtype + " model]")
fig3.set_size_inches(8,6)

j = 0
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

sizes = []
decay_factor = []
break_point = []
exp_factor_gcc = []
exp_factor_totvert = []
shift_gcc = []
shift_totvert = []
exp_stretch_gcc = []
exp_stretch_totvert = []

for f in files:
    data = pickle.load(open(f,'rb'))
    N = int(re.findall(r'\d+', f)[0])
    sizes.append(N)
    
    
    x0 = data[0,0]
    x1 = data[-1,0]
    linspace = np.linspace(x0,x1,100)
    
    # Third figure
    plt.figure(3)
    plt.semilogy(data[:,0],data[:,7]/N, 'o', label='N='+str(N), color = colors[j])
    plt.xlabel(r'Relative probability $\left[\frac{p}{p_c}\right]$')
    plt.ylabel(r'Relative size of the strongly giant connected component $\left[\frac{GSCC}{N}\right]$')
    plt.tight_layout()
    
    baseline = 1/N * np.ones(len(data[:,7]))
    excursion = np.absolute(np.subtract(data[:,7]/N,baseline))
    plateau = list( np.where(excursion <= 1/N)[0] )
    growth = list( np.where(excursion > 1/N)[0] )
    
    [d,e,g] = scipy.optimize.curve_fit(gcc, data[growth,0], data[growth,7]/N, p0=[data[plateau[-1],0],5,0], bounds = [[data[plateau[-1],0],-np.inf,-np.inf], [data[plateau[-1],0]+1,np.inf,np.inf]] )[0]
    exp_stretch_gcc.append(g)
    shift_gcc.append(d)
    break_point.append(d)
    exp_factor_gcc.append(e)
    yf = gcc(linspace,d,e,g)
    yf = np.maximum(1/N,yf)
    plt.semilogy(linspace,yf, '--', color = colors[j])
    plt.legend()
    
    # First figure
    plt.figure(1)
    plt.semilogy(data[:,0],data[:,1]/N, '-', label=N)
    plt.xlabel(r'Relative probability $\left[\frac{p}{p_c}\right]$')
    plt.ylabel(r'Relative number of ergodic sets $\left[\frac{ES}{N}\right]$')
    plt.legend()
    
    [a,b,c,z] = scipy.optimize.curve_fit(tot_vertices, data[:,0], data[:,5]/N, p0=[data[plateau[-1],0],3,1,12])[0]
    decay_factor.append(a)
    shift_totvert.append(c)
    exp_stretch_totvert.append(z)
    exp_factor_totvert.append(b)
    yf = tot_vertices(linspace,a,b,c,z)
    
    # Second figure
    plt.figure(2)
    plt.plot(data[:,0],data[:,5]/N, 'o', label='N='+str(N), color = colors[j])
    plt.legend()
    plt.xlabel(r'Relative probability $\left[\frac{p}{p_c}\right]$')
    plt.ylabel(r'Percentage of vertices in any ergodic set $\left[\frac{NES}{N}\right]$')
    plt.tight_layout()
    plt.semilogy(linspace,yf, '--', color = colors[j])
    
    
    j+=1
   
plt.show()

#%% Fit parameters plotting
plt.plot(sizes,decay_factor,'o', label = r'$\alpha$ from ES')
plt.title("Exponential decay factor for the number of vertices in any ES[" + graphtype + "]")
plt.xlabel("Network size [N]")
plt.ylabel(r'$\alpha$')
plt.legend()
plt.show()

plt.title("Exponential stretch factor for the fit [" + graphtype + "]")
plt.xlabel("Network size [N]")
plt.ylabel(r'$\delta$')
plt.semilogy(sizes,exp_stretch_gcc,'o', label = r'$\delta$ from NES')
plt.semilogy(sizes,exp_stretch_totvert,'<', label = r'$\delta$ from GSCC')
plt.legend()
plt.show()

plt.title("Exponential shift for the fit [" + graphtype + "]")
plt.xlabel("Network size [N]")
plt.ylabel(r'$\gamma$')
plt.plot(sizes,shift_gcc,'o', label = r'$\gamma$ from NES')
plt.plot(sizes,shift_totvert,'<', label = r'$\gamma$ from GSCC')
plt.legend()
plt.show()

plt.title("Exponential prefactor for the fit [" + graphtype + "]")
plt.xlabel("Network size [N]")
plt.ylabel(r'$\beta$')
plt.plot(sizes,exp_factor_gcc,'o', label = r'$\beta$ from NES')
plt.plot(sizes,exp_factor_totvert,'<', label = r'$\beta$ from GSCC')
plt.legend()
plt.show()

plt.title("Percolation threshold for for the GCC [" + graphtype + "]")
plt.xlabel("Network size [N]")
plt.ylabel(r'Plateu end [$p/p_c$]')
plt.plot(sizes,break_point,'o')
plt.show()


plt.title("Exponential stretch factor for the fit [" + graphtype + "]")
plt.xlabel("Network size [N]")
plt.ylabel(r'$\delta$')
plt.plot(sizes,exp_stretch_gcc,'o', label = r'$\delta$ from (1)')
plt.legend()
plt.show()


plt.title("Exponential shift for the fit [" + graphtype + "]")
plt.xlabel("Network size [N]")
plt.ylabel(r'$\gamma$')
plt.plot(sizes,shift_gcc,'o', label = r'$\gamma$ from (1)')
plt.legend()
plt.show()


