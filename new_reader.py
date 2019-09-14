
from __future__ import division
import sys, os


import pandas as pd
import matplotlib as mpl


import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from nxviz import ArcPlot
from nxviz import CircosPlot


# Define maximal_cliques()
def maximal_cliques(G, size):
    """
    Finds all maximal cliques in graph `G` that are of size `size`.
    """
    mcs = []
    for clique in nx.find_cliques(G):
        if len(clique) == size:
            mcs.append(clique)
    return mcs


# Define get_nodes_and_nbrs()
def get_nodes_and_nbrs(G, nodes_of_interest):
    """
    Returns a subgraph of the graph `G` with only the `nodes_of_interest` and their neighbors.
    """
    nodes_to_draw = []

    # Iterate over the nodes of interest
    for n in nodes_of_interest:

        # Append the nodes of interest to nodes_to_draw
        nodes_to_draw.append(n)

        # Iterate over all the neighbors of node n
        for nbr in G.neighbors(n):

            # Append the neighbors of n to nodes_to_draw
            nodes_to_draw.append(n)

    return G.subgraph(nodes_to_draw)

def di_graph_loader(nodes,edges):
	G = nx.Graph()
		# Add nodes from each of the partitions
	G.add_nodes_from(nodes)
	edges_sets = []
	# Add in each edge along with the date the edge was created
	for r, d in edges.iterrows():
		G.add_edge(d['node1'],d['node2']) 

	return G

def graph_loader(nodes,edges):
	G = nx.Graph()
		# Add nodes from each of the partitions
	G.add_nodes_from(nodes)
	edges_sets = []
	# Add in each edge along with the date the edge was created
	for r, d in edges.iterrows():
		if set([d['node1'],d['node2']]) not in edges_sets:
			G.add_edge(d['node1'],d['node2']) 
			edges_sets.append(set([d['node1'],d['node2']]))

	return G

# Define find_nodes_with_highest_deg_cent()
def deg_cent(G):

    # Compute the degree centrality of G: deg_cent
    deg_cent = nx.degree_centrality(G)

    return deg_cent


# Define find_nodes_with_highest_deg_cent()
def bet_cent(G):

    # Compute the betweenness centrality  of G: deg_cent
    bet_cent = nx.betweenness_centrality(G)

    return bet_cent


# Define find_nodes_with_highest_deg_cent()
def eig_cent(G):

    # Compute the eigenvector centrality of G: eig_cent
	eig_cent = nx.eigenvector_centrality(G)
	return eig_cent


# Define page_rank()
def page_rank(G):

    # Compute the page_rank  of G: pagerank
	pagerank = nx.pagerank(G)
	return pagerank


def main():
	print('Start csv loading process..', end='')
	nodes = pd.read_csv('nodes_full.csv')
	nodes = pd.DataFrame(nodes['node'], columns=['node'])

	node1 = []
	node2 = []
	edges = []
	edges = pd.read_csv('edges_full.csv')
	print(' Done!')

 	

	'''
	----------------

	'''
	print('Start pandas to nx loading process..', end='')
	G = di_graph_loader(nodes['node'],edges[['node1','node2']])
	print('Done!')
	

	print('Start page_rank', end='')
	page = page_rank(G)
	page_df = pd.DataFrame(list(page.items()), columns=['node','page_rank'])
	page_df.to_csv('page_rank.csv')
	print("Done")



	# print('Start degree calc..', end='')
	# degree = deg_cent(G)
	# degree_df = pd.DataFrame(list(degree.items()), columns=['node','degree'])
	# print(degree_df.head())
	# degree_df.to_csv('degree_centrality.csv')
	# print('Done')

	# print('Start betweenness calc..', end='')
	# betweenness = bet_cent(G)
	# betweenness_df = pd.DataFrame(list(betweenness.items()), columns=['node','betweenness'])
	# betweenness_df.to_csv('betweenness_centrality.csv')
	# print('Done')



	# print('Start eigenvector calc..', end='')
	# eigenvector = eig_cent(G)
	# eigenvector_df = pd.DataFrame(list(eigenvector.items()), columns=['node','eigenvector'])
	# eigenvector_df.to_csv('eigenvector_centrality.csv')
	# print('Done')
	# print('All shit done')
	
	


if __name__ == "__main__":
	main()

