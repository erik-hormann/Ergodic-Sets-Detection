#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 20:57:51 2021

@author: erikhormann
"""

import numpy as np
import networkx as nx
import scipy.sparse

def microcanonical_SBM(n,m):
    '''
    n = [n_r] = #nodes in group r
    m = [[m_rs]] = #edges between groups r,s
    '''

    num_groups = len(n)

    G = nx.Graph()
    groups = []
    i = 0
    for r in range(num_groups):
        groups.append([])
        for j in range(n[r]):
            G.add_node(i, group=r)
            groups[r].append(i)
            i += 1

    for r in range(num_groups):
        for s in range(r,num_groups):
            m_rs = m[r][s]
            while m_rs > 0:
                i,j = 0,0
                while (i==j) or (G.has_edge(i,j)):
                    i = np.random.choice(groups[r])
                    j = np.random.choice(groups[s])
                G.add_edge(i,j)
                m_rs -= 1

    return G


def microcanonical_SBM_routine(N,E,p_n,p_e):
    
    if (E % 2 != 0):
        raise "Error, the number of edges must be divisible by 2"

    N = int(N)
    
    X = [int(p_n * N), N - int(p_n * N)]
    
    m11 = m22 = int(p_e * E / 2)
    E = E - m11 - m22
    m21 = m12 = E
    
    E = np.array([[m11, m12], [m21, m22]])
    
    H = microcanonical_SBM(X, E)
    
    return H

def random_walk_matrix(G):
    n = G.number_of_nodes()
    W = np.zeros((n,n))
    for i,j in G.edges():
        W[i,j] = 1./G.degree(j)
        W[j,i] = 1./G.degree(i)
    return scipy.sparse.csc_matrix(W)

def zero_column(W, i):
    ans = W.copy()
    for j in W[:,i].nonzero()[0]:
        ans[j,i] = 0
    return ans

def return_pdf(W, i, trunc):
    ans = np.zeros(trunc)
    n = W.shape[0]
    x = np.zeros(n)
    x[i] = 1.
    x = W.dot(x)
    W_i = zero_column(W,i)
    for t in range(1,trunc):
        ans[t] = x[i]
        x = W_i.dot(x)
    return ans

def neighbourlist(G):
    N = G.vcount()
    neigh = {}
    for i in range(N):
        temp = G.neighbors(i, mode="out")
        neigh[i] = np.asarray(temp)
    
    return neigh