from math import log
import numpy as np
from unittest import result
import networkx as nx
import sna_implementation.metrics.metric_analysis as ma
from sna_implementation.visualiser.graph_visualiser import draw_graph
import sna_implementation.visualiser.metrics_visualiser as mv
from sna_implementation.clustering.signed_clusterable_network import SignedNetworkComponentClusterer

class Tester:

    def __init__(self, graph: nx.Graph, transform):
        self._sncc = SignedNetworkComponentClusterer(graph, transform)
        print("Analisys started")
        self._sncc.analyze()
        print("Analisys finished")



    def print_network(self):
        print(f"    Input network: {self._sncc._graph}")
        self._print_nodes_and_edges(self._sncc._graph)
        input(">>Print cultser network>>")
        print(f"    Cluster network: {self._sncc.get_cluster_graph().number_of_nodes()} clusters")
        self._print_cluster_network()


    def _print_nodes_and_edges(self, graph: nx.Graph):
        print(f"    Nodes: {list(graph.nodes())} \n    Total: {graph.number_of_nodes()}")
        print(f"    Edges: {list(graph.edges())} \n    Total: {graph.number_of_edges()}", end='\n\n')


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
            print(f"    Problematic edges: {len(self._sncc.get_problematic_edges(cluster))} edges")
            self._print_problematic_edges(cluster)
            print()

        print()
        print(f"    Number of trivial coalitions: {trivial}", end='\n\n')
        
        print("   Inter-component edges: ")
        for edge in cluster_graph.edges():
            print(f"{edge[0].name} (-) {edge[1].name}", end=", ")
        print()
        print(f"Total: {cluster_graph.number_of_edges()} edges")
        

    
    def _print_problematic_edges(self, graph: nx.Graph):
        for edge in self._sncc.get_problematic_edges(graph):
            print(f"{edge[0]} ({self._sncc._transform(self._sncc._graph, edge)}) {edge[1]}", end=", ")


    def check_clusterability(self):
        print("     CLUSTERABILITY & BALANCE")

        clusterable = not len(self._sncc.get_non_coalitions()) > 0
        balanced = clusterable and self._sncc.check_stuctural_balance()
        if not clusterable:
            clust = "not clusterable"
        elif clusterable and not balanced:
            clust = "clusterable and not balanced"
        else:
            clust = "balanced" 
        details = f": {len(self._sncc.get_non_coalitions())} clusters with {len(self._sncc.get_negative_edges())} problematic edges"
        print(f"    Network is {clust} {'' if clusterable else details}") 

        # Print coalitions and components
        num_coalitions = len(self._sncc.get_coalitions())
        num_components = len(self._sncc.get_components()) 
        num_trivial = len([x for x in self._sncc.get_coalitions() if x.number_of_nodes() == 1])
        print(f"{num_coalitions} out of {num_components} clusters are coalitions, where {num_trivial} are trivial", end="\n\n")

    
    def show_degree_information(self, graph: nx.Graph):
        print("     DEGREE INFO")
        nodes_per_degree, degree_distribution, complementary_cumulative_distribution, average_degree, network_density = ma.get_degree_information(graph)
        mv.draw_degree_info_loglog(nodes_per_degree, "ND")
        mv.draw_degree_info_loglog(degree_distribution, "DD")
        mv.draw_degree_info_loglog(complementary_cumulative_distribution, "CC")
        print(f"    Average degree: {average_degree : .4f}")
        dense = "dense" if network_density > 0.7 else "sparse"
        print(f"    Network density: {network_density : .4f} (network is {dense})", end="\n\n")


    def print_centralities(self, graph: nx.Graph, has_name=False):
        metrics_results = [
            ma.get_betweeness_centrality(graph),
            ma.get_closeness_centrality(graph),
            ma.get_eigenvector_centrality(graph),
            ma.get_clustering_coefficients(graph)
        ]
        
        for i in range(len(metrics_results)):
            ma.print_node_metrics_results(metrics_results[i], ma.node_metrics[i], has_name)
            print(f"""
            Max: {max(metrics_results[i].values()) : .4f}, 
            Min: {min(metrics_results[i].values()) : .4f},
            Average: {sum(metrics_results[i].values()) / float(len(metrics_results[i])) : .4f}""", end="\n\n")
            input(">>next>>")



    def directed_graph_metrics(self, graph: nx.DiGraph):
        page_rank = ma.get_page_rank(graph)
        ma.print_node_metrics_results(page_rank, "Page Rank")
        input(">>next>>")
        hits = ma.get_hits_results(graph)
        ma.print_hits_results(hits)    
    

    def print_assortativity(self, graph: nx.Graph):
        mv.draw_assortativity(graph)
        print(f"    Pearson coefficient: {ma.get_pearson_coefficient(graph) : .4f}")
        print(f"    Spearman coefficient: {ma.get_spearman_coefficient(graph) : .4f}")


    def print_k_core_decomposition(self, graph: nx.Graph, has_name=False):
        k_core_decomposition = ma.get_k_core_decomposition(graph)
        print(f"    K-core decomposition: {graph.name}")
        max_layer = max(k_core_decomposition.values())
        layers = {i: set() for i in range(max_layer + 1)}
        if has_name:
            for node, value in k_core_decomposition.items():
                layers[value].add(node.name)
        else:
            for node, value in k_core_decomposition.items():
                layers[value].add(node)
        
        for i in range(len(layers)):
            print(f"    Shell {i}: {layers[i]}")
        print()

        for i in range(len(layers)):
            print(f"    Shell {i} size: {len(layers[i])}")
        print()
        mv.draw_degree_info_log([len(layers[i]) for i in range(len(layers))], "KC")

    
    def print_small_world_metrics(self, graph:  nx.Graph):
        small_world, efficiency, global_efficiency, diameter, radius = ma.get_small_world_metric_results(graph)
        print(f"""
            SMALL WORLD METRICS
        """)
        print(f"    Small world coefficient: {small_world : .4f}, log(number of nodes) = {log(float(graph.number_of_nodes()), 10) : .4f}")
        print(f"    Giant component network efficiency: {efficiency : .4f}")
        print(f"    Network efficiency: {global_efficiency: .4f}")
        print(f"    Diameter: {diameter}")
        print(f"    Radius: {radius}")
    
    
    def draw_network(self, graph: nx.Graph, layout="spring", name=False):
        draw_graph(graph, self._sncc._transform, layout_key=layout, has_name=name)


    def print_similarity_matrix(self, graph: nx.Graph, name=False):
        sim = ma.get_sim_rank_coefficients(graph)
        mv.draw_matrix(graph, sim, "Sim Rank", name)
        aa = ma.get_adamic_adar_coefficients(graph)
        mv.draw_matrix(graph, aa, "Adamic Adar", name)

        
    
    
