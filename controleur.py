import math
from configuration import largeur, hauteur


class Controleur:
    def __init__(self):
        pass

    def gerer_fleches(self, joueur, dx, dy):
        if dx != 0 or dy != 0:
            if dx != 0 and dy != 0:
                facteur = joueur.vitesse / math.sqrt(2)
            else:
                facteur = joueur.vitesse
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
            joueur.bouger_fleche(dx, dy, facteur)


    # def gerer_click(self, joueur, x, y):
    #     joueur.bouger_click(x, y)


    # def 




    def deplacer(self, joueur, mx, my):
        # while joueur.x != mx and joueur.y != my:
        dx, dy = 0, 0
        
        if joueur.x < mx:
            dx = 1
        elif joueur.x > mx:
            dx = -1
        if joueur.y < my:
            dy = 1
        elif joueur.y > my:
            dy = -1
        # else:
        #     dx, dy = 0, 0
        if dx != 0 and dy != 0:
            facteur = joueur.vitesse / math.sqrt(2)
        else:
            facteur = joueur.vitesse
        joueur.bouger_fleche(dx, dy, facteur)
