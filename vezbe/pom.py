import graphlib
import networkx as nx


# graph = nx.Graph()
# graph.name = "moj graf"
# print(graph.name)

str = input("Unesite: ")
print(str.replace("{", "(").replace("}", ", {'sign': '+'})"))