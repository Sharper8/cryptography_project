# In this project, we will implement an encryption and 
# deciphering using graph theory, and more specifically the concept of 
# of a covering tree.
# This algorithm is a symmetric key algorithm. It is based on the idea of finding 
# a minimum weight covering tree (using Kruskal or Prim)


# functions
def get_weight(node1, node2):
    # TODO  useless/better in ascii ? + can it be modulated with symmetrical key ?
    encoding_table = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k","l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v","w", "x", "y", "z"]
    return (encoding_table.index(node2) - encoding_table.index(node1))


def connect_nodes(nodes, links):
    # Initialize an empty dictionary for links
# links = {}

    # Loop over the nodes
    for i in range(len(nodes)):
        # If the node is not in the links dictionary, add it with an empty dictionary as value
        if nodes[i] not in links:
            links[nodes[i]] = {}
        
        # Add a link to only the next element 
        # print("adding link from ", nodes[i], " to ", nodes[(i+1)%len(nodes)], " with weight ", get_weight(nodes[i], nodes[(i+1)%len(nodes)]))
        links[nodes[i]][nodes[(i+1)%len(nodes)]] = get_weight(nodes[i], nodes[(i+1)%len(nodes)])
        # Add a link to only the previous element
        # print("adding link from ",nodes[(i+1)%len(nodes)], " to ", nodes[i], " with weight ", links[nodes[i]][nodes[(i+1)%len(nodes)]] )
        # new_value = links[nodes[i]][nodes[(i+1)%len(nodes)]]
        if nodes[(i+1)%len(nodes)] not in links:
            links[nodes[(i+1)%len(nodes)]] = {}
        links[nodes[(i+1)%len(nodes)]][nodes[i]] = links[nodes[i]][nodes[(i+1)%len(nodes)]]
    
    print("links after weight: ",links)

    #add the remaining nodes with wieght > 26
    iterator = 26
    for elt in nodes:
        iterator += 1
        for elt2 in nodes:
            if elt2 not in links[elt] and elt != elt2:
                links[elt][elt2] = iterator
                links[elt2][elt] = links[elt][elt2]
    
    print("links after covering tree: ",links)


def cipher(data):
    nodes = []
    # example of links = {a: {b: 1, c: 2}, b: {a: 1, c: 3}, c: {a: 2, b: 3}}
    links = {}
    for elt in data:
        nodes.append(elt)
    # print("nodes : ",nodes)
    connect_nodes(nodes, links)
    print("links : ",links)


def decipher(data):
    pass



# main code
data  = "code"
ciphered_data = cipher(data)
# print(ciphered_data)
# deciphered_data = decipher(ciphered_data)
# print(deciphered_data)


#tests

