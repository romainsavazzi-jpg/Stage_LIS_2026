from modele import Joueur
from controleur import Controleur
import math


def test_mouvement_bord():
    jim = Joueur(0, 0)
    control = Controleur()
    control.gerer_deplacement(jim, -1, -1)
    assert jim.x == jim.y == jim.taille
    control.gerer_deplacement(jim, -1, 0)
    control.gerer_deplacement(jim, 0, -1)
    assert jim.x == jim.y == jim.taille
    control.gerer_deplacement(jim, 1, 1)
    assert jim.x == jim.y == jim.taille + jim.vitesse / math.sqrt(2)
    temp = jim.y
    control.gerer_deplacement(jim, 0, 1)
    assert jim.y == temp + jim.vitesse


def test_mouvement():
    jack = Joueur(0, 0)
    jack.bouger_fleche(2, 8, 10)
    assert jack.x == 20
    assert jack.y == 80


def test_mouvement_click_souris():
    john = Joueur(0, 0)
    controle = Controleur()
    coordonnees = 200
    controle.cible_souris = (coordonnees, coordonnees)
    while controle.cible_souris is not None:
        controle.deplacer_vers_cible(john)
    print(john.x)
    assert john.x > coordonnees - (john.vitesse // 2 + 1) and john.x < coordonnees + (john.vitesse // 2 + 1)
    assert john.y > coordonnees - (john.vitesse // 2 + 1) and john.y < coordonnees + (john.vitesse // 2 + 1)
