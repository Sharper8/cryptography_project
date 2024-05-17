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
        
def get_weight(char1, char2):
    return (ord(char2) - ord(char1))
   
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
    #TODO caution if two times same letter, needs to be diff than 0
    
    num_nodes = len(graph_matrix)
    visited = [False] * num_nodes
    tree_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    edge_count = 0  # To keep track of the number of edges in the MST

    # Priority queue to store the edges (weight, start_node, end_node)
    import heapq
    min_heap = []

    # Start with the first node
    visited[0] = True
    for j in range(num_nodes):
        if graph_matrix[0][j] != 0:
            heapq.heappush(min_heap, (graph_matrix[0][j], 0, j))

    while min_heap and edge_count < num_nodes - 1:
        min_edge_weight, min_edge_start, min_edge_end = heapq.heappop(min_heap)

        if not visited[min_edge_end]:
            # Add edge to the tree
            tree_matrix[min_edge_start][min_edge_end] = min_edge_weight
            tree_matrix[min_edge_end][min_edge_start] = min_edge_weight
            visited[min_edge_end] = True
            edge_count += 1

            # Add all edges from the newly visited node to the heap
            for j in range(num_nodes):
                if not visited[j] and graph_matrix[min_edge_end][j] != 0:
                    heapq.heappush(min_heap, (graph_matrix[min_edge_end][j], min_edge_end, j))

    return tree_matrix

def cipher(data, public_key,spec_chara ):
    print("ciphering data : ", data)
    len_ascii = 128
    nodes = []
    size = len(data)
    for i in range (size):
        new_node = Node(i, data[i])
        # append neighbors 
        nodes.append(new_node)
    for i in range(len(nodes)):
        # add previous neighbor
        nodes[i].add_neighbor(nodes[(i-1)%size], get_weight(data[(i-1)%size], data[i]))
        nodes[i].add_neighbor(nodes[(i+1)%size], get_weight(data[i], data[(i+1)%size]))
    # for node in nodes:
    #     print("node : ", node.id, " => ", node.char, " neighbors : ", node.__str__())   
    connect_nodes(nodes, len_ascii)
    node_spec = Node(len(data)+1, spec_chara)
    node_spec.add_neighbor(nodes[0], get_weight(spec_chara, data[0]))
    nodes[0].add_neighbor(node_spec, get_weight(spec_chara,data[0]))
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
    X2_test = minimum_spanning_tree(X1)
    show_matrice_clean(X2_test, "X2_test")
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
    show_matrice_clean(X3, "X3")    

    Ct= np.dot(public_key, X3)
    show_matrice_clean(Ct, "CT")    

    return (X1, Ct)
    
    
def decipher(ciph_data, public_key,spec_chara):
    
    X1 = ciph_data[0]
    ciph_data_mess = ciph_data[1].astype(int)
    public_key_inv = np.linalg.inv(public_key).astype(int)
    print("\n Try inverting X1\n ")
    X1_inv = np.linalg.inv(X1)
    X3 = np.dot(public_key_inv, ciph_data_mess)
    X2_V1 = np.dot(X1_inv,X3)
    X2_rounded = np.round(X2_V1,0)
    X2 = X2_rounded.astype(int)
    print("\nDeciphering`...")
    head = ord(spec_chara)
    word = ""
    for i in range(len(X2)):
        if i==len(X2)-1:
                break
        elif i==(len(X2)-1) :
            head+=int(X2[i][i-1])
            word+=chr(head)
        else :
            head+=int(X2[1+i][i])
            word+=chr(head)

    return(word)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# main code
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# TODO user input ? 
data  = "Loot"
#probeleme du double element possible de work around avec des espaces
spec_chara = "a"

# public key
n = len(data)+1
public_key = np.zeros((n, n)).astype(int)  
for i in range(n):
    for j in range(i , n): 
        public_key[i, j] = 1
        
print("---")

ciphered_data = cipher(data, public_key,spec_chara,)
print("\n sending : ",ciphered_data)
deciphered_data = decipher(ciphered_data, public_key,spec_chara)

print("\nMot original : ",data)
print("/versus, décodé : ",deciphered_data)