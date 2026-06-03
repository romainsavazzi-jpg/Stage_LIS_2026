from modele import Joueur
from controleur import Controleur
import math


def test_mouvement_bord():
    jim = Joueur(0, 0)
    control = Controleur()
    control.gerer_fleches(jim, -1, -1)
    assert jim.x == jim.y == jim.taille
    control.gerer_fleches(jim, -1, 0)
    control.gerer_fleches(jim, 0, -1)
    assert jim.x == jim.y == jim.taille
    control.gerer_fleches(jim, 1, 1)
    assert jim.x == jim.y == jim.taille + jim.vitesse / math.sqrt(2)
    temp = jim.y
    control.gerer_fleches(jim, 0, 1)
    assert jim.y == temp + jim.vitesse


def test_mouvement():
    jack = Joueur(0, 0)
    jack.bouger_fleche(2, 8, 10)
    assert jack.x == 20
    assert jack.y == 80
