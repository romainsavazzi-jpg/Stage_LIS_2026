from Configuration import configuration
from Utilities.projection import projection_point_sur_segment
# from math import sqrt, cos, sin


class Objets_jeu:
    """Objets_jeu correspond au Modèle du design patern MVC mais on trouvait le nom "Objets_jeu" plus parlant"""
    def __init__(self):
        self.liste_joueurs = []
        self.liste_obstacles = []
        self.grille = None

    def ajouter_joueur(self, joueur):  # test
        self.liste_joueurs.append(joueur)

    def ajouter_obstacle(self, obstacle):  # test
        self.liste_obstacles.append(obstacle)

    def get_joueur(self, indice):  # test
        """Récupère un joueur à partir de son indice dans la liste des joueurs"""
        return self.liste_joueurs[indice]

    def ajouter_grille(self, grille):  # test
        self.grille = grille


class Collisions:
    def __init__(self):
        pass

    def collision_rect_rect(self, rect, dx, dy, facteur):
        if (
            self.x + dx * facteur >= rect.x + rect.largeur
            or self.x + dx * facteur <= rect.x - self.largeur
            or self.y + dy * facteur <= rect.y - self.hauteur
            or self.y + dy * facteur >= rect.y + rect.hauteur
        ):
            return False
        return True

    def collision_cercle_cercle(self, other, dx, dy, facteur):
        distance_entre_centres = (((self.x + dx * facteur) - other.x) ** 2 + ((self.y + dy * facteur) - other.y) ** 2)
        if distance_entre_centres < (self.taille + other.taille) ** 2:
            return True

    def collision_cercle_point(self, x, y, rayon, x_autre, y_autre):
        if ((x - x_autre) ** 2 + (y - y_autre) ** 2) <= rayon ** 2:
            return True

    def collision_cercle_rect(self, rect, dx, dy, facteur):
        carre_autour_du_cercle = Obstacle_rect(self.x - self.taille, self.y - self.taille, 2 * self.taille, 2 * self.taille)
        if not carre_autour_du_cercle.collision_rect_rect(rect, dx, dy, facteur):  # si les deux rectangles ont rien en commun il s'arrète pas de le collisions
            return False

        # sinon on regarde si l'un des coins du rectangle est dans le cercle
        if (
            self.collision_cercle_point(rect.x, rect.y, self.taille, self.x + dx * facteur, self.y + dy * facteur)
            or self.collision_cercle_point(rect.x, rect.y + rect.hauteur, self.taille, self.x + dx * facteur, self.y + dy * facteur)
            or self.collision_cercle_point(rect.x + rect.largeur, rect.y, self.taille, self.x + dx * facteur, self.y + dy * facteur)
            or self.collision_cercle_point(rect.x + rect.largeur, rect.y + rect.hauteur, self.taille, self.x + dx * facteur, self.y + dy * facteur)
        ):
            return True

        return projection_point_sur_segment(self.x + dx * facteur, self.y + dy * facteur, rect.x, rect.y, rect.x + rect.largeur, rect.y) or projection_point_sur_segment(self.x + dx * facteur, self.y + dy * facteur, rect.x, rect.y, rect.x, rect.y + rect.hauteur)  # Dernier cas qui regarde si le cercle coupe le rectangle au milieu d'un segment ou si on est dans un angle de la box autour du cercle

        # sinon on regarde si le cercle est en collisions avec les bords du rectangle


class Joueur(Collisions):
    def __init__(
        self,
        x,
        y,
        couleur=configuration.couleur_joueur,
        vitesse=configuration.vitesse,
        taille=configuration.taille,
    ):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.vitesse = vitesse
        self.taille = taille

    def bouger(self, dx, dy, facteur):  # test
        """Fait bouger le joueur en fonction du déplacement dx et dy donné (-1, 0, 1) et du facteur de déplacement calculé pour gérer les déplacements diagonaux et les limites de l'écran"""
        self.x += dx * facteur
        self.y += dy * facteur

    def tp_bord(self, marge_a_tp, direction):  # test
        """Téléporte le joueur au bord si il essaye de se déplacer hors de l'écran"""
        if direction == "horizontal":
            self.x += marge_a_tp
        if direction == "vertical":
            self.y += marge_a_tp

    def change_taille(self, increment):  # test
        if self.taille + increment >= 0:
            self.taille += increment

    def change_vitesse(self, increment):  # test
        if self.vitesse + increment >= 0:
            self.vitesse += increment


class Obstacle(Collisions):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Obstacle_rect(Obstacle):
    def __init__(self, x, y, largeur, hauteur, couleur=configuration.couleur_rectangle):
        super().__init__(x, y)
        self.couleur = couleur
        self.largeur = largeur
        self.hauteur = hauteur


class Obstacle_cercle(Obstacle):
    def __init__(self, x, y, taille=configuration.taille, couleur=configuration.couleur_cercle):
        super().__init__(x, y)
        self.couleur = couleur
        self.taille = taille


class Point(Collisions):
    def __init__(self, x, y, traversable=True, couleur=configuration.couleur_point):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.traversable = traversable

    def __eq__(self, other):  # test
        return self.x == other.x and self.y == other.y

    def __hash__(self):  # test
        return hash((self.x, self.y))

    def __str__(self):  # test
        return str(self.x) + " " + str(self.y) + " " + str(self.traversable)

    def changer_couleur_point(self, couleur):  # Test
        self.couleur = couleur

    def associer_traversabilité(self, traversabilite: bool):  # Test
        "Rend les points de la grille traversable ou non par A*"
        self.traversable = traversabilite
        if traversabilite:
            self.changer_couleur_point(configuration.couleur_point)
        else:
            self.changer_couleur_point(configuration.couleur_point_intravesable)


class Grille:
    def __init__(self, nbr_division=configuration.divisions):
        self.ecart = None
        self.grille = []
        self.nbr_division = nbr_division

    def diviser_ecran(self):  # Test
        """Divise l'écran en une grille de points et les stocke dans une matrice"""
        self.ecart = configuration.largeur / self.nbr_division
        premier = Point(0 + self.ecart / 2, 0 + self.ecart / 2)
        coordonnee = premier
        nbr_carres_hauteur = int((configuration.hauteur // self.ecart) + 1)
        for i in range(nbr_carres_hauteur):
            ligne = []
            for j in range(self.nbr_division):
                ligne.append(coordonnee)
                coordonnee = Point(coordonnee.x + self.ecart, coordonnee.y)
            self.grille.append(ligne)
            coordonnee = Point(premier.x, coordonnee.y + self.ecart)

    def allumer_points(self, liste_points, liste_des_points_verifies):  # Test
        """Colorie les points du meilleur chemin trouvé en vert et les points vérifiés en rose"""
        # for point in liste_des_points_verifies:
        #     point.couleur = configuration.couleur_points_verifie
        for point in liste_points:
            point.couleur = configuration.couleur_points_chemin
