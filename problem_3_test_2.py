# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 20:30:51 2018

@author: rajar
"""

import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community.quality import modularity
from sklearn.metrics.cluster import normalized_mutual_info_score

G = nx.read_adjlist('karate_edges_77.txt')

# Let each node in the graph be in its own community
communities = list()    
for i in G.nodes():
    communities.append(set([i]))
    
# Create a list for keeping track of all merges
tracking_merges = list()

modnew = modularity(G, communities)
print ('The modularity at the beginning is',modnew)
modold = None
comtrial = []
modtrial = 0
num_of_merges = 0
num_merges = []
modularity_scores = []

# Maximizing the modularity to find the best social parition
while (modold is None or modnew > modold):
    comtrial = list(communities)
    modold = modnew
    #print('The current modularity is', modold)
    to_be_merged = None
    for i, x in enumerate(communities):
        for j, y in enumerate(communities):
            if (j <= i or len(x) == 0 or len(y) == 0):
                continue
            comtrial[i] = set([])
            comtrial[j] = x | y
            modtrial = modularity(G, comtrial)
            #dq = modold - modtrial
            #all_dqs.append(dq)
            if (modtrial - modnew >= 0):
                if (modtrial - modnew > 0):
                    modnew = modtrial
                    #print ('Trial Modularity',modnew)
                    to_be_merged = (i, j, modnew - modold)
                elif (to_be_merged and
                    min(i, j) < min(to_be_merged[0], to_be_merged[1])):
                        modnew = modtrial
                        #print ('Trial Modularity',modnew)
                        to_be_merged = (i, j, modnew - modold)
            comtrial[i] = x
            comtrial[j] = y
    if (to_be_merged is not None):
        tracking_merges.append(to_be_merged)
        i, j, dq = to_be_merged
        x = communities[i]
        y = communities[j]
        communities[i] = set([])
        communities[j] = x | y
    #print('Old Modularity', modold)
    #print('New Modularity', modnew)
    #print(modularity(G,communities))
    num_of_merges += 1
    num_merges.append(num_of_merges)
    modularity_scores.append(modnew)
    
communities = [c for c in communities if len(c) > 0]                   
                
print(communities)

#Plotting the modularity score Q as a function of the number of merges.
x = num_merges
y = modularity_scores

plt.scatter(x,y, alpha=0.5, color = 'b')
plt.xlabel('Number of merges')
plt.ylabel('Modularity score')
plt.savefig('Mod_score_vs_num_merges.png', dpi = 300)
plt.show() 

print(len(communities))

pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos,
                       nodelist=['3', '13', '4', '14', '8', '22', '2', 
                                 '10', '18'],
                       node_color='r',
                       node_size=500,
                       alpha=0.8)

nx.draw_networkx_nodes(G, pos,
                       nodelist=['17', '6', '12', '20', '1', '7', '11',
                                 '5'],
                       node_color='b',
                       node_size=500,
                       alpha=0.8)

nx.draw_networkx_nodes(G, pos,
                       nodelist=['9', '23', '21', '28', '29', '24', '30', 
                                 '31', '34', '33', '32', '26', '19', '27',
                                 '25', '16', '15'],
                       node_color='g',
                       node_size=500,
                       alpha=0.8)

plt.axis('off')

nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

# Creating the labels
labels = {}
for i in range(1,35):
    labels[str(i)] = r'$' + str(i) + '$'
nx.draw_networkx_labels(G, pos, labels, font_size=16)
plt.savefig('networkvis_maxmodpartition', dpi = 300)
plt.show()

# Finding the normalized mutual information (NMI) between my partition 
# and the social partition
nmi = normalized_mutual_info_score([1,1,1,1,1,1,1,1,1,2,1,
                              1,1,1,2,2,1,1,2,1,2,1,
                              2,2,2,2,2,2,2,2,2,2,2,
                              2], 
                             [2,1,1,1,2,2,2,1,3,1,2,
                              2,1,1,3,3,2,1,3,2,3,1,
                              3,3,3,3,3,3,3,3,3,3,3,
                              3])

print (nmi)


