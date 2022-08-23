import networkx as nx
import random as rn


def get_erdos_renyi_model(n = 250, p = 0.05, seed = 12345, p_sign = 0.5):
    graph = nx.erdos_renyi_graph(n, p, seed)

    return add_signs(graph, p_sign, seed)


def get_configuration_model(n = 250, max_deg = 40, seed = 12345, p_sign = 0.5):
    rn.seed(seed)
    degrees = [rn.randint(0,max_deg) for i in range(250)]
    degrees[0] = degrees[0] + 1 if sum(degrees) % 2 == 1 else degrees[0]
    graph = nx.configuration_model(degrees, create_using=nx.Graph(),  seed=seed)

    return add_signs(graph, p_sign, seed)


def get_watts_strogatz_model(n = 250, k = 4, p = 0.05, seed = 12345, p_sign = 0.5):
    graph = nx.watts_strogatz_graph(n, k, p, seed)
    return add_signs(graph, p_sign, seed)


def get_barabasi_albert_model(n = 250, m0 = 50, m = 5, seed = 12345, p_sign = 0.5):
    graph = nx.barabasi_albert_graph(n, m, seed, nx.erdos_renyi_graph(m0, 0.1, seed))
    return add_signs(graph, p_sign, seed)


def get_barabasi_albert_extra_model(n = 250, m = 10, p = 0.33, q = 0.33, seed=12345, p_sign = 0.5):
    graph = nx.extended_barabasi_albert_graph(n, m, p, q, seed)
    return add_signs(graph, p_sign, seed)

def add_signs(graph, p_sign, seed):
    rn.seed(seed)
    for edge in graph.edges.data():
        edge[2]['sign'] = '+' if rn.random() <= p_sign else '-'
        print(edge)
    
    return graph

# get_erdos_renyi_model()