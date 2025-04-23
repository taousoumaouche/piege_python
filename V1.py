import random
import doctest

def creer_grille():
    """
    Crée une grille de jeu 7x7 initialisée avec des trous (représentées par '1').
    
    Valeur de retour:
        list: La grille de jeu.
    
    Exemple:
    >>> grille = creer_grille()
    >>> len(grille)
    7
    >>> len(grille[0])
    7
    >>> grille[0][0]
    '1'
    """
    lst1 = []
    for i in range(7):
        lst2 = []
        for j in range(7):
            lst2.append("1")
        lst1.append(lst2)
    return lst1

def afficher_grille(grille):
    """
    Affiche la grille de jeu.
    
    Exemple:
    >>> grille = creer_grille()
    >>> afficher_grille(grille)
    1 1 1 1 1 1 1 
    1 1 1 1 1 1 1 
    1 1 1 1 1 1 1 
    1 1 1 1 1 1 1 
    1 1 1 1 1 1 1 
    1 1 1 1 1 1 1 
    1 1 1 1 1 1 1 
    """
    for ligne in grille:
        for case in ligne:
            print(case, end=" ")
        print()

def placer_bille(grille, ligne, colonne):
    """
    Place une bille ('0') à la position spécifiée dans la grille.
    Paramètres:
        grille (liste): La grille de jeu.
        ligne (int): L'indice de la ligne.
        colonne (int): L'indice de la colonne.
    Valeur de retour:
        list: La grille après le plaçement des billes.
    """
    grille[ligne][colonne] = '0'
    return grille

def trou():
    """
    Remplace certains éléments de la ligne par des trous ('True') de manière aléatoire
    si le nombre de trous existants est inférieur à 3. (Chaque ligne aura au moins 3 trous (True))
    
    Paramètres:
        Aucun
        
    Valeur de retour:
        list: Une ligne avec des trous (True) et des absences de trous (False).
    """
    ligne = [False] * 7
    while ligne.count(True) < 3:   #.count c'est le nombre de répétition d'un élément dans une liste
        for i in range(7):
            ligne[i] = random.choice([True, False])
    return ligne

def creer_tirette():
    """
    Crée une tirette avec des lignes contenant aléatoirement des trous ('True' représentant
    la présence d'un trou) et des absences de trous ('False').
    
    Valeur de retour:
        list: Une tirette composée de plusieurs lignes.
        
    """
    tirette = []
    for _ in range(7):
        tirette.append(trou())
    return tirette


def affichage(grille, tirette_horizontale, tirette_verticale):
    """
    Met à jour la grille en fonction des tirettes horizontales et verticales.
    Paramètres:
        grille (list): La grille de jeu.
        tirette_horizontale (list): La tirette horizontale.
        tirette_verticale (list): La tirette verticale.
    Valeur de retour:
        list: La grille mise à jour.

    """
    for i in range(7):
        for j in range(7):
            if grille[i][j] != '0':  # Ne mettre à jour que les positions vides
                if tirette_horizontale[i][j] and tirette_verticale[i][j]:
                    grille[i][j] = 'T' 
                elif tirette_horizontale[i][j] and not tirette_verticale[i][j]:
                    grille[i][j] = 'H'
                elif not tirette_horizontale[i][j] and tirette_verticale[i][j]:
                    grille[i][j] = 'V'
    return grille

def decal_gauche(tirette):
    """
    Décale la tirette vers la gauche.
    Paramètres:
        tirette (list): La tirette à décaler.
    Valeur de retour:
        list: La tirette mise à jour.
    Exemple:
    >>> decal_gauche([False, True, False, True, True, True, False])
    [True, False, True, True, True, False, False]
    """
    tirette = tirette.copy()
    tirette.append(tirette.pop(0))
    return tirette

def decal_droite(tirette):
    tirette = tirette.copy()
    tirette.insert(0, tirette.pop())
    return tirette
    """
    Décale la tirette vers la droite.
    Paramètres:
        tirette (list): La tirette à décaler.
    Valeur de retour:
        list: La tirette mise à jour.
    Exemple:
    >>> decal_droite([False, True, False, True, True, True, False])
    [False, False, True, True, True, False, True]
    """

def decal_haut(tirette, j):
    """
    Décale la colonne spécifiée de la tirette vers le haut.
    Paramètres:
        tirette (list): La tirette à décaler.
        j (int): L'indice de la colonne.
    Valeur de retour:
        list: La tirette mise à jour.
    """
    colonne = [tirette[i][j] for i in range(7)]
    x = colonne[0]
    colonne.pop(0)
    colonne.append(x)
    for i in range(7):
        tirette[i][j] = colonne[i]
    return tirette

def decal_bas(tirette, j):
    """
    Décale la colonne spécifiée de la tirette vers le bas.
    Paramètres:
        tirette (list): La tirette à décaler.
        j (int): L'indice de la colonne.
    Valeur de retour:
        list: La tirette mise à jour.
    """

    colonne = [tirette[i][j] for i in range(7)]
    x = colonne[6]  # Prendre le dernier élément
    colonne.pop(6)
    colonne.insert(0, x)  # Insérer à la première position
    for i in range(7):
        tirette[i][j] = colonne[i]
    return tirette

def tomber_bille(grille, tirette_horizontale, tirette_verticale, ligne, colonne):
    """
    Fait tomber une bille à la position spécifiée si les tirettes horizontale et verticale ont des trous.
    Paramètres:
        grille (list): La grille de jeu.
        tirette_horizontale (list): La tirette horizontale.
        tirette_verticale (list): La tirette verticale.
        ligne (int): L'indice de la ligne.
        colonne (int): L'indice de la colonne.
    Valeur de retour:
        tuple: La grille mise à jour et un indicateur indiquant si une bille est tombée.
    """
    a = False
    if grille[ligne][colonne] == '0':
        if tirette_horizontale[ligne][colonne] and tirette_verticale[ligne][colonne]:
            grille[ligne][colonne] = 'T'
            a = True
    return grille, a

def terminer_jeu(grille):
    """
    Vérifie si le jeu est terminé en vérifiant s'il reste des billes dans la grille.
    Paramètres:
        grille (list): La grille de jeu.
    Valeur de retour:
        bool: True si le jeu est terminé, sinon False.
    """

    for ligne in grille:
        for case in ligne:
            if case == '0':
                return False 
    return True
if __name__ == "__main__":
    doctest.testmod()
    grille = creer_grille()
    tirette_horizontale = creer_tirette()
    tirette_verticale = creer_tirette()
    affichage(grille, tirette_horizontale, tirette_verticale)
    afficher_grille(grille)

    billes_placees = 0

    while billes_placees < 5:
        position = input("Choisir la ligne et la colonne (séparées par un espace) : ")
        try:
            ligne, colonne = map(int, position.split())
        except ValueError:
            print("Position invalide.")
            continue

        if 0 <= ligne < len(grille) and 0 <= colonne < len(grille[0]):
            if grille[ligne][colonne] == 'T':
                print("Impossible de placer une bille dans un trou.")
            elif grille[ligne][colonne] in ('1', 'H', 'V'):
                placer_bille(grille, ligne, colonne)
                billes_placees += 1
            elif grille[ligne][colonne] == '0':
                print("La case est occupée. Veuillez choisir une case vide.")
        else:
            print("Position invalide. Veuillez choisir une position dans les limites de la grille.")

    print("5 billes ont été placées.")
    afficher_grille(grille)

    score = 0
    jouer = True

    while jouer:
        choix_tirette = input("Voulez-vous décaler la tirette horizontale ou verticale ? : ")

        while choix_tirette not in ['horizontale', 'verticale']:
            print("Choix invalide.")
            choix_tirette = input("Voulez-vous décaler la tirette horizontale ou verticale ? : ")

        while True:
            i = input("Choisir une tirette à décaler (0-6) ou entrer 'q' pour quitter : ")

            if i == 'q':
                break

            try:
                i = int(i)

                if 0 <= i < 7:
                    if choix_tirette == "verticale":
                        direction = input("Choisir la direction: h pour haut / b pour bas : ")

                        while direction not in ['h', 'b']:
                            print("Direction invalide.")
                            direction = input("Choisir la direction: h pour haut / b pour bas : ")

                        if direction == "b":
                            tirette_verticale = decal_bas(tirette_verticale, i)
                            affichage(grille, tirette_horizontale, tirette_verticale)
                            score += 1
                        elif direction == "h":
                            tirette_verticale = decal_haut(tirette_verticale, i)
                            affichage(grille, tirette_horizontale, tirette_verticale)
                            score += 1
                    elif choix_tirette == "horizontale":
                        direction = input("Choisir la direction: d pour droite / g pour gauche : ")

                        while direction not in ['d', 'g']:
                            print("Direction invalide.")
                            direction = input("Choisir la direction: d pour droite / g pour gauche : ")

                        if direction == "d":
                            tirette_horizontale[i] = decal_droite(tirette_horizontale[i])
                            affichage(grille, tirette_horizontale, tirette_verticale)
                            score += 1
                        elif direction == "g":
                            tirette_horizontale[i] = decal_gauche(tirette_horizontale[i])
                            affichage(grille, tirette_horizontale, tirette_verticale)
                            score += 1

                    break

                else:
                    print("Tirette invalide. Veuillez choisir un numéro entre 0 et 6.")
            except ValueError:
                print("Veuillez entrer un nombre entier valide.")

        tombe = False

        for h in range(len(grille)):
            for g in range(len(grille[h])):
                grille, a = tomber_bille(grille, tirette_horizontale, tirette_verticale, h, g)
                affichage(grille, tirette_horizontale, tirette_verticale)

                if a:
                    tombe = True

        if tombe:
            print("Il reste encore des billes sur la grille.")

        if terminer_jeu(grille):
            print("Félicitations ! Toutes les billes ont été retirées.")
            jouer = False
        grille =  affichage(grille, tirette_horizontale, tirette_verticale)  
        afficher_grille(grille)

    print("Tu as gagné avec", score, "coups!")

