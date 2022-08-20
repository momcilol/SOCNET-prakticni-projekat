from math import log
from unittest import result
import networkx as nx
import metrics.metric_analysis as ma
import cluster as cl
from cluster.signed_clusterable_network import SignedNetworkComponentClusterer

class Tester:

    def __init__(self, graph: nx.Graph, transform):
        self._sncc = SignedNetworkComponentClusterer(graph, transform)


    def print_network(self):
        print(f"Input network: {self._sncc._graph}")
        self._print_nodes_and_edges(self._sncc._graph)
        print(f"Cluster network: {self._sncc.get_cluster_graph().number_of_nodes} clusters")
        self._print_cluster_network()


    def _print_nodes_and_edges(self, graph: nx.Graph):
        print(f"Nodes: {list(graph.nodes())}")
        print(f"Edges: {list(graph.edges())}", end='\n\n')


    def _print_cluster_network(self):

        cluster_graph = self._sncc.get_cluster_graph()
        coalitions = self._sncc.get_coalitions()
        non_coalitions = self._sncc.get_non_coalitions()

        trivial = 0

        for coalition in coalitions:
            triv = coalition.number_of_nodes() == 1
            if triv:
                trivial += 1
            
            print(f"{coalition.name}: {'trivial ' if triv else ''}coalition")
            self._print_nodes_and_edges(coalition)
            


        for cluster in non_coalitions:
            print(f"{cluster.name} cluster")
            self._print_nodes_and_edges(cluster)
            print(f"Problematic edges: {len(self._sncc.get_problematic_edges(cluster))} edges")
            self._print_negative_edges()


        print(f"Number of trivial coalitions: {trivial}", end='\n\n')
        
        print("Inter-component edges: ")
        for edge in cluster_graph.edges():
            print(f"{edge[0].name} ({self._sncc._transform(edge)}) {edge[1].name}", end=", ")
        print()

         

    
    def _print_negative_edges(self, graph: nx.Graph):
        for edge in self._sncc.get_negative_edges(graph):
            print(f"{edge[0].name} ({self._sncc._transform(edge)}) {edge[1].name}", end=", ")


    def check_clusterability(self):
        clusterable = len(self._sncc.get_non_coalitions()) > 0
        clust = "not " if clusterable else ""
        details = f": {len(self._sncc.get_non_coalitions())} clusters with {len(self._sncc.get_negative_edges())} problematic edges"
        print(f"Network is {clust}culsterable {details if clusterable else ''}") 
        num_coalitions = len(self._sncc.get_coalitions())
        num_components = len(self._sncc.get_components())
        num_trivial = len([x for x in self._sncc.get_coalitions() if x.number_of_nodes() == 1])
        print(f"{num_coalitions} out of {num_components} clusters are coalitions, where {num_trivial} are trivial", end="\n\n")

    
    def show_degree_information(self, graph: nx.Graph):
        nodes_per_degree, degree_distribution, complementary_cumulative_distribution, average_degree, network_density = ma.get_degree_information(graph)
        ma.draw_degree_info(nodes_per_degree, ma.degree_info_metric[0])
        ma.draw_degree_info(degree_distribution, ma.degree_info_metric[1])
        ma.draw_degree_info(complementary_cumulative_distribution, ma.degree_info_metric[2])
        print(f"Average degree: {average_degree : .4f}")
        dense = "dense" if network_density > 0.7 else "sparse"
        print(f"Network density: {network_density : .4f} (network is {dense})", end="\n\n")


    def print_centralities(self, graph: nx.Graph, has_name=False):
        metrics_results = [
            ma.get_betweeness_centrality(graph),
            ma.get_closeness_centrality(graph),
            ma.get_eigenvector_centrality(graph),
            ma.get_clustering_coefficients(graph)
        ]
        
        for i in range(len(metrics_results)):
            ma.print_node_metrics_results(metrics_results[i], ma.node_metrics[i], has_name)
        print(f"Average clustering coefficinet: {nx.average_clustering(graph)}", end="\n\n")



    def directed_graph_metrics(graph: nx.DiGraph):
        page_rank = ma.get_page_rank(graph)
        ma.print_node_metrics_results(page_rank, "Page Rank")
        hits = ma.get_hits_results(graph)
        ma.print_hits_results(hits)    
    

    def print_assortativity(self, graph: nx.Graph):
        ma.draw_assortativity(graph)
        print(f"Pearson coefficient: {ma.get_pearson_coefficient(graph)}")
        print(f"Spearman coefficient: {ma.get_spearman_coefficient(graph)}")


    def print_k_core_decomposition(self, graph: nx.Graph):
        k_core_decomposition = ma.get_k_core_decomposition(graph)
        print(f"K-core decomposition: {graph.name}")
        max_layer = max(k_core_decomposition.values())
        layers = {i: set() for i in range(max_layer + 1)}
        for node, value in k_core_decomposition:
            layers[value].add(node)
        
        for i in range(len(layers)):
            print(f"Shell {i}: {layers[i]}")
        
        print()

    
    def print_small_world_metrics(self, graph:  nx.Graph):
        small_world, efficiency, global_efficiency = ma.get_small_world_metric_results(graph)
        print(f"""
            SMALL WORLD METRICS
        """)
        print(f"Small world coefficient: {small_world : .4f}, log(number of nodes) = {log(graph.number_of_nodes, 10) : .4f}")
        print(f"Giant component network efficiency: {efficiency : .4f}")
        print(f"Network efficiency: {global_efficiency: .4f}")
        print(f"Diameter: {ma.get_diameter(graph)}")
        print(f"Radius: {ma.get_radius(graph)}")
    

    
    