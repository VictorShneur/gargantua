
from __future__ import division
import sys, os

# sys.path.append(os.path.expanduser("/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/networkx"))
# sys.path.append(os.path.expanduser('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/nxviz'))
# print(sys.path)
import pandas as pd
import matplotlib as mpl
# %matplotlib inline

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from nxviz import ArcPlot
from nxviz import CircosPlot
from matplotlib.collections import LineCollection


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
def find_nodes_with_highest_deg_cent(G):

    # Compute the degree centrality of G: deg_cent
    deg_cent = nx.degree_centrality(G)

    # Compute the maximum degree centrality: max_dc
    max_dc = sorted(list(deg_cent.values()), reverse=True)[:30]

    nodes = set()

    # Iterate over the degree centrality dictionary
    for k, v in deg_cent.items():

        # Check if the current value has the maximum degree centrality
        if v in max_dc:

            # Add the current node to the set of nodes
            nodes.add(k)

    return nodes


# Define find_nodes_with_highest_deg_cent()
def find_nodes_with_highest_bet_cent(G):

    # Compute the degree centrality of G: deg_cent
    bet_cent = nx.betweenness_centrality(G)

    # Compute the maximum degree centrality: max_dc
    max_bc = sorted(list(bet_cent.values()), reverse=True)[:30]

    nodes = set()

    # Iterate over the degree centrality dictionary
    for k, v in bet_cent.items():

        # Check if the current value has the maximum degree centrality
        if v in max_bc:

            # Add the current node to the set of nodes
            nodes.add(k)

    return nodes


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
	# print(len(G.nodes()))
	# print(len(G.edges()))
	# print(top_dc)
	print('Done!')
	# m_c = maximal_cliques(G, 5)
	print('Start interest graph searching..', end='')
	top_dc = find_nodes_with_highest_bet_cent(G)
	# Extract the subgraph with the nodes of interest: T_draw
	G_draw = get_nodes_and_nbrs(G, top_dc)
	print('Done!')

	# # Draw the subgraph to the screen
	# nx.draw(G_draw)
	# plt.show()


	# # Compute the betweenness centrality of T: bet_cen
	# bet_cen = nx.betweenness_centrality(G_draw)

	# # Compute the degree centrality of T: deg_cen
	# deg_cen = nx.degree_centrality(G_draw)
	# _ = plt.figure()
	# # Create a scatter plot of betweenness centrality and degree centrality
	# plt.scatter(list(bet_cen.values()),list(deg_cen.values()))

	# # Display the plot
	# plt.show()	
	pos = nx.layout.spring_layout(G_draw)

	node_sizes = [3 + 10 * i for i in range(len(G_draw))]
	M = G_draw.number_of_edges()
	edge_colors = range(2, M + 2)
	edge_alphas = [(5 + i) / (M + 4) for i in range(M)]

	nodes_i = nx.draw_networkx_nodes(G_draw, pos, node_size=node_sizes, node_color='blue')
	edges_i = nx.draw_networkx_edges(G_draw, pos, node_size=node_sizes, arrowstyle='->',
	                               arrowsize=10, edge_color=edge_colors,
	                               edge_cmap=plt.cm.Blues, width=2)
	# set alpha value for each edge
	for i in range(M):
	    edges_i[i].set_alpha(edge_alphas[i])

	pc = mpl.collections.PatchCollection(edges_i, cmap=plt.cm.Blues)
	pc.set_array(edge_colors)
	plt.colorbar(pc)

	ax = plt.gca()
	ax.set_axis_off()
	plt.show()

if __name__ == "__main__":
	main()

