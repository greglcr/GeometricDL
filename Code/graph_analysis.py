import networkx as nx
import os.path as osp
import numpy as np
import matplotlib.pyplot as plt

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

nb_graph = np.unique(node_graph).shape[0]
my_graphs = [nx.Graph() for i in range(nb_graph)]

maxi_graph = 0
id_maxi_graph = -1

for i_node in range(node_graph.shape[0]):
    graph_id = node_graph[i_node]
    prof = -1
    if my_graphs[graph_id].number_of_nodes() == 0:
        prof = 0
    my_graphs[graph_id].add_node(i_node, prof=prof, neg_prof=0)
    if my_graphs[graph_id].number_of_nodes() > maxi_graph and graph_label[graph_id] == 1:
        maxi_graph = my_graphs[graph_id].number_of_nodes()
        id_maxi_graph = graph_id

for i in range(len(edges)):
    graph_id = node_graph[edges[i][0]]
    my_graphs[graph_id].add_edge(edges[i][0], edges[i][1])
    my_graphs[graph_id].nodes[edges[i][1]]['prof'] = my_graphs[graph_id].nodes[edges[i][0]]['prof'] + 1

print("Nombre de graphe :", nb_graph)
print("Nombre total de noeud :", node_graph.shape[0])
print("Nombre total d'edges :", len(edges))

nb_nodes_per_graph = []
for i in range(nb_graph):
    nb_nodes_per_graph.append(my_graphs[i].number_of_nodes())
nb_nodes_per_graph.sort()

for_count = [nb_nodes_per_graph.count(i + 1) for i in range(max(nb_nodes_per_graph))]
x_value = [i for i in range(max(nb_nodes_per_graph) + 1)]
for_count.append(0)

plt.bar(x_value, for_count, width=1)
plt.ylim(0, max(for_count) + 1)
plt.margins(0)
plt.axhline(0, color='black', linewidth=0.8)
plt.xlabel('Size of URL cascade')
plt.ylabel('Number of cascade')
plt.savefig('Diagramme_bâton_cascades.png')