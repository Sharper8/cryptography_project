# Cryptography project

In this project, we will implement an encryption and 
deciphering using graph theory, and more specifically the concept of 
of a covering tree.
This algorithm is a symmetric key algorithm. It is based on the idea of finding 
a minimum weight covering tree (using Prim)


Questions : 

• Implémenter l’algorithme en Python de manière à pouvoir chiffrer et déchiffrer 
n’importe quelle phrase, une fois que nous nous sommes mis d’accord à l’avance 
sur la matrice clé privée.
=> la clé privée varie en fonction de la taille du message, le message est correctement chiffré et déchiffré

• Expliquer pourquoi on utilise un arbre couvrant de poids minimal ici.
=> L'arbre couvrant de poids minimal sert à retrouver le sens des charactères du message traduits en nombres. 

• Expliquer pourquoi, en utilisant la matrice X1 qui est envoyée publiquement, un 
attaquant ne peut pas déchiffrer le message facilement. C’est-à-dire, bien que 
X2 ​et X1 soient très proches, pourquoi avons-nous besoin de X2 pour déchiffrer 
et pourquoi X1 ne suffit pas.
=> Dans X1, il manque l'information de l'ordre des colonnes. On pourrait connaitre le sens du graphe ou sa forme en calculant le MST de X1, mais on a besoin de l'ordre pour savoir ou commence la tête et quel caractère est placé ou dans le mot final (diagonale de X2)