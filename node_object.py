#create a class nodes with the next nodes and the weight

class Node:
    def __init__(self, id, char):
        self.id = id
        self.char = char
        # ex neighbors = {Node1: 1, Node2: 4}
        self.neighbors = {}

    def add_neighbor(self, neighbor, weight):
        self.neighbors[neighbor] = weight
        
    def __str__(self):
        # Convertir le dictionnaire en une chaîne de caractères lisible
        neighbors_str = ", ".join([f"{neighbor.char}: {weight}" for neighbor, weight in self.neighbors.items()])
        return f"Node {self.id} ({self.char}) neighbors: {{{neighbors_str}}}"
