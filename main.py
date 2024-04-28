# In this project, we will implement an encryption and 
# deciphering using graph theory, and more specifically the concept of 
# of a covering tree.
# This algorithm is a symmetric key algorithm. It is based on the idea of finding 
# a minimum weight covering tree (using Kruskal or Prim)
import numpy as np

# functions

def see_links(links):
    for key in links:
        print(key, " : ", links[key],"\n")
        

def get_weight(node1, node2):
    # TODO  useless/better in ascii ? + can it be modulated with symmetrical key ?
    encoding_table = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k","l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v","w", "x", "y", "z"]
    return (encoding_table.index(node2) - encoding_table.index(node1))


def connect_nodes(nodes, links):
    # Loop over the nodes
    for i in range(len(nodes)):
        # If the node is not in the links dictionary, add it with an empty dictionary as value
        if nodes[i] not in links:
            links[nodes[i]] = {}
        # Add a link to only the next element 
        links[nodes[i]][nodes[(i+1)%len(nodes)]] = get_weight(nodes[i], nodes[(i+1)%len(nodes)])
        # Add a link to only the previous element
        if nodes[(i+1)%len(nodes)] not in links:
            links[nodes[(i+1)%len(nodes)]] = {}
        links[nodes[(i+1)%len(nodes)]][nodes[i]] = links[nodes[i]][nodes[(i+1)%len(nodes)]]
    
    #add the remaining nodes with wieght > len(encoding_table)
    iterator = 26
    for elt in nodes:
        iterator += 1
        for elt2 in nodes:
            if elt2 not in links[elt] and elt != elt2:
                links[elt][elt2] = iterator
                links[elt2][elt] = links[elt][elt2]
    
    # print("links after covering tree: ",links)
    
# def get_minimum_spanning_tree(shortest_tree, shortest_path):
#     # Loop over the nodes
#     for i in range(len(shortest_path)):
        
#         if i == len(shortest_path)-1:
#             shortest_tree[shortest_path[i]] = {}
#             break
#         if shortest_path[i] not in shortest_tree:
#             shortest_tree[shortest_path[i]] = {}
#         # construct the minimum spanning tree
#         # print("shortest_path : ", shortest_path)
#         print("For the element: ", shortest_path[i], "we add ", shortest_path[i+1], "like that : ", shortest_path[i+1],":",links[shortest_path[i]][shortest_path[i+1]])
#         shortest_tree[shortest_path[i]] = {shortest_path[i+1]:links[shortest_path[i]][shortest_path[i+1]]}
#         print("And reverse For the element: ", shortest_path[i+1], "we add ", shortest_path[i], "like that : ", shortest_path[i],":",links[shortest_path[i]][shortest_path[i+1]])
#         shortest_tree[shortest_path[i+1]] = {shortest_path[i]:links[shortest_path[i]][shortest_path[i+1]]}



    
def cipher(data, public_key):
    nodes = []
    # example of links = {a: {b: 1, c: 2}, b: {a: 1, c: 3}, c: {a: 2, b: 3}}
    links = {}
    for elt in data:
        nodes.append(elt)
    # print("nodes : ",nodes)
    # connect the nodes of the base data
    connect_nodes(nodes, links)
    # print("links : ",links)
    
    spec_chara = "a"
    links[spec_chara] = {data[0]: get_weight(spec_chara, data[0])}
    links[data[0]][spec_chara] = links["a"][data[0]]
    # see_links(links)
    # put the links into symmetric matrix
    X1 = []
    # copy the dict keys into a list
    keys = list(links.keys())
    # print("keys: ",keys)
    keys.remove(spec_chara)
    keys.insert(0,spec_chara)
    for key in keys:
        # print("For the key: ",key)
        temp = []
        for i in range(len(keys)):
            # print('is ',keys[i],' in ',links[key])
            if keys[i] in links[key]:
                # print('yes, then add the value:',links[key][keys[i]])
                temp.append(links[key][keys[i]])
            else:
                temp.append(0)
        # print(temp)
        X1.append(temp)
    
    # construct the minimum spanning tree
    # span_tree = get_minimum_spanning_tree(matrix) TODO do i have to calculate or will it alaways be the same as the word ?
    # split the data in a table with one character per element
    shortest_path = list(spec_chara+data)
    # print("shortest_path : ", shortest_path)
    shortest_tree = {}
    for i in range(len(shortest_path)):
        if i == len(shortest_path)-1:
            shortest_tree[shortest_path[i]] = {}
            break
        # Vérifie si la clé shortest_path[i] est déjà dans shortest_tree, sinon l'ajoute
        if shortest_path[i] not in shortest_tree:
            shortest_tree[shortest_path[i]] = {}
        # Vérifie si la clé shortest_path[i+1] est déjà dans shortest_tree, sinon l'ajoute
        if shortest_path[i+1] not in shortest_tree:
            shortest_tree[shortest_path[i+1]] = {}
        # print("element : ", shortest_path[i], "-> add ", shortest_path[i+1], ": { ", shortest_path[i+1],":",links[shortest_path[i]][shortest_path[i+1]], "}")
        shortest_tree[shortest_path[i]][shortest_path[i+1]] = links[shortest_path[i]][shortest_path[i+1]]
        # print("Reverse : ", shortest_path[i+1], "-> add ", shortest_path[i], "like that : ", shortest_path[i],":",links[shortest_path[i]][shortest_path[i+1]])
        shortest_tree[shortest_path[i+1]][shortest_path[i]] = links[shortest_path[i]][shortest_path[i+1]]

    # see_links(shortest_tree)
    
    matrix2 = []
    # print("Shortest tree", shortest_tree)
    keys = list(shortest_tree.keys())
    for key in keys:
        # print("For the key: ",key)
        temp = []
        for i in range(len(keys)):
            # print('is ',keys[i],' in ',links[key])
            if keys[i] in shortest_tree[key]:
                # print('yes, then add the value:',links[key][keys[i]])
                temp.append(shortest_tree[key][keys[i]])
            else:
                temp.append(0)
        # print(temp)
        matrix2.append(temp)
    # see_links(shortest_tree)
    matrix2 = []
    # print("Shortest tree", shortest_tree)
    keys = list(shortest_tree.keys())
    for key in keys:
        # print("For the key: ",key)
        temp = []
        for i in range(len(keys)):
            # print('is ',keys[i],' in ',links[key])
            if keys[i] in shortest_tree[key]:
                # print('yes, then add the value:',links[key][keys[i]])
                temp.append(shortest_tree[key][keys[i]])
            else:
                temp.append(0)
        # print(temp)
        matrix2.append(temp)
    for elt in matrix2:
        print(elt)
    # print("matrix2: ",matrix2)
    for i in range(len(matrix2)):
        for j in range(len(matrix2[i])):
            if i==j:
                matrix2[i][j] = i
    
    X3 = np.dot(X1, matrix2)
    print("---")
    
    
    ciphered_data = np.dot(public_key, X3)
    for elt in ciphered_data:
        print(elt)
    print("X1 : ")
    for elt in X1:
        print(elt)
    return (X1, ciphered_data)
    
    
def decipher(ciph_data, public_key):
    X1 = ciph_data[0]
    ciph_data_mess = ciph_data[1].astype(int)
    public_key_inv = np.linalg.inv(public_key).astype(int)
    print("public_key_inv : ")
    for elt in public_key_inv:
        print(elt)
        
    X1_inv = np.linalg.inv(X1)
    print("X1 received : ")
    for elt in X1:
        print(elt)
    print("message receiued : ")
    for elt in ciph_data_mess:
        print(elt)
    X3 = np.dot(ciph_data_mess, public_key_inv).astype(int)
    X2 = np.dot(X3, X1_inv).astype(int)
    print("X2 : ")
    for elt in X2:
        print(elt)
        
    encoding_table = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k","l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v","w", "x", "y", "z"]
    for i in range(len(X2)):
        if i==0 :
            print("elt : ", X2[i][i+1], " => ", encoding_table[1+int(X2[i][i+1])])
        else :
            print("elt : ", X2[i][i-1], " => ", encoding_table[1+int(X2[i][i-1])])


# main code
data  = "code"
# public key
n = len(data)+1
public_key = np.zeros((n, n)).astype(int)  
for i in range(n):
    for j in range(i , n): 
        public_key[i, j] = 1

for elt in public_key:
    print(elt)

print("---")

ciphered_data = cipher(data, public_key)

# print(ciphered_data)
deciphered_data = decipher(ciphered_data, public_key)
# print(deciphered_data)


#tests

