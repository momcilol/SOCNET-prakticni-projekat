import networkx as nx
import sna_implementation.clustering.edge_sign as es
import itertools

class SignedNetworkComponentClusterer: 

    # Konstruktor
    def __init__(self, graph: nx.Graph, transform):
        self._graph = graph
        self._transform = transform


    # ===== Deo za analizu mreze ============

    # Pokrecemo analizu grafa, pronalazenje komponenti
    def analyze(self):
        self.__possible_component_edges = set()
        self.__visited = set()
        self.__cluster_graph = nx.Graph()
        self.__components = []
        self.__negative_edges = {}

        self.__find_components()

        self.__create_cluster_graph()

        self.__components.sort(key=self.__sort_key, reverse=True)


    def __sort_key(self, value: nx.Graph):
        return value.number_of_nodes()


    # Pronalazimo sve komponente
    def __find_components(self):
        for node in self._graph:
            if node not in self.__visited:
                self.__identify_component(node)
    

    # Identifikujemo pojedinacnu komponentu
    def __identify_component(self, begin_node):
        node_queue = []
        node_queue.append(begin_node)
        self.__visited.add(begin_node)

        component = nx.Graph()
        component.add_node(begin_node)

        for curr in node_queue:
            # print(f"Curr: {curr}")
            for neigh in self._graph.neighbors(curr):
                # print(f"Neigb: {neigh}")
                # print(f"Edge: ({curr}, {neigh}) {self._transform(self._graph, (curr, neigh))}")
                # print(self._transform(self._graph, (curr, neigh)) == es.EdgeSign.NEGATIVE.value)
                
                if self._transform(self._graph, (curr, neigh)) == es.EdgeSign.NEGATIVE.value:
                    self.__possible_component_edges.add((curr, neigh))
                    continue
                
                if neigh not in self.__visited:
                    self.__visited.add(neigh)
                    node_queue.append(neigh)
                    component.add_node(neigh)
                
                if not component.has_edge(curr, neigh):
                    component.add_edges_from([(curr, neigh, self._graph[curr][neigh])])

                # print(node_queue)

        self.__detect_negative_edges(component)

        self.__components.append(component)
        component.name = "COMP " + str(self.__components.index(component))
        print(component)


    # Sakupimo sve negativne grane unutar komponente
    def __detect_negative_edges(self, component: nx.Graph):
        self.__negative_edges[component] = []
        nodes = list(component.nodes()) 

        if len(nodes) == 1 or len(nodes) == 2:
            return
        
        for i in range(0, len(nodes) - 1):
            for j in range(i + 1, len(nodes)):
                if self._graph.has_edge(nodes[i], nodes[j]) and self._transform(component, (nodes[i], nodes[j])) == es.EdgeSign.NEGATIVE:
                    self.__negative_edges[component].append((nodes[i], nodes[j], self._graph[nodes[i]][nodes[j]])) 


    # Konstruisemo graf od dobijenih komponenata
    def __create_cluster_graph(self):
        
        if not self.__possible_component_edges:
            return
        
        for edge in self.__possible_component_edges:
            node1 = edge[0]
            node2 = edge[1]

            component1 = [x for x in self.__components if x.has_node(node1)][0]
            component2 = [x for x in self.__components if x.has_node(node2)][0]

            if component1 not in self.__cluster_graph:
                self.__cluster_graph.add_node(component1)

            if component2 not in self.__cluster_graph:
                self.__cluster_graph.add_node(component2)

            if component1 == component2 or self.__cluster_graph.has_edge(component1, component2):
                continue

            self.__cluster_graph.add_edge(component1, component2, sign='-')

    # ========= Kraj analize mreze ===========

    # ========== Getteri ===========

    def get_components(self):
        return self.__components

    
    def get_cluster_graph(self):
        return self.__cluster_graph

    
    def get_giant_component(self) -> nx.Graph:
        return self.__components[0]

    
    def get_coalitions(self):
        return [c for c in self.__components if len(self.__negative_edges[c]) == 0]


    def get_non_coalitions(self):
        return [c for c in self.__components if len(self.__negative_edges[c]) > 0]


    def get_negative_edges(self):
        return list(itertools.chain(*list(self.__negative_edges.values())))   


    def get_problematic_edges(self, component: nx.Graph):
        return self.__negative_edges[component: nx.Graph]



    
















        


    

