from controleur import Controleur
from modele import Joueur, Objets_jeu, Grille, Point
import math


def test_mouvement_bord():
    """Test les fonctions de déplacement du joueur et vérifie que les limites de l'écran sont respectées"""
    jim = Joueur(0, 0)
    control = Controleur()
    modele = Objets_jeu()
    modele.ajouter_joueur(jim)
    control.attacher_modele(modele)
    control.gerer_deplacement_touches(-1, -1)
    assert jim.x == jim.y == jim.taille
    control.gerer_deplacement_touches(-1, 0)
    control.gerer_deplacement_touches(0, -1)
    assert jim.x == jim.y == jim.taille
    control.gerer_deplacement_touches(1, 1)
    assert jim.x == jim.y == jim.taille + jim.vitesse / math.sqrt(2)
    temp = jim.y
    control.gerer_deplacement_touches(0, 1)
    assert jim.y == temp + jim.vitesse


def test_selection_point_cible_et_mouvement():
    """Test la fonction de déplacement avec le clic souris"""
    john = Joueur(0, 0)
    controleur = Controleur()
    model = Objets_jeu()
    grille1 = Grille(150)
    grille1.diviser_ecran()
    model.ajouter_grille(grille1)
    model.ajouter_joueur(john)
    controleur.attacher_modele(model)
    coordonnees = 200
    point, _, _ = controleur.selection_point(coordonnees, coordonnees)
    controleur.selection_point_cible(point)
    while controleur.point_cible is not None:
        controleur.deplacer_vers_cible()
    assert john.x > coordonnees - (john.vitesse // 2 + 1) and john.x < coordonnees + (john.vitesse // 2 + 1)
    assert john.y > coordonnees - (john.vitesse // 2 + 1) and john.y < coordonnees + (john.vitesse // 2 + 1)


def test_deplacer_vers_cible():
    """Test la fonction de déplacement avec le clic souris"""
    john = Joueur(0, 0)
    controleur = Controleur()
    model = Objets_jeu()
    model.ajouter_joueur(john)
    controleur.attacher_modele(model)
    coordonnees = 200
    controleur.point_cible = Point(coordonnees, coordonnees)
    while controleur.point_cible is not None:
        controleur.deplacer_vers_cible()
    assert john.x > coordonnees - (john.vitesse // 2 + 1) and john.x < coordonnees + (john.vitesse // 2 + 1)
    assert john.y > coordonnees - (john.vitesse // 2 + 1) and john.y < coordonnees + (john.vitesse // 2 + 1)
