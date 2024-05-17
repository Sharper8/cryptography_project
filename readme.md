This is the readme of the cryptography project

# In this project, we will implement an encryption and 
# deciphering using graph theory, and more specifically the concept of 
# of a covering tree.
# This algorithm is a symmetric key algorithm. It is based on the idea of finding 
# a minimum weight covering tree (using Kruskal or Prim)

questions : 

• Implémenter l’algorithme en Python de manière à pouvoir chiffrer et déchiffrer 
n’importe quelle phrase, une fois que nous nous sommes mis d’accord à l’avance 
sur la matrice clé privée.
• Expliquer pourquoi on utilise un arbre couvrant de poids minimal ici.
• Expliquer pourquoi, en utilisant la matrice X1 qui est envoyée publiquement, un 
attaquant ne peut pas déchiffrer le message facilement. C’est-à-dire, bien que 
X2 ​et X1 soient très proches, pourquoi avons-nous besoin de X2 pour déchiffrer 
et pourquoi X1 ne suffit pas.


TODO :

- changer la tete de l'arbre par d'autre charactère ? 
- faire l'algo pour le shortest path au lieu de prendre tout le temps le même ordre que le mot46
- mots avec deux fois la meme lettre qui se suit = singular matrix ?
