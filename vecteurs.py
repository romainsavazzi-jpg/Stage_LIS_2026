import math


class Vecteur2D:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, autre):
        return Vecteur2D(self.x + autre.x, self.y + autre.y)

    def __sub__(self, autre):
        return Vecteur2D(self.x - autre.x, self.y - autre.y)

    def __mul__(self, scalaire):
        return Vecteur2D(self.x * scalaire, self.y * scalaire)

    def __str__(self):
        return "Vecteur2D (", self.x, " ; ", self.y, " )"

    def longueur(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalise(self):
        long = self.longueur()
        if long == 0:
            return Vecteur2D(0, 0)
        return Vecteur2D(self.x / long, self.y / long)

    #  Normalise la longueur comme pour les ressort vecteur OM sur norme de OM
