import networkx as nx
import pandas as pd
from sna_implementation.tester.test_perform import Tester

def main():
    data = pd.read_csv("projekat/data/GOT.csv")
    graph = nx.from_pandas_edgelist(data, source="V1", target="V2", edge_attr="type", create_using=nx.Graph(), edge_key="name")

    tester = Tester(graph, transform= lambda G, edge : '+' if G[edge[0]][edge[1]]['type'] == 1 else '-')
    input(">>Start printing>>")
    cluster_network = tester._sncc.get_cluster_graph()

    # Test results

    # tester.print_network()
    # input(">>next>>")
    # tester.check_clusterability()
    # input(">>next>>")
    # tester.show_degree_information(graph)
    # input(">>next>>")
    # tester.print_centralities(graph)
    # input(">>next>>")
    # tester.print_assortativity(graph)
    # input(">>next>>")
    # tester.print_k_core_decomposition(graph)
    # input(">>next>>")
    # tester.print_small_world_metrics(graph)
    # input(">>next>>")
    tester.print_similarity_matrix(graph)
    input(">>next>>")
    tester.draw_network(graph, "kamanda")
    input(">>next>>")

    print("Cluster network statistics:")

    # tester.show_degree_information(cluster_network)
    # input(">>next>>")
    # tester.print_centralities(cluster_network, True)
    # input(">>next>>")
    # tester.print_assortativity(cluster_network)
    # input(">>next>>")
    # tester.print_k_core_decomposition(cluster_network, True)
    # input(">>next>>")
    # tester.print_small_world_metrics(cluster_network)
    # input(">>next>>")
    tester.print_similarity_matrix(cluster_network, True)
    input(">>next>>")
    tester.draw_network(cluster_network, "kamanda", name=True) 
    input(">>Thats it>>")

    
    

if __name__ == "__main__":
    main()

