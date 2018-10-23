# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 23:23:20 2018

@author: rajar
"""

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from os import listdir
from os.path import isfile, join

status_assortativities = {}
major_assortativities = {}
onlyfiles = [f for f in listdir('./') if isfile(join('./', f))]
for i in onlyfiles:
    attr = {}
    dict_status = {}
    dict_major = {}
    if i.endswith('_attr.txt'):
        f = open(i,'r')
        next (f)
        count = 1
        for j in f:
            k = j.strip().split('\t')
            attr[count] = [k[0], k[1], k[2], k[3], k[4]]
            count = count + 1
        for k,v in attr.items():
            dict_status[str(k)] = int(v[0])
            dict_major[str(k)] = int(v[2])
        txt_file = i.replace('_attr.txt','.txt')
        G = nx.read_edgelist(txt_file)
        netsize = len(G.nodes())
        nx.set_node_attributes(G, dict_status,'status')
        stat_assort = nx.attribute_assortativity_coefficient(G, 'status')
        nx.set_node_attributes(G, dict_major,'major')
        maj_assort = nx.attribute_assortativity_coefficient(G, 'major')
        status_assortativities[txt_file] = (stat_assort, netsize)
        major_assortativities[txt_file] = (maj_assort, netsize)
        print(txt_file, stat_assort, maj_assort, netsize)
        
x1 = np.zeros((100))
y1 = np.zeros((100))
ind1 = 0
for j in status_assortativities:
    temp1=(status_assortativities[j])
    x1[ind1] = temp1[1]
    y1[ind1] = temp1[0]
    ind1 = ind1+1

#Plotting the Figure showing Status Modularity(Q) 
#vs. Network Size(n)    
plt.scatter(x1,y1, alpha=0.5, color = 'b')
plt.xlabel('Network size, n')
plt.ylabel('Status Modularity, Q')
plt.xscale('log')
plt.xlim((500,50000))
plt.savefig('status_modularity_1.png', dpi = 300)
plt.show() 

plt.hist(y1, normed=True, bins=30)
plt.xlabel('Assortativity (Status)')
plt.ylabel('Density')
plt.savefig('status_modularity_histogram', dpi = 300)
plt.show() 

print('Average Status Modularity:' ,sum(y1)/len(y1)) 


x2 = np.zeros((100))
y2 = np.zeros((100))
ind2 = 0
for j in major_assortativities:
    temp2=(major_assortativities[j])
    x2[ind2] = temp2[1]
    y2[ind2] = temp2[0]
    ind2 = ind2+1

#Plotting the Figure showing Major Modularity(Q) 
#vs. Network Size(n)    
plt.scatter(x2,y2, alpha=0.5, color = 'b')
plt.xlabel('Network size, n')
plt.ylabel('Major Modularity, Q')
plt.xscale('log')
plt.xlim((500,50000))
plt.savefig('major_modularity_1.png', dpi = 300)
plt.show() 

plt.hist(y2, normed=True, bins=30)
plt.xlabel('Assortativity (Major)')
plt.ylabel('Density')
plt.savefig('major_modularity_histogram', dpi = 300)
plt.show() 

print('Average Major Modularity:' ,sum(y2)/len(y2))           