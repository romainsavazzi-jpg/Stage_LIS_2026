import math
from Configuration import configuration
from Utilities import Algo_A_etoile, Bresenham


class Controleur:
    def __init__(self):
        self.cible_souris = None
        self.objets_jeu = None
        self.point_cible = None
        self.traj = False
        self.liste_points = []
        self.liste_des_points_verifies = []
        self.pixel_chemin = []
        self.aller_vers_point = False

    def attacher_modele(self, modele):
        self.objets_jeu = modele

    def selection_point(self, mx: float, my: float):
        """Associe les coordonnées du point de l'écran auquel on applique la méthode à un point de la grille"""
        ecart = self.objets_jeu.grille.ecart
        x_point = int(mx // ecart)
        y_point = int(my // ecart)
        return self.objets_jeu.grille.grille[y_point][x_point], x_point, y_point
        # (x_point, y_point)
        # self.point_cible = self.objets_jeu.grille.grille[y_point][x_point]
        # self.point_cible.couleur = (20, 250, 100)

    def selection_point_cible(self, point):
        """Définit le point cible vers lequel le joueur doit se diriger"""
        self.point_cible = point
        return point

    def determiner_chemin(self, point_arrivee):
        """Créer une liste de points à suivre pour aller de la position du joueur au point d'arrivée"""
        joueur = self.objets_jeu.get_joueur(0)
        point_joueur, _, _ = self.selection_point(joueur.x, joueur.y)
        self.liste_points, self.liste_des_points_verifies = Algo_A_etoile.cheminPlusCourt(
            self, self.objets_jeu.grille.grille, point_joueur, point_arrivee
        )
        self.liste_points, self.liste_des_points_verifies = Algo_A_etoile.determination_liste_reduite_chemin(self.liste_points, self.liste_des_points_verifies)
        self.objets_jeu.grille.allumer_points(
            self.liste_points, self.liste_des_points_verifies
        )
        """Détermine une liste de pixels pour tracer une droite entre les deux points de la grille"""
        self.pixel_chemin = []
        for i in range(len(self.liste_points) - 1):
            self.pixel_chemin += Bresenham.bresenham(
                (self.liste_points[i].x, self.liste_points[i].y), (self.liste_points[i + 1].x, self.liste_points[i + 1].y)
            )
        if self.liste_points:
            self.pixel_chemin = Bresenham.bresenham((joueur.x, joueur.y), (self.liste_points[0].x, self.liste_points[0].y)) + self.pixel_chemin

    def se_rendre_aux_points(self):
        """Fait suivre au joueur les points de la liste des points du chemin un par un"""
        if self.liste_points == []:
            self.aller_vers_point = False
            return
        if not self.aller_vers_point or self.point_cible is not None:
            return
        point = self.selection_point_cible(self.liste_points.pop(0))
        point.changer_couleur_point(configuration.couleur_point)

    def gerer_deplacement_touches(self, dx, dy):
        """Gère le déplacement du joueur en fonction des touches pressées"""
        joueur = self.objets_jeu.get_joueur(0)

        if dx != 0 or dy != 0:
            self.cible_souris = None
            self.point_cible = None
            self.aller_vers_point = False
            dx, dy, facteur = limite_bord_et_diago(joueur, dx, dy)
            joueur.bouger_fleche(dx, dy, facteur)

    def deplacer_vers_cible(self):
        """Gère le déplacement du joueur vers la cible définie par le clic souris"""

        joueur = self.objets_jeu.get_joueur(0)

        if self.point_cible is None:
            return
        else:
            mx, my = (
                self.point_cible.x,
                self.point_cible.y,
            )  # qui sera forcément un point de la grille, grâce à la fonction selection_point et selection_point_cible

        # if self.cible_souris is None:
        #     return
        # else:
        #     mx, my = self.cible_souris

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
            self.cible_souris = None
            self.point_cible = None
            return
        dx, dy, facteur = limite_bord_et_diago(joueur, dx, dy)
        joueur.bouger_fleche(dx, dy, facteur)

    # def recharger_traversables(self):
    #     # Aplatir la matrice en liste
    #     liste_grille = [p for ligne in self.objets_jeu.grille.grille for p in ligne]

    #     # Soustraire les points de la trajectoire des points à actualiser
    #     Listes_points_traj_set = set(self.liste_points)  # | set(self.liste_des_points_verifies)
    #     liste_grille_moins_points = [p for p in liste_grille if p not in Listes_points_traj_set]

    #     for point in liste_grille_moins_points:
    #         point.associer_traversabilité(True)

    def mettre_les_points_intravesables_rect(self, joueur):
        ecart = self.objets_jeu.grille.ecart
        largeur = configuration.largeur
        hauteur = configuration.hauteur
        # Aplatir la matrice en liste
        liste_grille = [p for ligne in self.objets_jeu.grille.grille for p in ligne]

        # Soustraire les points de la trajectoire des points à actualiser
        Listes_points_traj_set = set(self.liste_points) | set(self.liste_des_points_verifies)
        liste_grille_moins_points = [p for p in liste_grille if p not in Listes_points_traj_set]

        for point in liste_grille_moins_points:
            point.associer_traversabilité(True)

        for obstacle in self.objets_jeu.liste_obstacles:
            haut_gauche = (obstacle.x - joueur.taille, obstacle.y - joueur.taille)
            bas_droit = (
                obstacle.x + obstacle.largeur + joueur.taille,
                obstacle.y + obstacle.hauteur + joueur.taille,
            )
            mx = haut_gauche[0]
            my = haut_gauche[1]
            for i in range(int((bas_droit[1] - haut_gauche[1]) // ecart) + 2):
                mx = haut_gauche[0]
                for j in range(int((bas_droit[0] - haut_gauche[0]) // ecart) + 2):
                    if appartient_aux_limites_de_la_map(mx, largeur) and appartient_aux_limites_de_la_map(my, hauteur):
                        point, _, _ = self.selection_point(mx, my)
                        if (
                            haut_gauche[0] <= point.x <= bas_droit[0] and haut_gauche[1] <= point.y <= bas_droit[1]
                        ) and point not in Listes_points_traj_set:
                            point.associer_traversabilité(False)
                    mx += ecart
                my += ecart

        # Collision pour les bords
        for point in liste_grille_moins_points:
            if (
                point.x <= self.objets_jeu.liste_joueurs[0].taille or point.x >= configuration.largeur - self.objets_jeu.liste_joueurs[0].taille or point.y <= self.objets_jeu.liste_joueurs[0].taille or point.y >= configuration.hauteur - self.objets_jeu.liste_joueurs[0].taille
            ):
                point.associer_traversabilité(False)

            # pos_x_i = haut_gauche[0]
            # pos_y_i = haut_gauche[1]
            # if not appartient_aux_limites_de_la_map(pos_x_i, largeur):
            #     pos_x_i = 0
            # if not appartient_aux_limites_de_la_map(pos_y_i, hauteur):
            #     pos_y_i = 0
            # pos_x, pos_y = pos_x_i, pos_y_i
            #
            # pos_x_f = bas_droit[0]
            # pos_y_f = bas_droit[1]
            # if not appartient_aux_limites_de_la_map(pos_x_f, largeur):
            #     pos_x_f = largeur
            # if not appartient_aux_limites_de_la_map(pos_y_f, hauteur):
            #     pos_y_f = largeur
            #
            # while pos_y < pos_y_f:  # or 0 < pos_x or pos_x < configuration.largeur:
            #     pos_x = pos_x_i
            #     # if 0 > pos_y or pos_y > configuration.hauteur:
            #     #     continue
            #     while pos_x < pos_x_f:  # or 0 < pos_y or pos_y < configuration.hauteur:
            #         # if 0 > pos_x or pos_x > configuration.largeur:
            #         #     continue
            #         point, _, _ = self.selection_point(pos_x, pos_y)
            #         if (
            #             haut_gauche[0] <= point.x <= bas_droit[0] and haut_gauche[1] <= point.y <= bas_droit[1]
            #         ):
            #             point.associer_traversabilité(False)
            #         pos_x += ecart
            #     pos_y += ecart

            # pos_x_i = haut_gauche[0]
            # pos_y_i = haut_gauche[1]
            # if not appartient_aux_limites_de_la_map(pos_x_i, largeur):
            #     pos_x_i = 0
            # if not appartient_aux_limites_de_la_map(pos_y_i, hauteur):
            #     pos_y_i = 0
            # pos_x, pos_y = pos_x_i, pos_y_i
            #
            # pos_x_f = bas_droit[0]
            # pos_y_f = bas_droit[1]
            # if not appartient_aux_limites_de_la_map(pos_x_f, largeur):
            #     pos_x_f = largeur
            # if not appartient_aux_limites_de_la_map(pos_y_f, hauteur):
            #     pos_y_f = largeur
            #
            # while pos_y < pos_y_f:  # or 0 < pos_x or pos_x < configuration.largeur:
            #     pos_x = pos_x_i
            #     # if 0 > pos_y or pos_y > configuration.hauteur:
            #     #     continue
            #     while pos_x < pos_x_f:  # or 0 < pos_y or pos_y < configuration.hauteur:
            #         # if 0 > pos_x or pos_x > configuration.largeur:
            #         #     continue
            #         point, _, _ = self.selection_point(pos_x, pos_y)
            #         if (
            #             haut_gauche[0] <= point.x <= bas_droit[0] and haut_gauche[1] <= point.y <= bas_droit[1]
            #         ):
            #             point.associer_traversabilité(False)
            #         pos_x += ecart
            #     pos_y += ecart

            # point, pos_x_h, pos_y_h = self.selection_point(haut_gauche[0], haut_gauche[1])
            # pos_x, pos_y = pos_x_h, pos_y_h
            # x, y = point.x, point.y
            # while y < bas_droit[1]:
            #     pos_x = pos_x_h
            #     point = self.objets_jeu.grille.grille[pos_y][pos_x]
            #     if 0 > point.y > configuration.hauteur:
            #         continue
            #     while x < bas_droit[0]:
            #         if 0 > point.x > configuration.largeur:
            #             continue
            #         # point, _, _ = self.selection_point(pos_x, pos_y)
            #         point.associer_traversabilité(False)
            #         point = self.objets_jeu.grille.grille[pos_y][pos_x]
            #         x, y = point.x, point.y
            #         pos_x += 1
            #     pos_y += 1

            # for point in liste_grille_moins_points:
            #     if (
            #         haut_gauche[0] <= point.x <= bas_droit[0] and haut_gauche[1] <= point.y <= bas_droit[1]
            #     ) or (
            #         point.x <= self.objets_jeu.liste_joueurs[0].taille or point.x >= configuration.largeur - self.objets_jeu.liste_joueurs[0].taille or point.y <= self.objets_jeu.liste_joueurs[0].taille or point.y >= configuration.hauteur - self.objets_jeu.liste_joueurs[0].taille
            #     ):
            #         point.associer_traversabilité(False)

    def changer_taille(self, increment):
        self.objets_jeu.liste_joueurs[0].change_taille(increment)
        self.mettre_les_points_intravesables_rect(self.objets_jeu.liste_joueurs[0])


def appartient_aux_limites_de_la_map(pos_x_y, longueur):
    if pos_x_y > 0 and pos_x_y < longueur:
        return True


def limite_bord_et_diago(joueur, dx, dy):
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
