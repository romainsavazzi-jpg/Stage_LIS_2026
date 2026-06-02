from vecteurs import Vecteur2D


class Carte:
    def __init__(self):
        self.liste = []

    def ajouter(self, objet):
        self.liste.append(objet)


class Joueur:
    def __init__(self, x, y, taille=40):
        self.friction = 0.8
        self.cst_acceleration = 2
        self.vitesse_max = 15
        self.taille = taille

        self.position = Vecteur2D(x, y)
        self.vitesse = Vecteur2D(0, 0)
        self.acceleration = Vecteur2D(0, 0)

    def bouger(self, dx, dy, facteur):  # sert pour le déplacement
        self.position.x += dx * facteur
        self.position.y += dy * facteur

    def tp_bord(self, marge_a_tp, direction):
        if direction == "horizontal":
            self.position.x += marge_a_tp
        if direction == "vertical":
            self.position.y += marge_a_tp

    # def bouger_click(self, x, y):
    #     self.x = x
    #     self.y = y


class Obstacle_rect:
    def __init__(self, x, y, largeur, hauteur, couleur):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
