from cgi import test
import networkx as nx
from sna_implementation.tester.test_perform import Tester
from loader.loader import load_epinions


network_labels = [
    "Slashdot Zoo signed social network from November 6 2008", 
    "Slashdot Zoo signed social network from February 16 2009", 
    "Slashdot Zoo signed social network from February 21 2009"
]

network_files = [
    "soc-sign-Slashdot081106.txt",
    "soc-sign-Slashdot090216.txt",
    "soc-sign-Slashdot090221.txt"
]


def choose_test(options: list):
    ans = 0
    print("Choose type of network you want to analize: ")
    while True:
        for i in range(len(options)):
            print(f"{i}: {options[i]}")

        try:
            ans = int(input(">>"))
            if ans in range(len(options)):
                break
            else:
                print("Try again!")
        except:
            print("Try again!")
    
    return ans

def main():
    ans = choose_test(network_labels)
    graph, diGraph = load_epinions(network_files[ans])
    
    input(">>Model generated>>")
    tester = Tester(graph, transform= lambda G, edge : '+' if G[edge[0]][edge[1]]['sign'] > 0 else '-')
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
    tester.directed_graph_metrics(diGraph)
    input(">>next>>")
    tester.draw_network(graph)
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
        tester.draw_network(cluster_network, name=True) 
    else:
        print("Cluster network has only one node. Nothing to analize...")
    input(">>Thats it>>")



if __name__ == "__main__":
    main()