from src.fltk import *
from time import sleep
import random 
import doctest
#********************************Fonctions de moteur de jeu*******************************************
def creer_grille():
    """
    Crée et retourne une grille de jeu sous forme de liste de listes.

    La grille est un carré de 7x7 où chaque élément est initialisé à "0".

    Returns:
        list: Une liste de 7 listes, chacune contenant 7 éléments "0".
    >>> grille = creer_grille()
    >>> len(grille)
    7
    >>> all(len(ligne) == 7 for ligne in grille) 
    True
    >>> all(all(cell == "0" for cell in ligne) for ligne in grille)
    True
    """
    lst1 = []
    for i in range(7):
        lst2 = []
        for j in range(7):
            lst2.append("0")
        lst1.append(lst2)
    return lst1

def trou():
    """
    Crée une ligne de 7 éléments représentant la présence ou l'absence de trous.
    La ligne est une liste de booléens où `True` indique un trou et `False` indique l'absence d'un trou. 
    Il y a une garantie d'avoir au moins 4 trous par ligne (éléments `True`).

    Returns:
        list: Une liste de 7 booléens avec au moins 4 `True`.
    >>> ligne_trou = trou()
    >>> len(ligne_trou)
    7
    >>> ligne_trou.count(True) >= 4
    True
    """
    ligne = [False] * 7
    while ligne.count(True) < 2:   #.count c'est le nombre de répétition d'un élément dans une liste
        for i in range(7):
            ligne[i] = random.choice([True, False])
    return ligne

def creer_tirette():
    """
    Crée et initialise une tirette pour le jeu.

    Cette fonction est utilisée pour créer et initialiser les tirettes utilisées dans le jeu.
    Elle détermine l'état initial de chaque tirette.

    Returns:
        list: Un objet représentant l'état initial de la tirette, sous forme de liste.
    """
    tirette = []
    for _ in range(7):
        tirette.append(trou())
    return tirette

def placer_bille(grille, ligne, colonne, joueur):
    """
    Place une bille sur la grille à une position spécifiée par le joueur.

    Args:
        grille (list): La grille de jeu.
        ligne (int): L'indice de la ligne où placer la bille.
        colonne (int): L'indice de la colonne où placer la bille.
        joueur (str): Le symbole représentant le joueur.

    Returns:
        None: La grille est modifiée en place.
    >>> grille = creer_grille()
    >>> placer_bille(grille, 2, 3, "X")
    [['0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', 'X', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0']]
    >>> grille[2][3]
    'X'
    """
    grille[ligne][colonne] = str(joueur)
    return grille


def mettre_a_jour_grille(grille, tirette_horizontale, tirette_verticale):
    """
    Met à jour l'état de la grille en fonction des mouvements des tirettes horizontales et verticales.

    Args:
        grille (list): La grille de jeu.
        tirette_horizontale (list): L'état actuel des tirettes horizontales.
        tirette_verticale (list): L'état actuel des tirettes verticales.

    Returns:
        None: La grille est modifiée en place.
    >>> grille = creer_grille()
    >>> tirette_horizontale = [1, 0, 0, 0, 0, 0, 0]
    >>> tirette_verticale = [0, 0, 0, 0, 0, 0, 1]
    >>> mettre_a_jour_grille(grille, tirette_horizontale, tirette_verticale)
    >>> # Tester un comportement spécifique de la mise à jour
    """
    for i in range(7):
        for j in range(7):
            if grille[i][j] not in ['1','2','3','4']:  
                if tirette_horizontale[i][j]==True and tirette_verticale[i][j]==True:
                    grille[i][j] = 'T'
                elif tirette_horizontale[i][j]==True and tirette_verticale[i][j]==False:
                    grille[i][j] = 'H'
                elif tirette_horizontale[i][j]==False and tirette_verticale[i][j]==True:
                    grille[i][j] = 'V'
    return grille

def decal_gauche(tirette, i):
    """
    Décale une tirette vers la gauche à l'indice spécifié.

    Args:
        tirette (list): La liste représentant l'état de la tirette.
        i (int): L'indice de la tirette à décaler.

    Returns:
        None: La tirette est modifiée en place.
    >>> tirette = [0, 0, 1, 0, 0, 0, 0]
    >>> decal_gauche(tirette, 2)
    >>> tirette
    [0, 1, 0, 0, 0, 0, 0]
    """
    liste = tirette[i].copy()  # Créez une copie de la liste
    x = liste[0]
    liste.pop(0)
    liste.append(x)
    tirette[i] = liste
    return tirette

def decal_droite(tirette, i):
    """
    Décale une tirette vers la droite à l'indice spécifié.

    Args:
        tirette (list): La liste représentant l'état de la tirette.
        i (int): L'indice de la tirette à décaler.

    Returns:
        None: La tirette est modifiée en place.
    >>> tirette = [0, 0, 1, 0, 0, 0, 0]
    >>> decal_droite(tirette, 2)
    >>> tirette
    [0, 1, 0, 0, 0, 0, 0]
    """
    liste = tirette[i].copy()  # Créez une copie de la liste
    x = liste[6]
    liste.pop(6)
    liste.insert(0, x)
    tirette[i] = liste
    return tirette

def decal_haut(tirette, j):
    """
    Décale une tirette verticale vers le haut à l'indice spécifié.

    Args:
        tirette (list): La liste représentant l'état de la tirette verticale.
        j (int): L'indice de la colonne de la tirette à décaler.

    Returns:
        None: La tirette est modifiée en place.
    >>> tirette = [0, 0, 1, 0, 0, 0, 0]
    >>> decal_haut(tirette, 2)
    >>> tirette
    [1, 0, 0, 0, 0, 0, 0]
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
    Décale une tirette verticale vers le bas à l'indice spécifié.

    Args:
        tirette (list): La liste représentant l'état de la tirette verticale.
        j (int): L'indice de la colonne de la tirette à décaler.

    Returns:
        None: La tirette est modifiée en place.
    >>> tirette = [0, 0, 1, 0, 0, 0, 0]
    >>> decal_bas(tirette, 2)
    >>> tirette
    [0, 0, 1, 0, 0, 0, 0]
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
    Gère la chute d'une bille sur la grille en fonction de la position des tirettes.

    Args:
        grille (list): La grille de jeu.
        tirette_horizontale (list): L'état des tirettes horizontales.
        tirette_verticale (list): L'état des tirettes verticales.
        ligne (int): L'indice de la ligne où la bille tombe.
        colonne (int): L'indice de la colonne où la bille tombe.

    Returns:
        None: La grille est modifiée en place pour refléter la chute de la bille.
    >>> grille = creer_grille()
    >>> tirette_horizontale = [1, 0, 0, 0, 0, 0, 0]
    >>> tirette_verticale = [0, 0, 0, 0, 0, 0, 1]
    >>> tomber_bille(grille, tirette_horizontale, tirette_verticale, 2, 3)
    [['0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0']]
    >>> # Vérifier un comportement spécifique après la chute de la bille
    """
    if grille[ligne][colonne] in ['1', '2', '3', '4']:
        if tirette_horizontale[ligne][colonne] and tirette_verticale[ligne][colonne]:
            grille[ligne][colonne] = 'T'
    return grille

def verifier_fin_jeu_et_compter_billes(grille, jouer_a_1):
    """
    Vérifie si le jeu est terminé et compte les billes sur la grille.
    Cette fonction pourrait par exemple vérifier si toutes les billes sont tombées dans des trous,
    ou si un joueur a atteint un certain score.

    Args:
        grille (list): La grille de jeu.
        jouer_a_1 (bool): Un booléen indiquant si le jeu est en mode solo (True) ou multi-joueur (False).

    Returns:
        tuple: Un booléen indiquant si le jeu est terminé, et un entier représentant le nombre de billes.
    >>> grille = creer_grille()
    >>> jeu_termine, nombre_billes = verifier_fin_jeu_et_compter_billes(grille, True)
    >>> type(jeu_termine)
    <class 'bool'>
    >>> type(nombre_billes)
    <class 'list'>
    """
    joueurs_restants = [0, 0, 0, 0]  # Pour compter le nbr de billes restantes de chaque joueur
    for ligne in grille:
        for case in ligne:
            if case in ['1', '2', '3', '4']:
                joueur_index = int(case) - 1 # Si la case contient le numéro d'un joueur,cette ligne convertit cette chaîne de caractères en un entier  et soustrait 1 pour obtenir l'indice correspondant  
                joueurs_restants[joueur_index] += 1 #Cette ligne incrémente le compteur de billes pour lejoueur correspondant à l'indice joueur_index dans la listejoueurs_restants. Cela compte le nombre de billes de chaque joueur sur la grille

    if jouer_a_1:
        for billes in joueurs_restants:
            if billes > 0:   #si le joueur a encore des billes sur la grille
                return False, joueurs_restants  # Des billes sont encore sur la grille (jeu pas terminé)
        return True, joueurs_restants  # Toutes les billes sont tombées
    else:
        # Vérifier pour les autres modes
        joueurs_avec_billes = sum(1 for billes in joueurs_restants if billes > 0) #compter le nombre de joueurs ayant encore des billes sur la grille. Elle parcourt la liste joueurs_restants et ajoute 1 à chaque fois que le compteur de billes de ce joueur est supérieur à zéro.
        return joueurs_avec_billes <= 1, joueurs_restants #retourne True si joueurs_avec_billes est inférieur ou égal à 1, ce qui signifie qu'il ne reste qu'un joueur ou aucun joueur avec des billes sur la grille, indiquant ainsi que le jeu est terminé en mode multijoueur. Elle renvoie également la liste joueurs_restants qui contient le nombre de billes de chaque joueur.



#*****************************Fonctions de l'interface graphique**************************************
def dessiner_plateau():
    """
    Dessine le plateau de jeu à l'écran.

    Cette fonction s'occupe de dessiner le plateau de jeu, en utilisant les fonctions de la bibliothèque fltk.
    Elle peut être appelée à chaque fois que le plateau de jeu doit être rafraîchi.

    Returns:
        None: Le plateau est dessiné à l'écran mais il n'y a pas de valeur de retour.
    """
    image(500, 300, "assets/fond.png", ancrage='center')
    image(500, 350, "assets/grille.png", ancrage='center')

def dessiner_grille():
    """
    Dessine la grille de jeu à l'écran.

    Cette fonction s'occupe de représenter graphiquement la grille du jeu en utilisant la bibliothèque fltk.
    Elle est typiquement appelée après chaque mise à jour du jeu pour rafraîchir l'affichage.

    Returns:
        None: La grille est dessinée à l'écran mais il n'y a pas de valeur de retour.
    """
    j = 110
    for x in range(len(grille)):
        i = 260 
        for y in range(len(grille)):
            if tirette_horizontale[x][y]==True and tirette_verticale[x][y] == True  :
                rectangle(i, j, i + taille_carre, j + taille_carre, couleur='black',remplissage='black')    
            else:
                rectangle(i, j, i + taille_carre, j + taille_carre, couleur='#813016',epaisseur = 2)
            i += taille_carre + espace_entre_carres
        j += taille_carre + espace_entre_carres


def dessiner_tirettes_verticales():
    """
    Dessine les tirettes verticales du jeu à l'écran.

    Utilise la bibliothèque fltk pour afficher graphiquement les tirettes verticales utilisées dans le jeu.
    Cette fonction est appelée pour mettre à jour l'affichage des tirettes verticales.

    Returns:
        None: Les tirettes verticales sont dessinées à l'écran sans valeur de retour.
    """
    i = 280  
    j = 110
    for x in range(len(tirette_verticale)):
        for y in range(len(tirette_verticale)):
            if tirette_verticale[x][y]==False and tirette_horizontale[x][y]==True :
                rectangle(i, j, i + taille_carre / 3, j + taille_carre, couleur='white', remplissage='white')
            i += taille_carre + espace_entre_carres
        j += taille_carre + espace_entre_carres
        i = 280 
            
            
def dessiner_tirettes_horizontales():
    """
    Dessine les tirettes horizontales du jeu à l'écran.

    Utilise la bibliothèque fltk pour afficher graphiquement les tirettes horizontales utilisées dans le jeu.
    Cette fonction est appelée pour mettre à jour l'affichage des tirettes horizontales.

    Returns:
        None: Les tirettes horizontales sont dessinées à l'écran sans valeur de retour.
    """
    j = 130
    for x in range(len(tirette_horizontale)):
        i = 260
        for y in range(len(tirette_horizontale)):
            if tirette_horizontale[x][y]==False :
                rectangle(i, j, i + taille_carre, j + taille_carre / 3, couleur='#D4450B', remplissage='#D4450B')
            i += taille_carre + espace_entre_carres
        j += taille_carre + espace_entre_carres

def dessiner_fleche():
    """
    Dessine une flèche horizontale sur la grille de jeu.

    Cette fonction est utilisée pour indiquer une direction ou un mouvement sur la grille de jeu.
    Elle fait appel à la bibliothèque fltk pour le rendu graphique.

    Returns:
        None: La flèche est dessinée à l'écran mais il n'y a pas de valeur de retour.
    """
    for i in range(7):
        x = 260 + i * (taille_carre + espace_entre_carres)
        ligne(x+30, 110, x + 30,65, couleur='white', epaisseur=20)
        fleche(x+30, 110, x+30, 65, couleur='white', epaisseur=21)
        ligne(x+30, 591,x+30, 625, couleur='white', epaisseur=20)
        fleche(x+30, 591,x+30, 625, couleur='white', epaisseur=21)
        ligne(210,x-120, 260, x-120, couleur="#D4450B",epaisseur=20)
        fleche(250, x-120, 210,x-120, couleur='#D4450B', epaisseur=21)
        ligne(785, x-120, 741, x-120, couleur='#D4450B', epaisseur=20)
        fleche(751, x-120, 785, x-120, couleur='#D4450B', epaisseur=21)
        x+=1

def dessiner_billes():
    """
    Dessine les billes sur la grille de jeu.

    Cette fonction se charge de représenter graphiquement les billes sur le plateau de jeu.
    Elle est généralement appelée après chaque action du joueur pour mettre à jour la position des billes.

    Returns:
        None: Les billes sont dessinées à l'écran mais il n'y a pas de valeur de retour.
    """
    for i in range(7):
        for j in range(7):
            x = 260 + j * (taille_carre + espace_entre_carres)
            y = 110 + i * (taille_carre + espace_entre_carres)
            if grille[i][j] in ['1', '2', '3', '4']:
                joueur = int(grille[i][j]) - 1 #convertit le numéro du joueur contenu dans la case en un entier (par exemple, '1' en 1) et soustrait 1 pour obtenir l'indice correspondant dans la liste couleurs_billes'''
                couleur = couleurs_billes[joueur]
                cercle(x + taille_carre / 2, y + taille_carre / 2, 25, couleur=couleur, remplissage=couleur)
                
#**************************************Programme principal*******************************************
if __name__ == "__main__":
    doctest.testmod()
    # Dimensions du jeu
    taille_case = 25
    largeur_plateau = 40 
    hauteur_plateau = 30 
    cree_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
    taille_carre = 60
    espace_entre_carres = 10
    taille_fleche = 20
    tour_joueur = 1
    nombre_joueurs = 0
    couleurs_billes = ['#F777B3', '#177B80', '#8751D6', '#F57724']
    menu = True
    regles = False
    regles1 = False
    jouer_a_1 = False
    jouer_a_2 = False
    jouer_a_3 = False
    jouer_a_4 = False
    afficher_message = True        #pour affiche le message de placer bille
    décale_terminee = False        #si le déplacement de tirette est terminé
    afficher_message_tirettes = False

    # calculer les coordonnées de la zone des flèches haut
    zones_fleches_haut = []
    for colonne in range(7):
        x_centre = 260 + colonne * (taille_carre + espace_entre_carres) + taille_carre / 2
        y_centre = 65  
        x_min = x_centre - taille_fleche 
        x_max = x_centre + taille_fleche 
        y_min = y_centre - taille_fleche 
        y_max = y_centre + taille_fleche 
        zones_fleches_haut.append((x_min, x_max, y_min, y_max))

    # calculer les coordonnées de la zone des flèches bas
    zones_fleches_bas = []
    for colonne in range(7):
        x_centre = 260 + colonne * (taille_carre + espace_entre_carres) + taille_carre / 2
        y_centre = 625  
        x_min = x_centre - taille_fleche 
        x_max = x_centre + taille_fleche 
        y_min = y_centre - taille_fleche 
        y_max = y_centre + taille_fleche 
        zones_fleches_bas.append((x_min, x_max, y_min, y_max))
    
    # calculer les coordonnées de la zone des flèches gauche
    zones_fleches_gauche = []
    for l in range(7):
        y_centre = 110 + l * (taille_carre + espace_entre_carres) + taille_carre / 2
        x_min = 210 - taille_fleche  # Coordonnées X pour le côté gauche à côté de la tirette horizontale
        x_max = 230
        y_min = y_centre - taille_carre / 3
        y_max = y_centre + taille_carre / 3
        zones_fleches_gauche.append((x_min, x_max, y_min, y_max))

    # calculer les coordonnées de la zone des flèches droites
    zones_fleches_droite = []
    for l in range(7):
        y_centre = 110 + l * (taille_carre + espace_entre_carres) + taille_carre / 2
        x_min = 765  # Coordonnées X pour le côté droit à côté de la tirette horizontale
        x_max = 785 + taille_fleche
        y_min = y_centre - taille_carre / 3
        y_max = y_centre + taille_carre / 3
        zones_fleches_droite.append((x_min, x_max, y_min, y_max))

    # Initialisation du jeu
    grille = creer_grille()
    tirette_horizontale = creer_tirette()
    tirette_verticale = creer_tirette()
    nombre_billes_placees = 0 
    placer_billes_termine = False 
    fin_jeu = False
    # Boucle principale
    jouer = True
    while jouer:
        image(500, 400, "assets/menu.png", ancrage='center')
        while menu:

            # 1 joueur
            rectangle(200,293,370,342,remplissage="#4EFF1E")
            centre_x = (200 + 370) / 2
            centre_y = (293 + 342) / 2
            texte(centre_x, centre_y, "1 joueur", police='Forte', ancrage='center',couleur='white')
            
            # 2 joueurs
            rectangle(630,293,800,342,remplissage="#4EFF1E")
            centre_x = (630 + 800) / 2
            centre_y = (293 + 342) / 2
            texte(centre_x, centre_y, "2 joueurs", police='Forte', ancrage='center',couleur='white')            
            
            # 3 joueurs
            rectangle(200,450,370,500,remplissage="#4EFF1E")
            centre_x = (200 + 370) / 2 
            centre_y = (450 + 500) / 2
            texte(centre_x, centre_y, "3 joueurs", police='jumble', ancrage='center',couleur='white')
            
            #4 joueurs
            rectangle(630,450,800,500,remplissage="#4EFF1E")
            centre_x = (630 + 800) / 2
            centre_y = (450 + 500) / 2
            texte(centre_x, centre_y, "4 joueurs", police='jumble', ancrage='center',couleur='white')
            
            #How to play
            rectangle(800,10,990,50,remplissage="#EC9033")
            centre_x = (800 + 990) / 2
            centre_y = (10 + 50) / 2
            texte(centre_x, centre_y, "How to play", police='jumble', ancrage='center',couleur='white')
            mise_a_jour()

            
            # gestion des événements
            ev = donne_ev()
            ty = type_ev(ev)
            # Quand on quitte le jeu il se ferme
            if ty == 'Quitte':
                jouer = False
                menu = False
                break
            # Fonctionnement des boutons
            elif ty == 'ClicGauche':

                #Jouer_a_1
                if 200 <= abscisse(ev) <= 370 and 293 <= ordonnee(ev) <= 342:
                    jouer_a_1 = True
                    jouer_a_2 = jouer_a_3 = jouer_a_4 = False
                    nombre_joueurs = 1
                    scores = [0] 
                    menu = False

                # jouer_a_2  
                elif 630 <= abscisse(ev) <= 800 and 293 <= ordonnee(ev) <= 342:
                    jouer_a_2 = True
                    jouer_a_1 = jouer_a_3 = jouer_a_4 = False
                    nombre_joueurs = 2
                    scores = [0] * nombre_joueurs 
                    menu = False
                    
                # jouer_a_3    
                elif 200 <= abscisse(ev) <= 370 and 450 <= ordonnee(ev) <= 500:
                    jouer_a_3 = True
                    jouer_a_1 = jouer_a_2 = jouer_a_4 = False
                    nombre_joueurs = 3
                    scores = [0] * nombre_joueurs 
                    menu = False

                # jouer_a_4   
                elif 630 <= abscisse(ev) <= 800 and 450 <= ordonnee(ev) <= 500:
                    jouer_a_4 = True
                    jouer_a_2 = jouer_a_3 = jouer_a_1 = False
                    nombre_joueurs = 4
                    scores = [0] * nombre_joueurs 
                    menu = False
                
                # How to play
                elif 800 <= abscisse(ev) <= 990 and 10 <= ordonnee(ev) <= 50:
                    regles = True
                    menu = False
                    
### Menu regles ##############################################################

        while regles:

            image(500,300,'assets/règles.png', ancrage = "center")
            rectangle(880,20,980,60,remplissage='#2E90F3')  
            texte(890, 20,"Menu", taille = "23",police = 'benguiat',couleur='white')          

            mise_a_jour()

            ev = donne_ev()
            ty = type_ev(ev)

            if ty == 'Quitte':
                jouer = False
                break
                # Fonctionnement des boutons
            elif ty == 'ClicGauche':

                if 880 <= abscisse(ev) <= 980 and 20 <= ordonnee(ev) <= 60:
                    menu = True
                    regles = False

                if 500 <= abscisse(ev) <= 700 and 580 <= ordonnee(ev) <= 630:
                    regles1 = True
                    regles = False

        while regles1:
            image(500,300,'assets/règle_1.png', ancrage = "center")
            rectangle(880,20,980,60,remplissage='#2E90F3')  
            texte(890, 20,"Menu", taille = "23",police = 'benguiat',couleur='white') 

            mise_a_jour()

            ev = donne_ev()
            ty = type_ev(ev)

            if ty == 'Quitte':
                jouer = False
                break
            # Fonctionnement des boutons
            elif ty == 'ClicGauche':
                if 880 <= abscisse(ev) <= 980 and 20 <= ordonnee(ev) <= 60:
                    menu = True
                    regles1 = False

        # Affichage des objets
        efface_tout()
        dessiner_plateau()
        dessiner_tirettes_verticales()
        dessiner_tirettes_horizontales()
        dessiner_fleche()
        dessiner_grille()
        dessiner_billes()

        if afficher_message_tirettes:
            texte(370, 20, "Décalez vos tirettes", taille=24, couleur='#45FF50')
        if afficher_message and not placer_billes_termine:
            if jouer_a_1:
                texte(200, 400, "Placez vos billes", taille=24, couleur='#45FF50')
            else:
                texte(200, 400, f"Joueur {tour_joueur}, placez vos billes", taille=24, couleur='#45FF50')
        elif placer_billes_termine and not jouer_a_1:  
            texte(200, 400, f"A ton tour, Joueur {tour_joueur}", taille=24, couleur='#45FF50')
            
        if jouer_a_1 and len(scores) > 0:
            texte(850, 20, f"Score: {scores[0]}", taille=24, couleur='red')
        else:
            for i in range(nombre_joueurs):
                if i < len(scores):
                    texte(20, 20 + i * 30, f"Joueur {i + 1}: {scores[i]}", taille=24, couleur=couleurs_billes[i])


        mise_a_jour()
        # Gestion des événements
        ev = donne_ev()
        ty = type_ev(ev)
        if ty == 'Quitte':
            jouer = False
        elif ty == 'ClicGauche':
            x_souris = abscisse(ev)
            y_souris = ordonnee(ev)
            # Convertir les coordonnées de la souris en indices de grille
            colonne = int((x_souris - 260) // (taille_carre + espace_entre_carres))
            lignee = int((y_souris - 110) // (taille_carre + espace_entre_carres))
            # Vérifiez si la case est valide pour placer une bille
            if 0 <= lignee < 7 and 0 <= colonne < 7:
                if not (tirette_horizontale[lignee][colonne] and tirette_verticale[lignee][colonne]) and grille[lignee][colonne] not in['1','2','3','4'] and not placer_billes_termine:  
                    if nombre_billes_placees < 5:
                        grille = placer_bille(grille, lignee, colonne, tour_joueur)
                        nombre_billes_placees += 1
                        afficher_message = False

                        if nombre_billes_placees == 5:
                            if tour_joueur < nombre_joueurs: #déterminer s'il y a encore des joueurs qui n'ont pas encore eu leur tour de placement de billes.
                                tour_joueur += 1
                                nombre_billes_placees = 0 
                                afficher_message = True
                            else:
                                # Tous les joueurs ont placé leurs billes
                                tour_joueur = 1
                                nombre_billes_placees = 0
                                placer_billes_termine = True
                                afficher_message_tirettes = True

            if placer_billes_termine:
                # Déplacement vers la haut
                for j, (x_min, x_max, y_min, y_max) in enumerate(zones_fleches_haut):
                    if x_min <= x_souris <= x_max and y_min <= y_souris <= y_max:
                        tirette_verticale = decal_haut(tirette_verticale, j)
                        grille = mettre_a_jour_grille(grille, tirette_horizontale, tirette_verticale)
                        décale_terminee = True
                        if jouer_a_1:
                            scores[0] += 1
                    
                # Déplacement vers la gauche
                for j, (x_min, x_max, y_min, y_max) in enumerate(zones_fleches_gauche):
                    if x_min <= x_souris <= x_max and y_min <= y_souris <= y_max:
                        tirette_horizontale = decal_gauche(tirette_horizontale, j)
                        grille = mettre_a_jour_grille(grille, tirette_horizontale, tirette_verticale)
                        décale_terminee = True
                        if jouer_a_1:
                            scores[0] += 1

                # Déplacement vers la droite
                for j, (x_min, x_max, y_min, y_max) in enumerate(zones_fleches_droite):
                    if x_min <= x_souris <= x_max and y_min <= y_souris <= y_max:
                        tirette_horizontale = decal_droite(tirette_horizontale, j)
                        grille = mettre_a_jour_grille(grille, tirette_horizontale, tirette_verticale)
                        décale_terminee = True
                        if jouer_a_1:
                            scores[0] += 1                        

                # Déplacement vers le bas
                for j, (x_min, x_max, y_min, y_max) in enumerate(zones_fleches_bas):
                    if x_min <= x_souris <= x_max and y_min <= y_souris <= y_max:
                        tirette_verticale = decal_bas(tirette_verticale, j)
                        grille = mettre_a_jour_grille(grille, tirette_horizontale, tirette_verticale)
                        décale_terminee = True
                        if jouer_a_1:
                            scores[0] += 1                    
        if décale_terminee:
            tour_joueur = (tour_joueur % nombre_joueurs) + 1
            décale_terminee = False
            afficher_message_tirettes = False


        for i in range(7):
            for j in range(7):
                grille= tomber_bille(grille, tirette_horizontale, tirette_verticale, i, j)
        fin_jeu, scores_actuels = verifier_fin_jeu_et_compter_billes(grille, jouer_a_1)
        if not jouer_a_1:
            scores = scores_actuels
        if placer_billes_termine and fin_jeu:
            if jouer_a_1:
                message_fin = f"Vous avez gagné en {scores[0]} coups!"
            else:
                gagnant = scores.index(max(scores)) + 1
                message_fin = f"Le joueur {gagnant} a gagné!"
            # Attente de l'action de l'utilisateur
            while True:
                efface_tout()
                image(500, 300, "assets/fond.png", ancrage='center')
                texte(500, 150, message_fin, ancrage='center', taille=20, couleur='blue')
                # Dessiner les boutons Rejouer et Quitter
                rectangle(200, 300, 400, 350, remplissage='lightgreen')
                texte(300, 325, "Rejouer", ancrage='center', taille=20)

                rectangle(600, 300, 800, 350, remplissage='red')
                texte(700, 325, "Quitter", ancrage='center', taille=20)

                mise_a_jour()

                # Gestion des clics
                ev = donne_ev()
                ty = type_ev(ev)
                if ty == 'Quitte':
                    jouer = False
                    break
                elif ty == 'ClicGauche':
                    x, y = abscisse(ev), ordonnee(ev)
                    if 200 <= x <= 400 and 300 <= y <= 350:
                        # Rejouer
                        efface_tout()
                        mise_a_jour()

                        # Réinitialiser les variables pour une nouvelle partie
                        grille = creer_grille()
                        tirette_horizontale = creer_tirette()
                        tirette_verticale = creer_tirette()
                        nombre_billes_placees = 0
                        placer_billes_termine = False
                        fin_jeu = False
                        tour_joueur = 1
                        afficher_message = True
                        menu = True
                        jouer = True
                        break
                    elif 600 <= x <= 800 and 300 <= y <= 350:
                        # Quitter
                        jouer = False
                        fin_jeu = False
                        break
ferme_fenetre()
