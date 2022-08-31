from math import e, sqrt
from zoneinfo import available_timezones
import networkx as nx
import random as rn


def get_erdos_renyi_model(n=250, p=0.05, seed=12345, p_sign=0.5):
    graph = nx.erdos_renyi_graph(n, p, seed)

    return add_signs(graph, p_sign, seed)


def get_configuration_model(n=250, max_deg=40, seed=12345, p_sign=0.5):
    rn.seed(seed)
    degrees = [rn.randint(0, max_deg) for i in range(250)]
    degrees[0] = degrees[0] + 1 if sum(degrees) % 2 == 1 else degrees[0]
    graph = nx.configuration_model(degrees, create_using=nx.Graph(),  seed=seed)

    return add_signs(graph, p_sign, seed)


def get_watts_strogatz_model(n=250, k=10, p=0.1, seed=12345, p_sign=0.5):
    graph = nx.watts_strogatz_graph(n, k, p, seed)
    return add_signs(graph, p_sign, seed)


def get_barabasi_albert_model(n=250, m0=50, m=5, seed=12345, p_sign=0.5):
    graph = nx.barabasi_albert_graph(n, m, seed, nx.erdos_renyi_graph(m0, 0.1, seed))
    return add_signs(graph, p_sign, seed)


def get_barabasi_albert_extra_model(n=250, m=10, p=0.33, q=0.33, seed=12345, p_sign=0.5):
    graph = nx.extended_barabasi_albert_graph(n, m, p, q, seed)
    return add_signs(graph, p_sign, seed)


def get_full_barabasi_albert_model(n=250, n_s=50, p_s=0.04, m=10, a=15, p_c=0.75, cap=50, time_lim=150, seed=12345, p_sign=0.5):
    graph = nx.erdos_renyi_graph(n_s, p_s, seed)
    graph = add_signs(graph, p_sign, seed)
    graph: nx.Graph

    rn.seed(seed)
    degs = []
    times = {}

    # Popunimo stepenu listu i recnik vremena
    for node in graph:
        for _ in range(graph.degree(node) + a):
            degs.append(node)
            times[node] = 0

    # Ubacujemo novi cvor
    for node in range(n_s, n):
        graph.add_node(node)
        # print(f"Added node {node}")

        # Biramo prototip
        prototype = rn.choice(degs)
        sign = '+' if rn.random() < p_sign else '-'
        graph.add_edges_from([(node, prototype, {'sign': sign})])
        # print(f"\tAdded edge: {(node, prototype)}")
        update_trackers(graph, prototype, degs, times, cap)
        
        neighbours = [n for n in graph.neighbors(prototype) if n in degs]
        # Dodajemo m novih grana
        for _ in range(m):
            # Dodajemo grane sa susedima protorype cvora
            if rn.random() < p_c and len(neighbours) > 0:
                neigh = rn.choice(neighbours)
                # Biramo znak grane
                if graph[prototype][neigh]['sign'] == sign:
                    new_edge_sign = '+' if rn.random() < sqrt(p_sign) else '-'
                else:
                    new_edge_sign = '+' if rn.random() < p_sign ** 2 else '-'

                graph.add_edges_from([(node, neigh, {'sign': new_edge_sign})])
                # print(f"\t\tAdded neighbour edge {(node, neigh)}")
                update_trackers(graph, neigh, degs, times, cap)
            else:
                rannode = rn.choice(degs)
                new_edge_sign = '+' if rn.random() < p_sign else '-'
                graph.add_edges_from([(node, rannode, {'sign': new_edge_sign})])
                # print(f"\tAdded edge: {(node, old)}")
                update_trackers(graph, rannode, degs, times, cap)


        # Azuriramo vremena i izbacimo sve one koji su prekoracili
        times = {k: v + 1 for k, v in times.items() if v + 1 < time_lim}
        # print(f"Times: {times}")
        # Ako su izbaceni iz times, izbacujemo ih i iz degs
        degs = [k for k in degs if k in times]
        # print(f"Degrees: {degs}")
        # print("Trackers updated")

        # Dodajemo novi cvor u degs i times
        for _ in range(graph.degree(node) + a):
            degs.append(node)
            times[node] = 0

    return graph

    # return add_signs(graph, p_sign, seed)


# Izbacujemo sve one koji imaju stepen >= cap
def update_trackers(graph, node, degs, times, cap):
    if graph.degree(node) >= cap:
        degs = [n for n in degs if n != node]
        try:
            times.pop(node)
        except KeyError:
            print(f"No such key: {node}")
    else:
        degs.append(node)


def get_planted_partition_model(n=250, z=0.5, p=0.07, q=0.01, seed=12345):
    m = [z, 1.0-z]

    B = [
        [p, q],
        [q, p]
    ]
    return get_stochastic_block_model(n, 2, m, B, seed)


def get_stochastic_block_model(n=250, q=10, m=None, B=None, seed=12345, p_sign=0.5):
    rn.seed(seed)
    if m is None:
        m = [rn.random() for _ in range(q-1)]
        m.append(1.0)
        m.append(0.0)
        m.sort(reverse=True)
        m = [m[i] - m[i+1] for i in range(q)]
    
    sizes = [int(m[i]*n) for i in range(q)]
    sizes[sizes.index(min(sizes))] += n - sum(sizes)

    if B is None:
        B = [[0 for _ in range(q)] for _ in range(q)]
        for i in range(q):
            for j in range(i, q):
                if i == j:
                    B[i][j] = 0.05 * (1 + rn.random())
                else:
                    B[i][j] = 0.05 * (1 + rn.random()) / q
                    B[j][i] = B[i][j]

    return add_signs(nx.stochastic_block_model(sizes, B, seed=seed), p_sign, seed)


# Dodajemo znakove na linkove
def add_signs(graph, p_sign, seed):
    rn.seed(seed)
    for edge in graph.edges.data():
        edge[2]['sign'] = '+' if rn.random() <= p_sign else '-'
        # print(edge)

    return graph

# get_erdos_renyi_model()
