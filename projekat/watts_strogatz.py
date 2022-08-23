import networkx as nx
from sna_implementation.tester.test_perform import Tester
from sna_implementation.models.models import get_watts_strogatz_model





def main():

    graph = get_watts_strogatz_model()
    tester = Tester(graph, transform= lambda G, edge : G[edge[0]][edge[1]]['sign'])
    input(">>Start printing>>")
    cluster_network = tester._sncc.get_cluster_graph()

    # Test results

    tester.print_network()
    input(">>next>>")
    tester.check_clusterability()
    input(">>next>>")
    tester.show_degree_information(graph)
    input(">>next>>")
    tester.print_centralities(graph)
    input(">>next>>")
    tester.print_assortativity(graph)
    input(">>next>>")
    tester.print_k_core_decomposition(graph)
    input(">>next>>")
    tester.print_small_world_metrics(graph)
    input(">>next>>")
    tester.print_similarity_matrix(graph)
    input(">>next>>")
    tester.draw_network(graph, "kamanda")
    input(">>next>>")

    print("Cluster network statistics:")

    if cluster_network.number_of_nodes() != 1:
        tester.show_degree_information(cluster_network)
        input(">>next>>")
        tester.print_centralities(cluster_network, True)
        input(">>next>>")
        tester.print_assortativity(cluster_network)
        input(">>next>>")
        tester.print_k_core_decomposition(cluster_network, True)
        input(">>next>>")
        tester.print_small_world_metrics(cluster_network)
        input(">>next>>")
        tester.print_similarity_matrix(cluster_network, True)
        input(">>next>>")
        tester.draw_network(cluster_network, "kamanda", name=True) 
    else:
        print("Cluster network has only one node. Nothing to analize...")
    input(">>Thats it>>")



if __name__ == "__main__":
    main()