import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools as iter

from sympy import re


def get_signs_of_tris(tris_list, G):
    #tris_list = [[1,2,3],[4,5,3]]
    #all_signs = [['+', '-', '+'], []]
    all_signs = []
    for i in range(len(tris_list)):
        temp = []
        temp.append(G[tris_list[i][0]][tris_list[i][1]]['sign'])
        temp.append(G[tris_list[i][1]][tris_list[i][2]]['sign'])
        temp.append(G[tris_list[i][2]][tris_list[i][0]]['sign'])
        all_signs.append(temp)
    return all_signs


def count_unstable(all_signs):
    stable = 0
    unstable = 0
    for i in range(len(all_signs)):
        if all_signs[i].count('+') == 3 or all_signs[i].count('+') == 1:
            stable += 1
        elif all_signs[i].count('+') == 2 or all_signs[i].count('+') == 0:
            unstable += 1
    
    print('Number of stable triangles out of ', stable + unstable, ' are ', stable)
    print('Number of unstable triangles out of ', stable + unstable, ' are ', unstable)

    return unstable


def move_a_tri_to_stable(G, tris_list, all_signs):
    found_unstable = False
    while(found_unstable == False):
        index = random.randint(0, len(tris_list) - 1)
        if all_signs[index].count('+') == 2 or all_signs[index].count('x') == 0:
            found_unstable = True
        else:
            continue 

    # move the unstable triangle to stable state
    r = random.randint(1, 3)
    if all_signs[index].count('+') == 2:
        if r == 1:
            if G[tris_list[index][0]][tris_list[index][1]]['sign'] == '+':
                G[tris_list[index][0]][tris_list[index][1]]['sign'] = '-'

            elif G[tris_list[index][0]][tris_list[index][1]]['sign'] == '-':
                G[tris_list[index][0]][tris_list[index][1]]['sign'] = '+'

        elif r == 2:    
            if G[tris_list[index][1]][tris_list[index][2]]['sign'] == '+':
                G[tris_list[index][1]][tris_list[index][2]]['sign'] = '-'

            elif G[tris_list[index][1]][tris_list[index][2]]['sign'] == '-':
                G[tris_list[index][1]][tris_list[index][2]]['sign'] = '+'
            
        elif r == 3:
            if G[tris_list[index][2]][tris_list[index][0]]['sign'] == '+':
                G[tris_list[index][2]][tris_list[index][0]]['sign'] = '-'

            elif G[tris_list[index][2]][tris_list[index][0]]['sign'] == '-':
                G[tris_list[index][2]][tris_list[index][0]]['sign'] = '+'
            
    elif all_signs[index].count('+') == 0:
        if r == 1:
            G[tris_list[index][0]][tris_list[index][1]]['sign'] = '+'
                
        elif r == 2:    
            G[tris_list[index][1]][tris_list[index][2]]['sign'] = '+'
            
        elif r == 3:
            G[tris_list[index][2]][tris_list[index][0]]['sign'] = '+'

    return G


def see_coalitions(G: nx.Graph):
    first_coalition = []
    second_coalition = []
    
    nodes = list(G.nodes)
    r = random.choice(nodes)

    first_coalition.append(r)

    processed_nodes = []
    to_be_processed = [r]

    for each in to_be_processed:
        if each not in processed_nodes:
            neigh = list(G.neighbors(each))

            for i in range(len(neigh)):
                if G[each][neigh[i]]['sign'] == '+':
                    if neigh[i] not in first_coalition:
                        first_coalition.append(neigh[i])
                    if neigh[i] not in to_be_processed:
                        to_be_processed.append(neigh[i])
                elif G[each][neigh[i]]['sign'] == '-':
                    if neigh[i] not in second_coalition:
                        second_coalition.append(neigh[i])
                        processed_nodes.append(neigh[i])

            processed_nodes.append(each)
    
    return first_coalition, second_coalition

G = nx.Graph()
n = 10
G.add_nodes_from([i for i in range(1, n+1)])
mapping = {1:"Hungary", 2:"Belarus", 3:"Austria", 4:"Serbia",
           5:"Switzerland", 6:"Germany", 7:"Holy See", 8:"Andorra",
           9:"Bulgaria", 10:"United Kingdom", 11:"France", 12:"Montenegro",
           13:"Luxembourg", 14:"Italy", 15:"Denmark"}
G = nx.relabel_nodes(G, mapping)

signs = ['+', '-'] 
for i in G.nodes(): 
    for j in G.nodes():
        if i != j:
            G.add_edge(i, j, sign = random.choice(signs))

# display the network
edge_lables = nx.get_edge_attributes(G, 'sign')
pos = nx.circular_layout(G)
# pos = nx.spring_layout(G)
nx.draw(G, pos, node_size = 5000)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_lables, font_size = 20, font_color = 'red')
plt.show()

# List of all triangles in network
nodes = G.nodes()
tris_list = [list(x) for x in iter.combinations(nodes, 3)]
all_signs = get_signs_of_tris(tris_list, G)
unstable = count_unstable(all_signs)
unstable_track = [unstable]

# Move network to stable state
while (unstable != 0):
    G = move_a_tri_to_stable(G, tris_list, all_signs)
    all_signs = get_signs_of_tris(tris_list, G)
    unstable = count_unstable(all_signs)
    unstable_track.append(unstable)

# plt.bar([i for i in range(len(unstable_track))], unstable_track)
# plt.show()

first, second = see_coalitions(G)

print(first)
print(second)

edge_lables = nx.get_edge_attributes(G, 'sign')
# pos = nx.circular_layout(G)
pos = nx.bipartite_layout(G, first)
nx.draw(G, pos, node_size = 5000)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_lables, font_size = 20, font_color = 'red')
plt.show()


# Draw coalitions
edge_lables = nx.get_edge_attributes(G, 'sign')

pos = nx.circular_layout(G)
nx.draw_networkx_nodes(G,  pos, nodelist = first, node_color = 'red', node_size = 4000, alpha = 0.8)
nx.draw_networkx_nodes(G,  pos, nodelist = second, node_color = 'blue', node_size = 4000, alpha = 0.8)

nx.draw_networkx_labels(G, pos, font_size = 10, font_family = 'sans-serif')

nx.draw_networkx_edges(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_lables, font_size = 20, font_color = 'green')

plt.show()
