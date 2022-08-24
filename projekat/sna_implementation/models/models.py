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


def get_full_barabasi_albert_model(n = 500, n_s = 50, p_s = 0.04, m = 20, a = 25, p_c = 0.2, cap = 100, time_lim = 20, seed=12345, p_sign = 0.03):
    graph = nx.erdos_renyi_graph(n_s, p_s, seed)

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

        # Dodajemo m novih grana
        for _ in range(m):
            index = rn.randint(0, len(degs) - 1)
            old = degs[index]
            graph.add_edge(node, old)
            # print(f"\tAdded edge: {(node, old)}")
            update_trackers(graph, old, degs, times, cap)

            # Dodajemo grane sa susedima old cvora
            for neigh in graph.neighbors(old):
                if rn.random() < p_c and neigh in degs:
                    graph.add_edge(node, neigh)
                    # print(f"\t\tAdded neighbour edge {(node, neigh)}")
                    update_trackers(graph, neigh, degs, times, cap)
        
        # Azuriramo vremena i izbacimo sve one koji su prekoracili
        times = {k : v + 1 for k, v in times.items() if v + 1 < time_lim}
        print(f"Times: {times}")
        # Ako su izbaceni iz times, izbacujemo ih i iz degs
        degs = [k for k in degs if k in times]
        print(f"Degrees: {degs}")
        print("Trackers updated")

        # Dodajemo novi cvor u degs i times
        for _ in range(graph.degree(node) + a):
            degs.append(node)
            times[node] = 0
    

    return add_signs(graph, p_sign, seed)


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
     

# Dodajemo znakove na linkove
def add_signs(graph, p_sign, seed):
    rn.seed(seed)
    for edge in graph.edges.data():
        edge[2]['sign'] = '+' if rn.random() <= p_sign else '-'
        # print(edge)
    
    return graph

# get_erdos_renyi_model()