import math
from Configuration import configuration
from Utilities import Algo_A_etoile


class Controleur:
    def __init__(self):
        self.cible_souris = None
        self.objets_jeu = None
        self.point_cible = None
        self.traj = False
        self.liste_points = []
        self.aller_vers_point = False

    def attacher_modele(self, modele):
        self.objets_jeu = modele

    def selection_point(self, mx: float, my: float):
        """Associe le clic souris à un point de la grille"""
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
        self.liste_points, liste_des_points_verifies = Algo_A_etoile.cheminPlusCourt(
            self, self.objets_jeu.grille.grille, point_joueur, point_arrivee
        )
        self.objets_jeu.grille.allumer_points(
            self.liste_points, liste_des_points_verifies
        )

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

    def mettre_les_points_intravesables_rect(self, joueur):
        for ligne in self.objets_jeu.grille.grille:
            for point in ligne:
                point.associer_traversabilité(True)

        for obstacle in self.objets_jeu.liste_obstacles:
            haut_gauche = (obstacle.x - joueur.taille, obstacle.y - joueur.taille)
            bas_droit = (
                obstacle.x + obstacle.largeur + joueur.taille,
                obstacle.y + obstacle.hauteur + joueur.taille,
            )
            for ligne in self.objets_jeu.grille.grille:
                for point in ligne:
                    if (
                        haut_gauche[0] <= point.x <= bas_droit[0] and haut_gauche[1] <= point.y <= bas_droit[1]
                    ):
                        point.associer_traversabilité(False)


def limite_bord_et_diago(joueur, dx, dy):
    """Empêche le joueur de dépasser les bords de l'écran"""
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
