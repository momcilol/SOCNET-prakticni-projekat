from locale import normalize
from math import sqrt
import numpy as np
import networkx as nx
from scipy.stats import spearmanr


# Node metrics

node_metrics = [
    "Betweeness centrality", 
    "Closeness centrality", 
    "EigenVector centrality",
    "Clustering coefficient"
]


def get_betweeness_centrality(graph):
    return nx.betweenness_centrality(graph, normalized=True)


def get_closeness_centrality(graph):
    return nx.closeness_centrality(graph)


def get_eigenvector_centrality(graph):
    return nx.eigenvector_centrality(graph, tol=1.0e-3)


def get_page_rank(graph: nx.DiGraph):
    return nx.pagerank(graph, tol=1.0e-3)


def get_clustering_coefficients(graph):
    return nx.clustering(graph)


def get_sim_rank_coefficients(graph):
    sim = nx.simrank_similarity(graph)
    return np.array([[sim[u][v] for v in graph] for u in graph])


def get_adamic_adar_coefficients(graph: nx.Graph):
    aait = nx.adamic_adar_index(graph)
    num = graph.number_of_nodes()
    aam = [[0 for j in range(num)] for i in range(num)]
    nodes = list(graph.nodes())
    for u, v, p in aait:
        i = nodes.index(u)
        j = nodes.index(v)
        aam[i][j] = p
        aam[j][i] = p
    
    return np.array(aam)

# Console print

def print_node_metrics_results(results, metric, has_name=False):
    print(f"""
                    {metric.upper()}

                    NODES  |  SCORES 
    """)
    if has_name:
        for node, score in results.items():
            print(f"{node.name : >25}  | {score : .4f}")
    else:
        for node, score in results.items():
            print(f"{node : >25}  | {score : .4f}")
    print()



def get_hits_results(graph: nx.DiGraph):
    return nx.hits(graph)


def print_hits_results(results, has_name=False):
    hubs, authorities = results
    print(f"""
                    HITS

                    NODES  |     HUBS     |  AUTHORITIES
    """)
    if has_name:
        for (k, v), (k1, v1) in zip(hubs.items(), authorities.items()):
            print(f"{k.name : >25}  | {v : 12.4f} | {v1 : 12.4f}")
    else:
        for (k, v), (k1, v1) in zip(hubs.items(), authorities.items()):
            print(f"{k : >25} | {v : 12.4f} | {v1 : 12.4f}")
    print()


# Small world metrics


def get_small_world_metric_results(graph: nx.Graph):
    G = list(graph.nodes())

    if not nx.is_connected(graph):
        largest_cc = max(nx.connected_components(graph), key=len)
        G = list(largest_cc)

    n = len(G)
    nn = (n*(n-1))
    small = 0
    eff = 0

    min_ecc = n
    max_dis = 0

    for a in G:
        ecc = 0

        for b in G:
            if a != b:
                distance = nx.shortest_path_length(graph, a, b)
                small += distance
                eff += 1/distance
                if distance > max_dis:
                    max_dis = distance
                if distance > ecc:
                    ecc = distance
                
        if min_ecc > ecc:
            min_ecc = ecc

    global_efficiency = 0
    for a in graph:
        for b in graph:
            if a!=b:
                try:
                    tmp = nx.shortest_path_length(graph, a, b)
                    global_efficiency += 1/tmp 
                except nx.NetworkXNoPath:
                    pass

    non = graph.number_of_nodes()            
 
    return small/nn, eff/nn, global_efficiency/(non * (non - 1)), max_dis, min_ecc


# K-core decomposition

def get_k_core_decomposition(graph: nx.Graph, sign=None):
    # sign je ostavljen da bi se kasnije implementiralo za znake edge-a
    max_degree = max([v[1] for v in list(graph.degree())])
    d = {node: 0 for node in graph.nodes()}
    D = [set() for m in range(max_degree+1)]

    # izlazni niz shell indexa
    S = {}

    # postavimo inicijalne stepene
    for v in graph.nodes():
        k = graph.degree(v)
        d[v] = k
        D[k].add(v)

    # print(f"Start K core")
    # print(f"Start d: {d}")
    # print(f"Start D: {D}")

    # print("Calculating...")
    for k in range(max_degree + 1):
        while len(D[k]) != 0:
            # izbacujemo jedan cvor iz tekuceg skupa (shell-a)
            x = D[k].pop()
            S[x] = k
            # prebacimo sve susedne cvorove koji su u "visim" skupovima u
            # skupove sa indexom za 1 manji od dosadasnjeg
            for v in graph.neighbors(x):
                if d[v] > k:
                    D[d[v]].remove(v)
                    D[d[v]-1].add(v)
                    d[v] = d[v] - 1
            # print(x)
            # print(f"d: {d}")
            # print(f"D: {D}")
            # print(f"S: {S}")

    
    # print(f"K core preview: {S}")

    return S


# Degree information


def get_degree_information(graph: nx.Graph):

    num_nodes =  graph.number_of_nodes()
    nodes_per_degree = nx.degree_histogram(graph)
    max_degree = len(nodes_per_degree) - 1
    max_node_count = max(nodes_per_degree)

    degree_distribution = [count / max_node_count for count in nodes_per_degree]

    complementary_cumulative_distribution = list(range(max_degree + 1))
    complementary_cumulative_distribution[max_degree] = nodes_per_degree[max_degree]

    for i in range(max_degree - 1, -1, -1):
        complementary_cumulative_distribution[i] = float(complementary_cumulative_distribution[i+1] + nodes_per_degree[i])
        complementary_cumulative_distribution[i+1] /= num_nodes

    complementary_cumulative_distribution[0] /= num_nodes  

    average = sum([y for x, y in list(graph.degree())])/num_nodes
    density = average / (graph.number_of_nodes() - 1)

    return nodes_per_degree, degree_distribution, complementary_cumulative_distribution, average, density
        

# Network assortativity
    
def get_pearson_coefficient(graph: nx.Graph):
    return nx.degree_pearson_correlation_coefficient(graph)


def get_spearman_coefficient(graph: nx.Graph):
    xy = nx.node_degree_xy(graph)
    x, y = zip(*xy)
    return spearmanr(x, y)[0]

