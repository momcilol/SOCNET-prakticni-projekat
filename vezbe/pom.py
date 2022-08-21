import graphlib
import networkx as nx


# graph = nx.Graph()
# graph.name = "moj graf"
# print(graph.name)

# str = input("Unesite: ")
# print(str.replace("{", "(").replace("}", ", {'sign': '+'})"))

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

for edge in graph.edges:
    print(graph[edge[0]][edge[1]])