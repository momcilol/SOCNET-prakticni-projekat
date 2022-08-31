import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def draw_centrality_results(results: dict, metric, has_name=False):

    plt.style.use('_mpl-gallery')
    sizes = [x*60 + 20 for x in list(results.values)]
    colors = [80 - x*60 for x in list(results.values)]
    fig, ax = plt.subplots()

    x = results.keys.name if has_name else results.keys
    y = results.values

    ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100)
    plt.xlabel('Nodes')
    plt.ylabel('Scores')
    plt.title(metric)
    plt.subplots_adjust(left=0.1, bottom=0.12, top=0.9, right=0.95)
    plt.show()


degree_info_metric = {
    "ND": "Nodes per degree",
    "DD": "Degree distribution",
    "CC": "Complementary cumulative degree distribution"
}


def draw_degree_info(results: list, metric):
    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots()


    ax.bar(list(range(len(results))), results, linewidth=2.0)
    plt.xlabel('Degree')
    plt.title(degree_info_metric[metric])
    plt.subplots_adjust(left=0.1, bottom=0.12, top=0.9, right=0.95)
    plt.show()


def draw_degree_info_log(results: list, metric):
    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots()


    ax.bar(list(range(len(results))), results, linewidth=2.0, log= True)
    plt.xlabel('Degree')
    plt.title(degree_info_metric[metric])
    plt.subplots_adjust(left=0.1, bottom=0.12, top=0.9, right=0.95)
    plt.show()

def draw_degree_info_loglog(results: list, metric):
    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots()


    ax.scatter(list(range(len(results))), results)
    
    if max(results) > 10*(min(results) + 1):
        ax.set_yscale('log')
    
    if len(results) > 50:
        ax.set_xscale('log')
    
    plt.xlabel('Degree')
    plt.title(degree_info_metric[metric])
    plt.subplots_adjust(left=0.1, bottom=0.12, top=0.9, right=0.95)
    plt.show()


def draw_assortativity(graph: nx.Graph, rang=False):
    xy = nx.node_degree_xy(graph)
    x, y = zip(*xy)

    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots()

    ax.scatter(x, y)

    if max(y) > 10*(min(y) + 1):
        ax.set_yscale('log')
        ax.set_xscale('log')


    plt.title("Assortativity")
    plt.xlabel('Node degrees')
    plt.ylabel('Node degrees')
    plt.subplots_adjust(left=0.1, bottom=0.12, top=0.9, right=0.95)
    plt.show()


def draw_matrix(graph: nx.Graph, a: np.array, title: str, has_name=False):
    nodes = []
    if has_name:
        nodes = [node.name for node in graph.nodes()]
    else:
        nodes = list(graph)

    plt.matshow(a)
    plt.title(title)
    plt.xticks(range(graph.number_of_nodes()), nodes, rotation=45)
    plt.yticks(range(graph.number_of_nodes()), nodes)
    plt.show()