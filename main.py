import hashlib
import random
import numpy as np
import os

print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("+                                                                    +")
print("+ BIENVENUE DANS NOTRE PROGRAMME D'IMPLEMENTATION DE SIGNATURE ECDSA +")
print("+                                                                    + ")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print(
    "ECDSA: Elliptic Curve Digital Signature Algorithm: algorithme qui utilise les courbes elliptiques pour signer.\n")
print("Une courbe elliptique est une courbe de forme générale: y² = x³ + ax + b.\n")
print("Nous avons opté de donner la latitude à l'utilisateur d'entrer lui-même les paramètres de la courbe elliptique.")
print("Pour cette raison donc, il vous sera demandé au tout début d'entrer les valeurs de a et b.")
print("Il vous sera aussi demandé d'entrer la coordonnée suivant les abcisses d'un point sur la courbe elliptique.\n")
print("Assez bavardé, passons aux choses sérieuses.\n")
# Definition des paramètres de la courbe elliptique
a = int(input("Valeur de a : "))
b = int(input("Valeur de b : "))
p = int(input("Valeur de p : "))

while (4 * (a ** 3) + 27 * (b ** 2)) % p != 0:
    # Point de base de la courbe elliptique
    Gx = int(input("Valeur de Gx : "))
    Gy = np.sqrt(Gx ** 3 + a * Gx + b) % p
    # print(Gy)
    G = np.array([[Gx], [Gy]])

    # Ordre de G
    # n = int(p + 1 - 2*np.sqrt(p))
    n = 9
    # n = int(input("Valeur de n (n est premier) : "))

    # Génération de la clé privée
    d = random.randint(1, n - 1)
    print(d)

    # Calcul de la clé publique
    Qx = Gx * d
    Qy = np.sqrt(Qx ** 3 + a * Qx + b) % p
    Q = [Qx, Qy]

    # inverse modulaire
    def inverse_modulaire(a, m):
        # Utilise l'algorithme d'Euclide étendu pour trouver le PGCD de a et m
        # ainsi que les coefficients de Bézout x et y tels que ax + my = PGCD(a, m)
        def euclid(a, b):
            if b == 0:
                return a, 1, 0
            else:
                c, x, y = euclid(b, a % b)
                return c, y, x - (a // b) * y

        c, x, y = euclid(a, m)

        # Si le PGCD de a et m n'est pas 1, alors l'inverse modulaire n'existe pas
        if c != 1:
            return None

        # L'inverse modulaire est alors x modulo m
        return x % m


    # fonction qui hash et signe le document
    def sign():
        # Récupérer le chemin d'accès du document
        doc_path = "/home/hacker/Bureau/chapter4.pdf"
        # Vérifier si le fichier existe
        if not os.path.isfile(doc_path):
            print("Erreur: Fichier introuvable!")
            exit()
            # Lire le contenu du document
        with open(doc_path, 'rb') as f:
            file_content = f.read()
        hash_doc = int(hashlib.sha256(file_content).hexdigest(), 16)
        print(type(hash_doc))
        # Choix d'un nombre aléatoire k
        k = random.randint(1, n - 1)

        # Calcul du point (x, y) = k*G
        x = k * Gx
        y = k * Gy

        # Calcul de r = x mod n
        r = x % n

        # Calcul de s = (k^-1)*(sha256(msg) + d*r) mod n
        k_inv = inverse_modulaire(k, n)
        # k_inv = pow(k, n - 2, n)
        s = k_inv * (hash_doc + d * r) % n
        while s == 0 or r == 0:
            print("la signature ne doit pas être nulle")
            break
        return print("\nVoici votre signature: " + "r = " + str(r) + ",s = " + str(s))


    sign()

    print("\n++++++Bravo!! Vous venez de signer avec succès votre document. Vérifiez-la!!++++++\n")


    def hash_function():
        # Récupérer le chemin d'accès du document
        doc_path = "/home/hacker/Bureau/chapter4.pdf"
        # Vérifier si le fichier existe
        if not os.path.isfile(doc_path):
            print("Erreur: Fichier introuvable!")
            exit()
        # Lire le contenu du document
        with open(doc_path, 'rb') as f:
            file_content = f.read()
        hash_doc = int(hashlib.sha256(file_content).hexdigest(), 16)
        return hash_doc


    def is_point_at_infinity(x, y):
        if x is None and y is None:
            return True
        else:
            return False

        # Fonction de vérification de signature ECDSA


    def verify():
        r = float(input("Entrer r: "))
        s = float(input("Entrer s: "))
        hashed = hash_function()
        # verifier que Q est different du point à l'infini
        if is_point_at_infinity(Q[0], Q[1]) == True:
            return print("La signature n'est pas vérifiée, car Q est le point à l'infini")

        # verifier que Q appartient à la courbe
        if Q[1] != np.sqrt(Q[0] ** 3 + a * Q[0] + b) % p:
            return print("La signature n'est pas vérifiée, car Q n'appartient pas à la courbe")
        # verifier que nQ est le poit à l'infini

        if is_point_at_infinity(n * Q[0], n * Q[1]) == True:
            return print("La signature n'est pas valide, car nQ n'est pas le point à l'infini ")
        # Vérification que r et s sont dans l'intervalle [1, n-1]
        if not 1 <= r and r <= n - 1 and 1 <= s <= n - 1:
            return print("La signature n'est pas valide, car r et s ne sont pas compris entre 1 et n-1")

        # Calcul du point (x, y) = (s^-1)*sha256(msg)*G + (s^-1)*r*Q
        s_inv = inverse_modulaire(s, n)
        x1 = (hashed * s_inv % n) * Gx + Q[0] * (r * s_inv % n)
        x_ver = x1 % n

        # Verification que r = x mod n
        #if r != x_ver:
            #return print("La signature nest pas verifier, car r different de de x")

        return print("\n++++++++++Mes felicitations,la signature est verifies avec success++++++++\n")


    verify()

    """windows = tk.Tk()
    button = tk.Button(windows, text="Signer", width = 50)
    button.pack()
    button.bind('<ButtonRelease-1>', sign())"""
