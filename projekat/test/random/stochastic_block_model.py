import networkx as nx
from sna_implementation.tester.test_perform import Tester
from sna_implementation.models.models import get_stochastic_block_model, get_planted_partition_model


methods_labels = [
    "Stochastic Block Model",
    "Planted Partition Model"
]


methods = [
    get_stochastic_block_model,
    get_planted_partition_model
]

def choose_test(options: list):
    ans = 0
    print("Choose type of network you want to analize: ")
    while True:
        for i in range(len(options)):
            print(f"{i}: {options[i]}")

        try:
            ans = int(input(">> "))
            if ans in range(len(options)):
                break
            else:
                print("Try again!")
        except:
            print("Try again!")
    
    return ans



def main():

    ans = choose_test(methods_labels)
    graph = methods[ans]()
    input(">>Model generated>>")
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
        tester.draw_network(cluster_network, layout= "kamanda", name=True) 
    else:
        print("Cluster network has only one node. Nothing to analize...")
    input(">>Thats it>>")



if __name__ == "__main__":
    main()