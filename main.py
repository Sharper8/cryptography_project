# In this project, we will implement an encryption and 
# deciphering using graph theory, and more specifically the concept of 
# of a covering tree.
# This algorithm is a symmetric key algorithm. It is based on the idea of finding 
# a minimum weight covering tree (using Kruskal or Prim)
import numpy as np

# functions

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

def multiply_matrices(matrix1, matrix2):
    # Vérifier si les dimensions des matrices sont valides pour la multiplication
    if len(matrix1[0]) != len(matrix2):
        raise ValueError("! need to be same length")

    # Initialiser une nouvelle matrice résultante avec des zéros
    result = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]

    # Effectuer la multiplication
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                result[i][j] += matrix1[i][k] * matrix2[k][j]
                print("result[",i,",",j,"] += matrix1[",i,",",k,"] * matrix2[",k,",",j,"] = ",matrix1[i][k], " * ", matrix2[k][j], " = ", result[i][j])
    return result

    
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
            # shortest_tree[shortest_path[i]] = {}
            break
        # Vérifie si la clé shortest_path[i] est déjà dans shortest_tree, sinon l'ajoute
        if shortest_path[i] not in shortest_tree:
            shortest_tree[shortest_path[i]] = {}
        # Vérifie si la clé shortest_path[i+1] est déjà dans shortest_tree, sinon l'ajoute
        if shortest_path[i+1] not in shortest_tree:
            shortest_tree[shortest_path[i+1]] = {}
        print("element : ", shortest_path[i], "-> add ", shortest_path[i+1], ": { ", shortest_path[i+1],":",links[shortest_path[i]][shortest_path[i+1]], "}")
        shortest_tree[shortest_path[i]][shortest_path[i+1]] = links[shortest_path[i]][shortest_path[i+1]]
        print("Reverse : ", shortest_path[i+1], "-> add ", shortest_path[i], "like that : ", shortest_path[i],":",links[shortest_path[i]][shortest_path[i+1]])
        shortest_tree[shortest_path[i+1]][shortest_path[i]] = links[shortest_path[i]][shortest_path[i+1]]

    see_links(shortest_tree)
    
    X2 = []
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
    
        X2.append(temp)

    matrix2 = np.zeros((len(X2), len(X2))).astype(int)
    for i in range(len(X2)):
        for j in range(len(X2[i])):
            if i==j:
                matrix2[i][j] = i
            else:
                matrix2[i][j] = X2[i][j]
                
    show_matrice_clean(X1, "X1")
    show_matrice_clean(X2, "X2")
    show_matrice_clean(matrix2, "matrix2")
    # show_matrice_clean(public_key, "public_key")
    #  = np.dot(X1,X2)
    # show_matrice_clean(X3, "X3")
    X3 = np.dot(X1,matrix2)
    show_matrice_clean(X3, "X3test")
    Ct= np.dot(public_key, X3)
    show_matrice_clean(Ct, "Ct")
    return (X1, Ct)
    
    
def decipher(ciph_data, public_key):
    X1 = ciph_data[0]
    show_matrice_clean(X1, "RX1")
    ciph_data_mess = ciph_data[1].astype(int)
    public_key_inv = np.linalg.inv(public_key).astype(int)
    print("public_key_inv : ")
    for elt in public_key_inv:
        print(elt)

    X1_inv = np.linalg.inv(X1)
    
    X3 = np.dot(public_key_inv, ciph_data_mess)
    show_matrice_clean(X3, "RX3")
    X2 = np.dot(X1_inv,X3).astype(int)
    show_matrice_clean(X2, "RX2")
    
    # X3_test = np.dot(ciph_data_mess, public_key_inv)
    # show_matrice_clean(X3_test, "X3_test")
    # X2_test = np.dot(X3_test, X1_inv).astype(int)
    # show_matrice_clean(X2_test, "X2_test")
    print("\nDeciphering")
    encoding_table = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k","l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v","w", "x", "y", "z"]
    head = 0
    # for i in range(len(X2)):
    #     if i==(len(X2)-1) :
    #         head+=int(X2[i][i-1])
    #         print("elt : ", head, " => ", encoding_table[head])
    #     else :
    #         head+=int(X2[1+i][i])
    #         print("elt : ", head, " => ", encoding_table[head])
    #     print("head : ",head)
    i=0;
    head = 0
    for i in range(len(X2)):
        print(" i : ",i)
        if i==len(X2)-1:
            break
            head+=int(X2[i][i-1])
            print("last elt : ", head, " => ", encoding_table[head])
        elif i%2==0:
            head+=int(X2[i+1][i])
            print("elt : ", head, " => ", encoding_table[head])
        else :
            head+=int(X2[i][i+1])
            print("elt : ", head, " => ", encoding_table[head])
        

# main code
data  = "code"
# public key
n = len(data)+1
public_key = np.zeros((n, n)).astype(int)  
for i in range(n):
    for j in range(i , n): 
        public_key[i, j] = 1

# for elt in public_key:
#     print(elt)

print("---")

ciphered_data = cipher(data, public_key)

# print(ciphered_data)
deciphered_data = decipher(ciphered_data, public_key)
# print(deciphered_data)


#tests

