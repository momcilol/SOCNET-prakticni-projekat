from filecmp import cmp
import networkx as nx
from sna_implementation.clustering.edge_sign import EdgeSign
import matplotlib.pyplot as plt
from math import e, log


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


def draw_graph(G: nx.Graph, transform, layout_key="spring", has_name=False):
    pos = layout[layout_key](G)
    node_color = [log(float(G.degree(node) + 1), e) + 5 for node in G.nodes()]
    node_lables = {}
    if has_name:
        node_lables = {n: n.name for n in G.nodes()}
    else:
        node_lables = {n: n for n in G}

    nx.draw_networkx(G, pos, node_color=node_color, cmap=plt.cm.Blues, labels=node_lables)

    
    # nx.draw_networkx_labels(G, pos, labels=node_lables)

    edge_colors = ['red' if transform(G, edge) == EdgeSign.NEGATIVE.value else 'green' for edge in G.edges()]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors)
    
    edge_labels = {edge: transform(G, edge) for edge in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.subplots_adjust(left=0.1, bottom=0.12, top=0.9, right=0.95)
    plt.show()

