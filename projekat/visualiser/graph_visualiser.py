import networkx as nx

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

def draw_graph(G: nx.Graph, layout_key):
    pos = layout[layout_key](G)
    nx.draw_networkx(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edge_labels(G, pos, )