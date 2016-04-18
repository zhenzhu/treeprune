"""
Please cite our publication below if using the code:
    Zhu Z, Puliga M, Cerina F, Chessa A, Riccaboni M (2015) 
    Global Value Trees. PLoS ONE 10(5): e0126699. 
    doi:10.1371/journal.pone.0126699

This Python module provides a network-pruning functionality and returns a 
tree with the customized root node, edge weight threshold, maximum number 
of layers, and search direction. 

MIT License
Copyright (c) 2016 Zhen Zhu 
"""

import networkx as nx
import operator
import pygraphviz as pgv




def get_tree(data_path,sep,root,cutoff,layer_max,up=True):
    """
    This function takes the path of a data file of edge list with numeric 
    weights and returns a tree (DiGraph object). The parameters include:
    data_path: The path of a data file of edge list with numeric weights.
    sep: The delimiter of the data file. 
    root: A root node to start with. 
    cutoff: The edge weight threshold. 
    layer_max: The number of layers to explore.
    up: The direction (upstream or downstream) of the tree. 
    The default is upstream.  
    """
    # Read in the network data.
    F = nx.read_weighted_edgelist(data_path,delimiter=sep,create_using=nx.DiGraph())  
    # create_using is to specify a directed network, otherwise, an 
    # undirected network is returned.

    # Filter the edges with the cutoff value.
    G = nx.DiGraph( [ (u,v,d) for u,v,d in F.edges(data=True) if d['weight']>=cutoff] )    

    reachset = set()
    unreachset = set()
    for n in G.nodes():
        if(n != root):
            unreachset.add(n)
        else:
            reachset.add(n)

    H = nx.DiGraph() # Initiate a tree.
    oldreach = len(reachset)
    newreach = oldreach +1
    rndcount = 0

    if(up==True): # When an upstream tree is requested.
        while(newreach>oldreach and rndcount<layer_max):  
            oldreach = len(reachset)
            candidatesIn = {}
            for ee in G.edges(data = True):
                e1 = ee[0]
                e2 = ee[1]
                w = ee[2]['weight']
                if(e2 in reachset and e1 in unreachset): # e2 in reachset because the direction is upstream.
                    candidatesIn[(e1,e2)] = w  
            sorted_edges_in = sorted(candidatesIn.iteritems(), key=operator.itemgetter(1), reverse = True) 
            # reverse = True is to pick the edge with the largest weight 
            # first. Otherwise, the edge with the smallest weight will be 
            # picked first. 
            if(len(sorted_edges_in) > 0):
                for se in sorted_edges_in:
                    if (se[0][0] in unreachset): 
                        # The same candidate node may appear more than once 
                        # connecting with different existing nodes. So 
                        # se[0][0] needs to be checked if still in 
                        # unreachset before being added. This is to ensure 
                        # that all the nodes in the tree are unique. For 
                        # each round/layer of search, the edge with a 
                        # larger weight is preferred.  
                        reachset.add(se[0][0])
                        unreachset.remove(se[0][0])
                        H.add_edge(se[0][0],se[0][1],weight=se[1],layer=rndcount+1) # The edge attribute layer is added. 
                        H.node[se[0][0]]['dist']=rndcount+1 # The node attribute dist (distance from the root) is added.
                        newreach=len(reachset)
            else:
                newreach=oldreach
            rndcount=rndcount+1
        if(H.number_of_nodes()>0): # Error if empty tree. 
            H.node[root]['dist']=0 # Add the attribute dist for the root.

    else: # When a downstream tree is requested. 
        while(newreach>oldreach and rndcount<layer_max):  
            oldreach = len(reachset)
            candidatesOut = {}
            for ee in G.edges(data = True):
                e1 = ee[0]
                e2 = ee[1]
                w = ee[2]['weight']
                if(e1 in reachset and e2 in unreachset): # e1 in reachset because the direction is downstream.
                    candidatesOut[(e1,e2)] = w  
            sorted_edges_out = sorted(candidatesOut.iteritems(), key=operator.itemgetter(1), reverse = True) 
            # reverse = True is to pick the edge with the largest weight 
            # first. Otherwise, the edge with the smallest weight will be 
            # picked first. 
            if(len(sorted_edges_out) > 0):
                for se in sorted_edges_out:
                    if (se[0][1] in unreachset): 
                        # The same candidate node may appear more than once 
                        # connecting with different existing nodes. So 
                        # se[0][1] needs to be checked if still in 
                        # unreachset before being added. This is to ensure 
                        # that all the nodes in the tree are unique. For 
                        # each round/layer of search, the edge with a 
                        # larger weight is preferred.  
                        reachset.add(se[0][1])
                        unreachset.remove(se[0][1])
                        H.add_edge(se[0][0],se[0][1],weight=se[1],layer=rndcount+1) # The edge attribute layer is added. 
                        H.node[se[0][1]]['dist']=rndcount+1 # The node attribute dist (distance from the root) is added.
                        newreach=len(reachset)
            else:
                newreach=oldreach
            rndcount=rndcount+1
        if(H.number_of_nodes()>0): # Error if empty tree. 
            H.node[root]['dist']=0 # Add the attribute dist for the root. 

    return H


def plot_tree(tree,fig_path,layer_space=3,edge_color='crimson'):
    """
    This function returns a tree plot. The parameters include:
    tree: A tree (DiGraph object).
    fig_path: A string of the path saving the plot. 
    layer_space: A parameter controlling the space between layers. 
    The default is 3.
    edge_color: A string of edge color. The default is 'crimson'.
    """
    A = pgv.AGraph(strict=False,directed=True,ranksep=str(layer_space)) # ranksep controls the space between layers.    
    for e in tree.edges(data = True):
        lab0 = e[0]
        lab1 = e[1]
        A.add_edge(lab0,lab1,color=edge_color,arrowhead='open',style='bold') 
        n0 = A.get_node(lab0)
        n1 = A.get_node(lab1)
    A.node_attr['shape']='oval'
    A.node_attr['fixedsize']='true' # This is going to make the node size the same. 
    A.layout(prog='dot')  # This layout will make the tree look. 
    A.draw(fig_path)    



