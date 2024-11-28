import networkx as nx
import os.path as osp
import numpy as np

_file_ = '..'
file = _file_
dataset = 'gossipcop'  # or 'politifact'
path = osp.join('..', 'upfd_data-20241125T115418Z-001', 'upfd_data', 'gossipcop')

graph_label = np.load(osp.join(path, 'graph_labels.npy'))
node_graph = np.load(osp.join(path, 'node_graph_id.npy'))

edges = []
edges_file = 'A.txt'
with open(osp.join(path, edges_file)) as file:
    for line in file:
        edge = line.split(', ')
        edges.append([int(edge[0]), int(edge[1])])

my_graph = nx.Graph()
graph_id = 10

for i in range(node_graph.shape[0]):
    if node_graph[i] == graph_id:
        my_graph.add_node(i)

for i in range(len(edges)):
    if node_graph[edges[i][0]] == graph_id and node_graph[edges[i][1]] == graph_id:
        my_graph.add_edge(edges[i][0], edges[i][1])

fileName = 'true_graph_' + str(graph_id) + ".graphml"
nx.write_graphml_lxml(my_graph, fileName)