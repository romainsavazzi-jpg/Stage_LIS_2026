import math
from configuration import largeur, hauteur


class Controleur:
    def __init__(self):
        self.cible_souris = None

    def gerer_fleches(self, joueur, dx, dy):
        if dx != 0 or dy != 0:
            self.cible_souris = None
            if dx != 0 and dy != 0:
                facteur = joueur.vitesse / math.sqrt(2)
            else:
                facteur = joueur.vitesse
            dx, dy = limite_bord(joueur, dx, dy, facteur)
            joueur.bouger_fleche(dx, dy, facteur)

    # def gerer_click(self, joueur, x, y):
    #     joueur.bouger_click(x, y)

    # def

    def deplacer_vers_cible(self, joueur):
        if self.cible_souris is None:
            return
        mx, my = self.cible_souris

        dx, dy = 0, 0

        if joueur.x < mx - joueur.vitesse:
            dx = 1
        elif joueur.x > mx + joueur.vitesse:
            dx = -1
        else:
            dx = 0
        if joueur.y < my - joueur.vitesse:
            dy = 1
        elif joueur.y > my + joueur.vitesse:
            dy = -1
        else:
            dy = 0

        # Arrivé à destination
        if dx == 0 and dy == 0:
            self.cible_souris = None
            return

        # Si déplacement diagonal : la vitesse est adaptée
        if dx != 0 and dy != 0:
            facteur = joueur.vitesse / math.sqrt(2)
        else:
            facteur = joueur.vitesse
        dx, dy = limite_bord(joueur, dx, dy, facteur)
        joueur.bouger_fleche(dx, dy, facteur)


def limite_bord(joueur, dx, dy, facteur):
    bord_droit = joueur.x + joueur.taille
    bord_gauche = joueur.x - joueur.taille
    bord_haut = joueur.y - joueur.taille
    bord_bas = joueur.y + joueur.taille
    if bord_droit + facteur >= largeur and dx == 1:
        joueur.tp_bord(largeur - bord_droit, "horizontal")
        dx = 0
    if bord_gauche - facteur <= 0 and dx == -1:
        joueur.tp_bord(0 - bord_gauche, "horizontal")
        dx = 0
    if bord_haut - facteur <= 0 and dy == -1:
        joueur.tp_bord(0 - bord_haut, "vertical")
        dy = 0
    if bord_bas + facteur >= hauteur and dy == 1:
        joueur.tp_bord(hauteur - bord_bas, "vertical")
        dy = 0
    return dx, dy
