import matplotlib.pyplot as plt
import networkx as nx


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
    plt.show()


degree_info_metric = [
    "Nodes per degree",
    "Degree distribution",
    "Complementary cumulative degree distribution"
]


def draw_degree_info(results, metric):
    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots()

    ax.bar(results, linewidth=2.0)
    plt.xlabel('Nodes')
    plt.ylabel('Scores')
    plt.title(metric)
    plt.show()


def draw_assortativity(graph: nx.Graph, rang=False):
    xy = nx.node_degree_xy()
    x, y = zip(*xy)

    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots()

    ax.scatter(x, y)
    plt.title("Assortativity")
    plt.xlabel('Nodes')
    plt.ylabel('Scores')
    plt.show()
