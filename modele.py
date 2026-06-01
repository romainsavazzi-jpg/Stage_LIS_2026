

class Joueur:
    def __init__(self, x, y, vitesse=15, taille=20):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.taille = taille

    def bouger_fleche(self, dx, dy, facteur):
        self.x += dx * facteur
        self.y += dy * facteur
