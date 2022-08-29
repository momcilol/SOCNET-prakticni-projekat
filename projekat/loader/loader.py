import graphlib
from tokenize import group
import networkx as nx
import re

def load_epinions(filename: str, node_number=1_000):
    diGraph = nx.DiGraph()

    with open("projekat/data/" + filename) as file:
        file.readline()
        diGraph.name = file.readline()[2:]
        file.readline()
        file.readline()

        for line in file.readlines():
            tokens = re.split("[\t ]+", line)

            if int(tokens[2].strip()) > node_number:
                break

            diGraph.add_edges_from([(int(tokens[0].strip()), int(tokens[1].strip()), {'sign': int(tokens[2].strip())})])

    diGraph.remove_nodes_from([node for node in diGraph.nodes() if node > node_number])

    return to_udirected_graph(diGraph), diGraph


def load_wiki_rfa(filename: str, node_number=1_000):
    diGraph = nx.DiGraph()

    with open("projekat/data/" + filename) as file:
        diGraph.name = filename
        p = re.compile(r'(\n|.)*SRC:(?P<src>.+)(\n|.)*TGT:(?P<tgt>.+)(\n|.)*VOT:(?P<vot>.+)(\n|.)*')

        count = 0
        while True:
            block = ""
            
            for _ in range(8):
                block += file.readline()
            
            if block == "":
                break

            m = re.match(p, block)
            if m is not None:
                groups = m.groupdict()
                diGraph.add_edges_from([(groups['src'], groups['tgt'], {'sign': int(groups['vot'].strip())})])

            if diGraph.number_of_nodes() >= node_number:
                break

    return to_udirected_graph(diGraph), diGraph


def to_udirected_graph(diGraph: nx.DiGraph):
    graph = nx.Graph()
    graph.name = diGraph.name

    node_list = list(diGraph.nodes())
    node_list.sort()
    graph.add_nodes_from(node_list)

    for u, v in diGraph.edges():
        if u != v:
            if graph.has_edge(v, u):
                graph[v][u]['sign'] = graph[v][u]['sign'] + diGraph[u][v]['sign']
            else:
                graph.add_edges_from([(u, v, diGraph[u][v])])
    
    return graph


