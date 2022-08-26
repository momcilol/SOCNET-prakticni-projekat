from filecmp import cmp
import networkx as nx
from sna_implementation.clustering.edge_sign import EdgeSign
import matplotlib.pyplot as plt
from math import e, log


layout = {
    "circular": nx.circular_layout,
    "kamanda": nx.kamada_kawai_layout,
    "random": nx.random_layout,
    "spring": nx.spring_layout,
    "spiral": nx.spiral_layout,
}


def draw_graph(G: nx.Graph, transform, layout_key="spring", has_name=False):
    pos = layout[layout_key](G)
    max_deg = max([v for k, v in list(G.degree())]) + 1
    node_color = [1-log(float(0.6*max_deg + 0.6*(G.degree(node)+1)), 2*max_deg) for node in G.nodes()]
    node_size = [(2-x)*170 for x in node_color]
    # print(node_color)
    node_lables = {}
    if has_name:
        node_lables = {n: n.name for n in G.nodes()}
    else:
        node_lables = {n: n for n in G}

    nx.draw_networkx(G, pos,node_size=node_size , node_color=node_color, cmap=plt.get_cmap("YlOrBr"), labels=node_lables, vmin=0, vmax=1)

    
    # nx.draw_networkx_labels(G, pos, labels=node_lables)

    edge_colors = ['red' if transform(G, edge) == EdgeSign.NEGATIVE.value else 'green' for edge in G.edges()]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors)
    
    # edge_labels = {edge: transform(G, edge) for edge in G.edges()}
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.subplots_adjust(left=0.1, bottom=0.12, top=0.9, right=0.95)
    plt.show()

