import math
from Configuration import configuration
from Utilities import Algo_A_etoile, Bresenham
from modele import Obstacle_rect, Obstacle_cercle


class Controleur:
    def __init__(self):
        self.objets_jeu = None
        self.point_cible = None
        self.traj = False
        self.liste_points = []
        self.liste_points_reduite = []
        self.liste_des_points_verifies = []
        self.pixel_chemin = []
        self.liste_points_d_accroche = []
        self.aller_vers_point = False
        self.on_deplace = False
        self.indice_accroche = 0

    def attacher_modele(self, modele):
        self.objets_jeu = modele

    def changer_taille(self, increment):
        self.objets_jeu.liste_joueurs[0].change_taille(increment)
        self.mettre_les_points_intravesables_rect(self.objets_jeu.liste_joueurs[0])

    def selection_point(self, mx: float, my: float):  # Test
        """Associe les coordonnées du point de l'écran auquel on applique la méthode à un point de la grille"""
        ecart = self.objets_jeu.grille.ecart
        x_point = int(mx // ecart)
        y_point = int(my // ecart)
        return self.objets_jeu.grille.grille[y_point][x_point], x_point, y_point

    def selection_point_cible(self, point):  # Test
        """Définit le point cible vers lequel le joueur doit se diriger"""
        self.point_cible = point
        return point

    def determiner_chemin(self):
        """Créer une liste de points à suivre pour aller de la position du joueur au point d'arrivée"""
        # Initialisation du chemin
        joueur = self.objets_jeu.get_joueur(0)
        self.liste_points = []
        point_joueur, _, _ = self.selection_point(joueur.x, joueur.y)
        point_1 = point_joueur

        # Boucle déterminant le chemin
        for point_d_accroche in self.liste_points_d_accroche:
            point_2 = point_d_accroche
            liste_points_a_rajouter, self.liste_des_points_verifies = (
                Algo_A_etoile.cheminPlusCourt(
                    self, self.objets_jeu.grille.grille, point_1, point_2
                )
            )
            if liste_points_a_rajouter:
                self.liste_points += liste_points_a_rajouter
            point_1 = point_2

        # Détermination liste réduite du chemin
        self.liste_points_reduite = (Algo_A_etoile.determination_liste_reduite_chemin(self.liste_points))
        self.objets_jeu.grille.allumer_points(
            self.liste_points_reduite, self.liste_des_points_verifies
        )
        """Détermine une liste de pixels pour tracer une droite entre les deux points de la grille"""
        self.pixel_chemin = []
        for i in range(len(self.liste_points_reduite) - 1):
            self.pixel_chemin += Bresenham.bresenham(
                (self.liste_points_reduite[i].x, self.liste_points_reduite[i].y),
                (self.liste_points_reduite[i + 1].x, self.liste_points_reduite[i + 1].y),
            )
        if self.liste_points_reduite:
            self.pixel_chemin = (Bresenham.bresenham((joueur.x, joueur.y), (self.liste_points_reduite[0].x, self.liste_points_reduite[0].y)) + self.pixel_chemin)

    def lancer_chemin(self, mx, my):
        point_arrivee, _, _ = self.selection_point(mx, my)
        if point_arrivee.traversable:
            self.traj = True
            self.liste_points_d_accroche.append(point_arrivee)
        self.determiner_chemin()

    def actualiser_deplacement_point_d_accroche(self, mx, my):
        point_d_accroche, _, _ = self.selection_point(mx, my)
        if point_d_accroche.traversable:
            self.liste_points_d_accroche[self.indice_accroche] = point_d_accroche
        self.determiner_chemin()

    def selection_point_d_accroche(self, mx, my):
        points_potentiels = []
        self.indice_accroche = 0
        for point in self.liste_points:
            if point.collision_cercle_point(point.x, point.y, configuration.taille_selec_point_d_accroche, mx, my):
                if point in self.liste_points_d_accroche:
                    self.indice_accroche = self.liste_points_d_accroche.index(point)
                    self.on_deplace = True
                    return
                points_potentiels.append(point)

        if points_potentiels:
            meilleur_point = points_potentiels[0]
            ancienne_distance_au_click = (mx - meilleur_point.x) ** 2 + (my - meilleur_point.y) ** 2
            for point in points_potentiels:
                distance_au_click = (mx - point.x) ** 2 + (my - point.y) ** 2
                if distance_au_click < ancienne_distance_au_click:
                    meilleur_point = point
                    ancienne_distance_au_click = distance_au_click
            for point in self.liste_points:
                if point in self.liste_points_d_accroche:
                    indice_point_d_accroche_regarde = self.liste_points_d_accroche.index(point) + 1
                    if self.indice_accroche < indice_point_d_accroche_regarde:
                        self.indice_accroche = indice_point_d_accroche_regarde
                if point == meilleur_point:
                    self.liste_points_d_accroche.insert(self.indice_accroche, meilleur_point)
                    self.on_deplace = True
                    break

    def se_rendre_aux_points(self):
        """Fait suivre au joueur les points de la liste des points du chemin un par un"""
        if self.liste_points_reduite == []:
            self.aller_vers_point = False
            return
        if not self.aller_vers_point or self.point_cible is not None:
            return
        point = self.selection_point_cible(self.liste_points_reduite.pop(0))
        point.changer_couleur_point(configuration.couleur_point)

    def gerer_deplacement_touches(self, dx, dy):  # Test
        """Gère le déplacement du joueur en fonction des touches pressées"""
        joueur = self.objets_jeu.get_joueur(0)

        if dx != 0 or dy != 0:  # Si il y a déplacement
            self.point_cible = None
            self.pixel_chemin = []
            self.aller_vers_point = False
            dx, dy, facteur = limite_bord_et_diago(joueur, dx, dy)
            for obj in self.objets_jeu.liste_obstacles:
                if isinstance(obj, Obstacle_cercle):
                    if joueur.collision_cercle_cercle(obj, dx, dy, facteur):
                        dx, dy = 0, 0
            joueur.bouger(dx, dy, facteur)

    def deplacer_vers_cible(self):  # Test
        """Gère le déplacement du joueur vers la cible définie par le clic souris"""

        joueur = self.objets_jeu.get_joueur(0)

        if self.point_cible is None:
            return
        else:
            mx, my = (
                self.point_cible.x,
                self.point_cible.y,
            )

        dx, dy = 0, 0

        if joueur.x < mx - (joueur.vitesse // 2 + 1):
            dx = 1
        elif joueur.x > mx + (joueur.vitesse // 2 + 1):
            dx = -1
        else:
            dx = 0
        if joueur.y < my - (joueur.vitesse // 2 + 1):
            dy = 1
        elif joueur.y > my + (joueur.vitesse // 2 + 1):
            dy = -1
        else:
            dy = 0

        # Arrivé à destination
        if dx == 0 and dy == 0:
            self.point_cible = None
            if not self.liste_points:
                self.pixel_chemin = []
            return
        dx, dy, facteur = limite_bord_et_diago(joueur, dx, dy)
        joueur.bouger(dx, dy, facteur)

    def mettre_les_points_intravesables_rect(self, joueur):
        """défini la zone de collision entre le joueur et les obstacles rectangulaires et les bords"""
        ecart = self.objets_jeu.grille.ecart
        largeur = configuration.largeur
        hauteur = configuration.hauteur
        # Aplatir la matrice en liste
        liste_grille = [p for ligne in self.objets_jeu.grille.grille for p in ligne]

        # Soustraire les points de la trajectoire des points à actualiser
        Listes_points_traj_set = set(self.liste_points)  # | set(self.liste_des_points_verifies)
        liste_grille_moins_points = [
            p for p in liste_grille if p not in Listes_points_traj_set
        ]

        for point in liste_grille_moins_points:
            point.associer_traversabilité(True)

        for obstacle in self.objets_jeu.liste_obstacles:
            if isinstance(obstacle, Obstacle_rect):
                for dx in range(int(- (obstacle.x + joueur.taille)), int((obstacle.x + obstacle.largeur + joueur.taille) + 1), int(ecart)):
                    for dy in range(int(- (obstacle.y + joueur.taille)), int((obstacle.y + obstacle.hauteur + joueur.taille) + 1), int(ecart)):
                        nx, ny = obstacle.x + dx, obstacle.y + dy
                        if appartient_aux_limites_de_la_map(nx, largeur) and appartient_aux_limites_de_la_map(ny, hauteur):
                            point, _, _ = self.selection_point(nx, ny)
                            if (
                                obstacle.x - joueur.taille <= point.x <= obstacle.x + obstacle.largeur + joueur.taille and obstacle.y - joueur.taille <= point.y <= obstacle.y + obstacle.hauteur + joueur.taille
                            ) and point not in Listes_points_traj_set:
                                point.associer_traversabilité(False)
            elif isinstance(obstacle, Obstacle_cercle):
                rayon_collision = obstacle.taille + joueur.taille
                for dx in range(int(- (rayon_collision)), int((rayon_collision) + 1), int(ecart)):
                    for dy in range(int(- (rayon_collision)), int((rayon_collision) + 1), int(ecart)):
                        nx, ny = obstacle.x + dx, obstacle.y + dy
                        if appartient_aux_limites_de_la_map(nx, largeur) and appartient_aux_limites_de_la_map(ny, hauteur):
                            if (dx ** 2 + dy ** 2) < rayon_collision ** 2:
                                point, _, _ = self.selection_point(nx, ny)
                                point.associer_traversabilité(False)

        # Collision pour les bords
        for point in liste_grille_moins_points:
            if (
                point.x <= self.objets_jeu.liste_joueurs[0].taille or point.x >= configuration.largeur - self.objets_jeu.liste_joueurs[0].taille or point.y <= self.objets_jeu.liste_joueurs[0].taille or point.y >= configuration.hauteur - self.objets_jeu.liste_joueurs[0].taille
            ):
                point.associer_traversabilité(False)


def appartient_aux_limites_de_la_map(pos_x_y, longueur):  # Test
    if pos_x_y > 0 and pos_x_y < longueur:
        return True
    return False


def limite_bord_et_diago(joueur, dx, dy):  # Test
    """Empêche le joueur de dépasser les bords de l'écran et change la vitesse en fonction de diagonale ou pas
    Renvoie le déplacement et la bonne vitesse"""
    # Si déplacement diagonal : la vitesse est adaptée
    if dx != 0 and dy != 0:
        facteur = joueur.vitesse / math.sqrt(2)
    else:
        facteur = joueur.vitesse

    # Si le déplacement va dépasser le cadre, on ne déplace que vers la limite du bord
    bord_droit = joueur.x + joueur.taille
    bord_gauche = joueur.x - joueur.taille
    bord_haut = joueur.y - joueur.taille
    bord_bas = joueur.y + joueur.taille
    if bord_droit + facteur >= configuration.largeur and dx == 1:
        joueur.tp_bord(configuration.largeur - bord_droit, "horizontal")
        dx = 0
    if bord_gauche - facteur <= 0 and dx == -1:
        joueur.tp_bord(0 - bord_gauche, "horizontal")
        dx = 0
    if bord_haut - facteur <= 0 and dy == -1:
        joueur.tp_bord(0 - bord_haut, "vertical")
        dy = 0
    if bord_bas + facteur >= configuration.hauteur and dy == 1:
        joueur.tp_bord(configuration.hauteur - bord_bas, "vertical")
        dy = 0
    return dx, dy, facteur
