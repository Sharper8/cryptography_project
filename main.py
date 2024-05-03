# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# imports
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

import numpy as np
from node_object import *

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# functions
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def show_matrice_clean(matrice, name):
    print("\n --- ", name, " ---")
    for elt in matrice:
        print("[", end="")
        for elt2 in elt:
            print(elt2, end=" ")
        print("]")
    
def see_links(links):
    for key in links:
        print(key, " : ", links[key],"\n")
        
def get_weight(node1, node2, encoding_table):
    # TODO  useless/better in ascii ? + can it be modulated with symmetrical key ?
    return (encoding_table.index(node2) - encoding_table.index(node1))
   
def connect_nodes(nodes, lenght_alpha):
    # Loop over the nodes
    for elt in nodes:
        #if elt2 not in node neighbor, add the lengh as the weight
        lenght_alpha+=1
        for elt2 in nodes :
            if elt2 != elt:
                if elt2 not in elt.neighbors:
                    elt.add_neighbor(elt2, lenght_alpha)
                    elt2.add_neighbor(elt, lenght_alpha)

def minimum_spanning_tree(graph_matrix):
    num_nodes = len(graph_matrix)
    visited = [False] * num_nodes
    tree_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    # begin with the first node
    visited[0] = True
    while not all(visited):
        min_edge_weight = float('inf')
        min_edge_start = None
        min_edge_end = None
        for i in range(num_nodes):
            if visited[i]:
                for j in range(num_nodes):
                    if not visited[j] and graph_matrix[i][j] != 0:
                        if graph_matrix[i][j] < min_edge_weight:
                            min_edge_weight = graph_matrix[i][j]
                            min_edge_start = i
                            min_edge_end = j

        # add vertice at result
        tree_matrix[min_edge_start][min_edge_end] = min_edge_weight
        tree_matrix[min_edge_end][min_edge_start] = min_edge_weight
        visited[min_edge_end] = True

    return tree_matrix

def cipher(data, public_key):
    print("ciphering data : ", data)
    encoding_table = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k","l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v","w", "x", "y", "z"]
    nodes = []
    size = len(data)
    for i in range (size):
        new_node = Node(i, data[i])
        # append neighbors 
        nodes.append(new_node)
    for i in range(len(nodes)):
        # add previous neighbor
        nodes[i].add_neighbor(nodes[(i-1)%size], get_weight(data[(i-1)%size], data[i],encoding_table))
        nodes[i].add_neighbor(nodes[(i+1)%size], get_weight(data[i], data[(i+1)%size],encoding_table))
    # for node in nodes:
    #     print("node : ", node.id, " => ", node.char, " neighbors : ", node.__str__())   
    connect_nodes(nodes, len(encoding_table))
    spec_chara = "a"
    node_spec = Node(len(data)+1, spec_chara)
    node_spec.add_neighbor(nodes[0], get_weight(spec_chara, data[0],encoding_table))
    nodes[0].add_neighbor(node_spec, get_weight(spec_chara,data[0],encoding_table))
    nodes.insert(0, node_spec)
    X1 = []
    # copy the dict keys into a list
    for i in range (len(nodes)):
        temp = []
        for j in range (len(nodes)):
            if nodes[i] in nodes[j].neighbors.keys():
                temp.append(nodes[i].neighbors[nodes[j]])
            else:
                temp.append(0)
        X1.append(temp)
    show_matrice_clean(X1, "X1")    
    # X2 = minimum_spanning_tree(X1)
    X2 = np.zeros((len(X1), len(X1))).astype(int)
    for i in range(len(nodes)):
        if i==len(nodes)-1:
            break
        else :
            X2[i][i+1] = nodes[i].neighbors[nodes[i+1]]
            X2[i+1][i] = nodes[i].neighbors[nodes[i+1]]
    show_matrice_clean(X2, "X2")
    
    matrix2 = np.zeros((len(X2), len(X2))).astype(int)
    for i in range(len(X2)):
        for j in range(len(X2[i])):
            if i==j:
                matrix2[i][j] = i
            else:
                matrix2[i][j] = X2[i][j]
                
    X3 = np.dot(X1,matrix2)
    Ct= np.dot(public_key, X3)
    return (X1, Ct)
    
    
def decipher(ciph_data, public_key):
    X1 = ciph_data[0]
    ciph_data_mess = ciph_data[1].astype(int)
    public_key_inv = np.linalg.inv(public_key).astype(int)
    X1_inv = np.linalg.inv(X1)
    X3 = np.dot(public_key_inv, ciph_data_mess)
    X2_V1 = np.dot(X1_inv,X3)
    # show_matrice_clean(X2_V1, "RX2")
    X2_rounded = np.round(X2_V1,0)
    X2 = X2_rounded.astype(int)
    print("\nDeciphering`...")
    #TODO ameliorer pour table ascii
    encoding_table = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k","l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v","w", "x", "y", "z"]
    head = 0
    word = ""
    for i in range(len(X2)):
        if i==len(X2)-1:
                break
        elif i==(len(X2)-1) :
            head+=int(X2[i][i-1])
            word+=encoding_table[head]
        else :
            head+=int(X2[1+i][i])
            word+=encoding_table[head]

    return(word)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# main code
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# TODO user input ?
data  = "code"
# public key
n = len(data)+1
public_key = np.zeros((n, n)).astype(int)  
for i in range(n):
    for j in range(i , n): 
        public_key[i, j] = 1
        
print("---")

ciphered_data = cipher(data, public_key)
print("\n sending : ",ciphered_data)
deciphered_data = decipher(ciphered_data, public_key)

print("\nMot original : ",data)
print("/versus, décodé : ",deciphered_data)