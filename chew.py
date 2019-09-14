import pandas as pd
import seaborn as sns
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from nxviz import ArcPlot
from nxviz import CircosPlot
from bokeh.plotting import figure

from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.palettes import Spectral4


def vker(id):
	return 'https://www.vk.com/id'+str(id)
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



def main():

	print('Start csv loading process..', end='')
	nodes = pd.read_csv('nodes_full.csv')
	nodes = pd.DataFrame(nodes['node'], columns=['node'])
	node1,node2 ,edges =[],[],[]
	edges = pd.read_csv('edges_full.csv')
	print(' Done!')

 	

	'''
+++++++++++

	'''


	print('Start pandas to nx loading process..', end='')
	G = graph_loader(nodes['node'],edges[['node1','node2']])

	deg_df = pd.read_csv('degree_centrality.csv')
	bet_df = pd.read_csv('betweenness_centrality.csv')
	eif_df = pd.read_csv('eigenvector_centrality.csv')
	page_df = pd.read_csv('page_rank.csv')
	

	
	page_top_nodes = page_df.sort_values('page_rank', ascending=False)
	print(page_top_nodes.head())
	print(page_top_nodes.tail())
	print('Done!')	
	# eif_top_nodes = eif_df.sort_values('eigenvector', ascending=False)
	# print(eif_top_nodes.head())
	# print('Done!')
	# target_df = eif_top_nodes['node'].apply(vker)[:30]
	# target_df.to_csv('medichi.csv')
	# print(target_df.head(10))

	print('Start subgraph draw function..', end='')
	# Extract the subgraph with the nodes of interest: G_draw
	G_draw = get_nodes_and_nbrs(G, page_top_nodes['node'][:30])
	print('Done!')
	# # Display the plot
	# nx.draw(G_draw)
	# plt.show()




	# plot = Plot(plot_width=400, plot_height=400,
	#             x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1))
	# plot.title.text = "Graph Interaction Demonstration"

	# plot.add_tools(HoverTool(tooltips=None), TapTool(), BoxSelectTool())

	# graph_renderer = from_networkx(G_draw, nx.circular_layout, scale=1, center=(0,0))

	# graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
	# graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
	# graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

	# graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
	# graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
	# graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)

	# graph_renderer.selection_policy = NodesAndLinkedEdges()
	# graph_renderer.inspection_policy = EdgesAndLinkedNodes()

	# plot.renderers.append(graph_renderer)

	# output_file("interactive_graphs.html")
	# show(plot)


	plot = figure(title="Networkx Integration Demonstration", x_range=(-1.1,1.1), y_range=(-1.1,1.1),
	              tools="", toolbar_location=None)

	graph = from_networkx(G_draw, nx.spring_layout, scale=2, center=(0,0))
	plot.renderers.append(graph)

	output_file("networkx_graph.html")
	show(plot)
if __name__ == "__main__":
	main()

