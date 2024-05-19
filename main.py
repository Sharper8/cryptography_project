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
    # Calculer la largeur maximale de chaque colonne
    max_widths = [max(len(str(elt)) for elt in col) for col in zip(*matrice)]
    for row in matrice:
        print("[", end="")
        for i, elt in enumerate(row):
            print("{:>{width}}".format(elt, width=max_widths[i] + 1), end=" ")
        print("]")

def test_singular(matrix):
    # if the matrix is singular, return True
    if np.linalg.det(matrix) == 0:
        return True
    else:
        return False
    
def see_links(links):
    for key in links:
        print(key, " : ", links[key],"\n")
        
def get_weight(char1, char2):
    return (ord(char2) - ord(char1))
   
def connect_nodes(nodes, lenght_alpha):
    #Create a connected graph
    
    # Loop over the nodes
    for elt in nodes:
        #if elt2 not in node neighbor, add the lengh as the weight
        lenght_alpha+=1
        for elt2 in nodes :
            if elt2 != elt:
                if elt2 not in elt.neighbors:
                    elt.add_neighbor(elt2, lenght_alpha)
                    elt2.add_neighbor(elt, lenght_alpha)

    
def create_matrix(matrix, data, lenght_alpha, spec_chara):
    init = 0
    while init == 0 or test_singular(matrix) == True:
        if init != 0:
            data = " " + data
            # print('iteration N°', init + 1)
        init += 1
        
        nodes = []
        size = len(data)
        for i in range(size):
            new_node = Node(i, data[i])
            # append neighbors 
            nodes.append(new_node)
        for i in range(len(nodes)):
            # add previous neighbor
            # print("enter")
            prev_index = (i - 1) % size
            # print("try on data prev", data[prev_index])
            next_index = (i + 1) % size
            # print("data |" , data, "| index ; " , i)
            # for char in data:
                # print(f"char n°{i} : ", char)
            w1 = get_weight(data[prev_index], data[i])
            w2 = get_weight(data[i], data[next_index])
            nodes[i].add_neighbor(nodes[prev_index], w1)
            nodes[i].add_neighbor(nodes[next_index], w2)
        connect_nodes(nodes, lenght_alpha)
        node_spec = Node(len(data)+1, spec_chara)
        
        #add the spec node to the graph at random position
        random_index = 3
        # random_index = np.random.randint(0, len(nodes))    
        new_nodes = [elt for elt in nodes]
        new_nodes.insert(0, node_spec)
        nodes.insert(random_index, node_spec)
        next_node_index = (random_index+1)%len(nodes)
        node_spec.add_neighbor(nodes[next_node_index], get_weight(spec_chara,nodes[next_node_index].char))
        nodes[next_node_index].add_neighbor(node_spec, get_weight(spec_chara,nodes[next_node_index].char))
        print("added node spec : ", node_spec.char, " at index : ", random_index, "and with a weight of", get_weight(spec_chara,nodes[next_node_index].char))
        
        matrix = []
        #takes a singluar matrix and return a non singular matrix by adding 
        mask_matrix = []
        # copy the dict keys into a list
        for i in range (len(nodes)):
            temp = []
            temp_mask = []
            for j in range (len(nodes)):
                if nodes[i] in nodes[j].neighbors.keys():
                    temp_mask.append(1)
                    temp.append(nodes[i].neighbors[nodes[j]])
                else:
                    temp_mask.append(0)
                    temp.append(0)
            matrix.append(temp)
            mask_matrix.append(temp_mask)
        
            # print("Matrix is singular, adding a random value to the matrix")
    # public key
    n = len(data)+1
    public_key = np.zeros((n, n)).astype(int)
    # TODO randomize the shared key ?  
    for i in range(n):
        for j in range(i , n): 
            public_key[i, j] = 1
    # print the final word in console
    print("Final word : ", [node.char for node in nodes])
    return matrix,mask_matrix, nodes, new_nodes, public_key
        

def minimum_spanning_tree(graph_matrix,mask_matrix):
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
        if mask_matrix[0][j] != 0:
            heapq.heappush(min_heap, (graph_matrix[0][j], 0, j))

    while min_heap and edge_count < num_nodes - 1:
        min_edge_weight, min_edge_start, min_edge_end = heapq.heappop(min_heap)

        if not visited[min_edge_end]:
            # Add edge to the tree
            tree_matrix[min_edge_start][min_edge_end] = min_edge_weight
            tree_matrix[min_edge_end][min_edge_start] = min_edge_weight
            print("added edge : ", min_edge_start, " to ", min_edge_end, " with weight : ", min_edge_weight)
            visited[min_edge_end] = True
            edge_count += 1

            # Add all edges from the newly visited node to the heap
            for j in range(num_nodes):
                if not visited[j] and mask_matrix[min_edge_end][j] != 0:
                    heapq.heappush(min_heap, (graph_matrix[min_edge_end][j], min_edge_end, j))

            # Add all edges from the newly visited node to the heap
            for j in range(num_nodes):
                if not visited[j] and mask_matrix[min_edge_end][j] != 0:
                    heapq.heappush(min_heap, (graph_matrix[min_edge_end][j], min_edge_end, j))

    return tree_matrix
    
def translate_neighbors(matrix, matrix_mask, index, preword,visited, head, flag, init):
    #recursively check if the neighbor has been visited, if not, add the weight to the preword
    print("\nIn index : ", index)
    print("Adding the character : ", chr(head), "in the index : ", matrix[index][index], "of preword")
    preword[matrix[index][index]]=chr(head)
    #stopcondition : reaching a neigbor with neighbors already visited
    new_neighbors = False
    print("line : ", matrix[index])
    print("visi : ", visited)
    temp = []
    for i in range(len(matrix[index])):
        
        #if this is an arc of value 0
        test = ((matrix[index][i] == 0) and(matrix_mask[index][i] <128)) and (not visited[i]) and matrix_mask[index][i] == 0
        if not init:
            #if the value was in fact a 0, we count it, else we don't
            if test :
                print(f"a route with weight 0 exists in coord {index} and {i} ; init = {init}")
        else : 
            test = not test
        
        if ((matrix[index][i] != 0) or test)and not visited[i]:
            # needs to ignore if this is a diagonal number
            if i != index:
                #if this line as some neigbors that have not been visited
                new_neighbors = True
                temp.append(i)
                print("new neighbors to visit at index : ", i)

    # if all neighbors were vsited 
    if new_neighbors == False:
        print("no new neighbors to visit")
        return 0
    # if there is new neighbors
    for i in range(len(temp)):
        # print("DEBUG line : ", matrix[index], "id: ", i, "temp : ", temp[i])
        # this flags tell if we are going in the right direction : if the index in the word of next char is bigger
        # if our id in the diagonal is less than what we are going to calculate, we are going in the right direction
        if matrix[index][index] < matrix[temp[i]][temp[i]]: #special case if len(word)->0
            flag = 1
            print("current index is : ", index, " next is : ", temp[i], " flag is : ", flag)
            if matrix[temp[i]][temp[i]]==len(preword)-1 and matrix[index][index]==1:
                print("Mauvais SENS FINALEMENT")
                flag = -1
        else:
            flag = -1
            if matrix[temp[i]][temp[i]]==1 and matrix[index][index]==len(preword)-1:
                print("BON SENS FINALEMENT")
                flag = 1
            print("current index is : ", index, " next is : ", temp[i], " flag is : ", flag)
            # 
        print("temp : ", temp[i]," Head : ", head, " = ", chr(head))
        visited[index] = True
        print("1head = ", chr(head), " += ", flag*matrix[index][temp[i]])
        head+=flag*(matrix[index][temp[i]])
        print("2head = ", chr(head))
        # print(f"DEBUG  {matrix[index]} => MA[{index}][{index}] = {matrix[index][index]}")
        # print("preword : ", preword)
        translate_neighbors(matrix, matrix_mask, temp[i], preword, visited, head, flag, False)
        head-=flag*(matrix[index][temp[i]])
    

def cipher(data,spec_chara):
    print("ciphering data : ", data)
    len_ascii = 128
    X1 = []
    print('-----Nodes-----')

    tupleres = create_matrix(X1, data, len_ascii, spec_chara)
    X1 = tupleres[0]
    # mask will help determine the min span tree algo to see if 0 is an empty value or a weight
    mask_matrix = tupleres[1]
    nodes = tupleres[2]
    new_nodes = tupleres[3]
    public_key = tupleres[4]
        
    show_matrice_clean(X1, "X1")    
    
    X2 = minimum_spanning_tree(X1, mask_matrix)
    show_matrice_clean(X2, "X2")

    matrix2 = np.zeros((len(X2), len(X2))).astype(int)
    for i in range(len(X2)):
        for j in range(len(X2[i])):
            if i==j:
                matrix2[i][j] = new_nodes.index(nodes[i])
            else:
                matrix2[i][j] = X2[i][j]
    show_matrice_clean(matrix2, "matrix2")
    
    X3 = np.dot(X1,matrix2)
    show_matrice_clean(X3, "X3")    
    Ct= np.dot(public_key, X3)
    show_matrice_clean(Ct, "CT")    
    return (X1, Ct,public_key)
    
    
def decipher(ciph_data,spec_chara):
    print("\nDeciphering`...")
    X1 = ciph_data[0]
    
    ciph_data_mess = ciph_data[1].astype(int)
    public_key = ciph_data[2]
    public_key_inv = np.linalg.inv(public_key).astype(int)
    show_matrice_clean(X1, "X1 RECEIVED")
    # print("\n Try inverting X1\n ")
    X1_inv = np.linalg.inv(X1)
    X3 = np.dot(public_key_inv, ciph_data_mess)
    show_matrice_clean(X3, "X3 RECEIVED")
    X2_V1 = np.dot(X1_inv,X3)
    X2_rounded = np.round(X2_V1,0)
    X2 = X2_rounded.astype(int)
    show_matrice_clean(X2, "X2 RECEIVED")

    flag = 1
    head = ord(spec_chara)
    # preword = ""
    preword_filled = ["0" for _ in range(len(X2))]
    ord_list_indexes=[]
    # list in what order needs to be read thje matrix to get the base word
    for i in range(len(X2)):
        for j in range(len(X2[i])):
            if X2[j][j] == i: 
                ord_list_indexes.append(j)
    
    # visited nodes
    visited = [False] * len(X2)
    #TODO implement the following numbers of 0
    translate_neighbors(X2, X1, ord_list_indexes[0], preword_filled, visited, head, flag, True)
    
    # print("Debug : the constructed word", preword_filled)    
    #reconstruct the word from the list
    word=""
    for i in range(1,len(preword_filled)):
        word+=preword_filled[i]
    
    return(word)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# main code
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# TODO user input ? 
data  = "J'ai réussi :!: : : : : :"
#probeleme du double element possible de work around avec des espaces
spec_chara = "!"

print("---")

ciphered_data = cipher(data,spec_chara)
print("\n sending : ",ciphered_data)
deciphered_data = decipher(ciphered_data,spec_chara)

print("\nMot original : ",data)
print("/versus, décodé : ",deciphered_data)