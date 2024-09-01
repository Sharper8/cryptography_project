# Cryptography project

In this project, we will implement an encryption and 
deciphering using graph theory, and more specifically the concept of 
of a covering tree.
This algorithm is a symmetric key algorithm. It is based on the idea of finding 
a minimum weight covering tree (using Prim)


# Questions : 

Implement the algorithm in Python in a way that can be encrypted and decrypted any sentence, once we are put d’accord to l’ advance on the private key matrix.
=> the private key varies depending on the size of the message, the message is correctly encrypted and decrypted

Explain why a minimum weight covering tree is used here.
=> The covering tree of minimum weight is used to find the meaning of the characters of the message works in numbers. 

- Explain why, using the X1 matrix that is sent, an attacker cannot make the message easy. That is, although X2 and X1 are close, why do we need X2 and why X1 is not enough.
=> In X1, it lacks information of order of columns. One could know the direction of the graph or its shape by calculating the STM of X1, but one needs the order to know or start the head and which loom is placed or in the final word (diagonal of X2)
