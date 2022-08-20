from filecmp import cmp
import networkx as nx
from cluster.edge_sign import EdgeSign
import matplotlib.pyplot as plt

layout = {
    "circular": nx.circular_layout,
    "kamanda": nx.kamada_kawai_layout,
    "planar": nx.planar_layout,
    "random": nx.random_layout,
    "shell": nx.shell_layout,
    "spring": nx.spring_layout,
    "spectral": nx.spectral_layout,
    "spiral": nx.spiral_layout,
    "multipartite": nx.multipartite_layout    
}


def draw_graph(G: nx.Graph, layout_key, transform):
    pos = layout[layout_key](G)
    nx.draw_networkx(G, pos, node_color=range(10, 24), cmap=plt.cm.Blues)
    nx.draw_networkx_labels(G, pos)

    positive = [edge for edge in G.edges() if transform(edge) == EdgeSign.POSITVE]
    nx.draw_networkx_edges(G, pos, edgelist=positive, edge_color='green')

    negative = [edge for edge in G.edges() if transform(edge) == EdgeSign.NEGATIVE]
    nx.draw_networkx_edges(G, pos, edgelist=negative, edge_color='red')
    
    edge_labels = {edge: transform(edge) for edge in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()
