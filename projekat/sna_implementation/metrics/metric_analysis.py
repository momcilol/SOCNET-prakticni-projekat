from math import degrees
from platform import node
from queue import Empty
import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import sna_implementation.clustering.signed_clusterable_network as cl
from sna_implementation.clustering.edge_sign import EdgeSign


# Node metrics

node_metrics = [
    "Betweeness centrality", 
    "Closeness centrality", 
    "EigenVector centrality",
    "Clustering coefficient"
]


def get_betweeness_centrality(graph):
    return nx.betweenness_centrality(graph)


def get_closeness_centrality(graph):
    return nx.closeness_centrality(graph)


def get_eigenvector_centrality(graph):
    return nx.eigenvector_centrality(graph)


def get_page_rank(graph: nx.DiGraph):
    return nx.pagerank(graph)


def get_clustering_coefficients(graph):
    return nx.clustering(graph)


# Console print

def print_node_metrics_results(results, metric, has_name=False):
    print(f"""
       {metric.upper()}

        NODES  |  SCORES 
    """)
    if has_name:
        for node, score in results.items():
            print(f"{node.name : >13}  | {score : .4f}")
    else:
        for node, score in results.items():
            print(f"{node : >13}  | {score : .4f}")
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
            print(f"{k.name : >10} | {v : 12.4f} | {v1 : 12.4f}")
    else:
        for (k, v), (k1, v1) in zip(hubs.items(), authorities.items()):
            print(f"{k : >10} | {v : 12.4f} | {v1 : 12.4f}")
    print()


# Small world metrics


def get_small_world_metric_results(graph: nx.Graph):
    G = list(graph.nodes())

    if not nx.is_connected:
        largest_cc = max(nx.connected_components(graph), key=len)
        G = list(largest_cc)

    n = len(G)
    nn = (n*(n-1))
    small = 0
    eff = 0

    for a in G:
        for b in G:
            if a != b:
                tmp = nx.shortest_path_length(graph, a, b)
                small += tmp
                eff += 1/tmp

    global_efficiency = 0
    for a in graph:
        for b in graph:
            if a!=b:
                tmp = nx.shortest_path_length(graph, a, b)
                if tmp != nx.NetworkXNoPath:
                    global_efficiency += 1/tmp

    non = graph.number_of_nodes()            
 
    return small/nn, eff/nn, global_efficiency/(non * (non - 1))


def get_diameter(graph: nx.Graph):
    return nx.diameter(graph)


def get_radius(graph: nx.Graph):
    return nx.radius(graph)

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

    for k in range(max_degree + 1):
        while len(D[k]) != 0:
            # izbacujemo jedan cvor iz tekuceg skupa (shell-a)
            x = D[k].pop()
            S[x] = k
            # prebacimo sve susedne cvorove koji su u "visim" skupovima u
            # skupove sa indexom za 1 manji od dosadasnjeg
            for v in graph.neighbors(x):
                if d[v] > k:
                    D[d[v]].pop()
                    D[d[v]-1].add(v)
                    d[v] = d[v] - 1
    
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

