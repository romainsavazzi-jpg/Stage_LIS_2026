from controleur import Controleur, appartient_aux_limites_de_la_map, limite_bord_et_diago
from modele import Joueur, Objets_jeu, Grille, Point
from Configuration import configuration
import math


def test_appartient_aux_limites_de_la_map():
    assert appartient_aux_limites_de_la_map(90, 200)
    assert not appartient_aux_limites_de_la_map(250, 220)
    assert not appartient_aux_limites_de_la_map(-5, 220)


def test_limite_bord_et_diago():
    jacousteau = Joueur(200, 200, vitesse=5, taille=10)
    controleur = Controleur()
    modele = Objets_jeu()
    configuration.largeur = 500
    configuration.hauteur = 500
    modele.ajouter_joueur(jacousteau)
    controleur.attacher_modele(modele)
    dx, dy, facteur = limite_bord_et_diago(jacousteau, 1, 1)
    assert facteur == jacousteau.vitesse / math.sqrt(2)
    assert dx == 1 and dy == 1
    dx, dy, facteur = limite_bord_et_diago(jacousteau, 0, 1)
    assert facteur == jacousteau.vitesse
    assert dx == 0 and dy == 1
    jacousteau = Joueur(0, 0, vitesse=5, taille=10)
    dx, dy, facteur = limite_bord_et_diago(jacousteau, -1, -1)
    assert facteur == jacousteau.vitesse / math.sqrt(2)
    assert dx == 0, dy == 0
    jacousteau = Joueur(configuration.largeur, 0, vitesse=5, taille=10)
    dx, dy, facteur = limite_bord_et_diago(jacousteau, 1, -1)
    assert facteur == jacousteau.vitesse / math.sqrt(2)
    assert dx == 0, dy == 0


def test_mouvement_bord_clavier():
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
    point, coordonnee_grille_x, coordonnee_grille_y = controleur.selection_point(coordonnees, coordonnees)
    assert point == controleur.objets_jeu.grille.grille[coordonnee_grille_y][coordonnee_grille_x]
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
