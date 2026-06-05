from configuration import largeur, hauteur, couleur_joueur, couleur_point, couleur_rectangle, divisions


class Objets_jeu:
    def __init__(self):
        self.liste_joueurs = []
        self.liste_obstacles = []
        self.grille = None

    def ajouter_joueur(self, objet):
        self.liste_joueurs.append(objet)

    def ajouter_obstacle(self, objet):
        self.liste_obstacles.append(objet)

    def get_joueur(self, indice):
        return self.liste_joueurs[indice]

    def ajouter_grille(self, objet):
        self.grille = objet


class Joueur:
    def __init__(self, x, y, couleur=couleur_joueur, vitesse=15, taille=40):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.vitesse = vitesse
        self.taille = taille

    def bouger_fleche(self, dx, dy, facteur):
        self.x += dx * facteur
        self.y += dy * facteur

    def tp_bord(self, marge_a_tp, direction):
        if direction == "horizontal":
            self.x += marge_a_tp
        if direction == "vertical":
            self.y += marge_a_tp

    def change_taille(self, increment):
        self.taille += increment

    def change_vitesse(self, increment):
        self.vitesse += increment


class Obstacle_rect:
    def __init__(self, x, y, largeur, hauteur, couleur=couleur_rectangle):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur


class Point:
    def __init__(self, x, y, traversable=True, couleur=couleur_point):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.traversable = traversable

    def __str__(self):
        return (str(self.x) + " " + str(self.y) + " " + str(self.traversable))


class Grille:
    def __init__(self, nbr_division=divisions):
        self.ecart = None
        self.grille = []
        self.nbr_division = nbr_division

    def diviser_ecran(self):
        self.ecart = largeur / self.nbr_division
        premier = Point(0 + self.ecart // 2, 0 + self.ecart // 2)
        coordonnee = premier
        nbr_carres_hauteur = int((hauteur // self.ecart) + 1)
        for i in range(nbr_carres_hauteur):
            ligne = []
            for j in range(self.nbr_division):
                ligne.append(coordonnee)
                coordonnee = Point(coordonnee.x + self.ecart, coordonnee.y)
            self.grille.append(ligne)
            coordonnee = Point(premier.x, coordonnee.y + self.ecart)
