from Configuration import configuration


class Objets_jeu:
    def __init__(self):
        self.liste_joueurs = []
        self.liste_obstacles = []
        self.grille = None
        # self.controleur = None

    # def attacher_controleur(self, controleur):
    #     self.controleur = controleur

    def ajouter_joueur(self, objet):
        """Ajoute un joueur à la liste des joueurs"""
        self.liste_joueurs.append(objet)

    def ajouter_obstacle(self, objet):
        """Ajoute un obstacle à la liste des obstacles"""
        self.liste_obstacles.append(objet)
        # self.controleur.mettre_les_points_intravesables(self.liste_joueurs[0])

    def get_joueur(self, indice):
        """Récupère un joueur à partir de son indice dans la liste des joueurs"""
        return self.liste_joueurs[indice]

    def ajouter_grille(self, objet):
        """Ajoute une grille au modèle"""
        self.grille = objet


class Joueur:
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

    def bouger_fleche(self, dx, dy, facteur):
        """Fait bouger le joueur en fonction des touches pressées et du facteur de déplacement calculé pour gérer les déplacements diagonaux et les limites de l'écran"""
        self.x += dx * facteur
        self.y += dy * facteur

    def tp_bord(self, marge_a_tp, direction):
        """Téléporte le joueur au bord si il essaye de se déplacer hors de l'écran"""
        if direction == "horizontal":
            self.x += marge_a_tp
        if direction == "vertical":
            self.y += marge_a_tp

    def change_taille(self, increment):
        """Change la taille du joueur"""
        self.taille += increment

    def change_vitesse(self, increment):
        """Change la vitesse du joueur"""
        self.vitesse += increment


class Obstacle_rect:
    def __init__(self, x, y, largeur, hauteur, couleur=configuration.couleur_rectangle):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur


class Point:
    def __init__(self, x, y, traversable=True, couleur=configuration.couleur_point):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.traversable = traversable

    def __str__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.traversable)

    def changer_couleur_point(self, couleur):
        self.couleur = couleur

    def associer_traversabilité(self, traversabilite):
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

    def diviser_ecran(self):
        """Divise l'écran en une grille de points et les stocke dans une matrice"""
        self.ecart = configuration.largeur / self.nbr_division
        premier = Point(0 + self.ecart // 2, 0 + self.ecart // 2)
        coordonnee = premier
        nbr_carres_hauteur = int((configuration.hauteur // self.ecart) + 1)
        for i in range(nbr_carres_hauteur):
            ligne = []
            for j in range(self.nbr_division):
                ligne.append(coordonnee)
                coordonnee = Point(coordonnee.x + self.ecart, coordonnee.y)
            self.grille.append(ligne)
            coordonnee = Point(premier.x, coordonnee.y + self.ecart)

    def allumer_points(self, liste_points, liste_des_points_verifies):
        """Colorie les points du meilleur chemin trouvé en vert et les points vérifiés en rose"""
        for point in liste_des_points_verifies:
            point.couleur = (250, 60, 250)
        for point in liste_points:
            point.couleur = (20, 250, 100)
