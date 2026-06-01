import math
from configuration import largeur, hauteur


class Controleur:
    def __init__(self):
        pass
    # self.controleur = 0

    def gerer_fleches(self, joueur, dx, dy):
        if dx != 0 or dy != 0:
            bord_droit = joueur.x + joueur.taille
            bord_gauche = joueur.x - joueur.taille
            bord_haut = joueur.y - joueur.taille
            bord_bas = joueur.y + joueur.taille
            if bord_droit + dx >= largeur and dx == 1:
                dx = 0
            if bord_gauche - dx <= 0 and dx == -1:
                dx = 0
            if bord_haut - dy <= 0 and dy == -1:
                dy = 0
            if bord_bas + dy >= hauteur and dy == 1:
                dy = 0
            if dx != 0 and dy != 0:
                facteur = joueur.vitesse / math.sqrt(2)
            else:
                facteur = joueur.vitesse
            joueur.bouger_fleche(dx, dy, facteur)
