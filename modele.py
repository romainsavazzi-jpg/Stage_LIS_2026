class Carte:
    def __init__(self):
        self.liste = []

    def ajouter(self, objet):
        self.liste.append(objet)


class Joueur:
    def __init__(self, x, y, vitesse=15, taille=20):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.taille = taille

    def bouger_fleche(self, dx, dy, facteur):
        self.x += dx * facteur
        self.y += dy * facteur

    def tp_bord(self, marge_a_tp, direction):
        if direction == "horizontal":
            self.x += marge_a_tp
        elif direction == "vertical":
            self.y += marge_a_tp

    def bouger_click(self, x, y):
        self.x = x
        self.y = y


class Obstacle_rect:
    def __init__(self, x, y, largeur, hauteur, couleur):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
