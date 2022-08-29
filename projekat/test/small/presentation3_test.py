import networkx as nx

from sna_implementation.tester.test_perform import Tester


def main():
    graph = nx.Graph(name="Presentation")
    graph.add_edges_from([
        ( 1,  2, {'sign': '+'}), 
        ( 1,  3, {'sign': '+'}), 
        ( 2,  3, {'sign': '+'}), 
        ( 2,  5, {'sign': '+'}), 
        ( 2,  4, {'sign': '-'}), 
        ( 3,  6, {'sign': '-'}),
        ( 4,  7, {'sign': '-'}),
        ( 4,  9, {'sign': '-'}), 
        ( 5,  6, {'sign': '-'}), 
        ( 6,  8, {'sign': '+'}),
        ( 6, 11, {'sign': '-'}),
        ( 7, 12, {'sign': '+'}),
        ( 8, 11, {'sign': '-'}),
        ( 9, 12, {'sign': '+'}),
        (10, 11, {'sign': '-'}),
        (10, 12, {'sign': '+'}),
        (11, 13, {'sign': '-'}),
        (11, 14, {'sign': '-'}),
        (12, 13, {'sign': '+'}),
        (13, 15, {'sign': '-'}),
        (14, 15, {'sign': '-'})
    ]) 


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
    tester.draw_network(graph)
    input(">>next>>")

    print("Cluster network statistics:")

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
    tester.draw_network(cluster_network, name=True) 
    input(">>Thats it>>")


if __name__=="__main__":
    main()

