import networkx as nx

import projekat.tester.test_perform as te


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


    tester = te.Tester(graph, transform= lambda G, edge : G[edge[0]][edge[1]]['sign'])
    cluster_network = tester._sncc.get_cluster_graph()

    # Test results

    tester.print_network()
    tester.check_clusterability()
    tester.show_degree_information(graph)
    tester.print_centralities(graph, True)
    tester.print_assortativity(graph)
    tester.print_k_core_decomposition(graph)
    tester.print_small_world_metrics(graph)
    tester.draw_network(graph)

    print("Cluster network statistics:")

    tester.show_degree_information(cluster_network)
    tester.print_centralities(cluster_network)
    tester.print_assortativity(cluster_network)
    tester.print_k_core_decomposition(cluster_network)
    tester.print_small_world_metrics(cluster_network)
    tester.draw_network(cluster_network) 

 

if __name__=="__main__":
    main()