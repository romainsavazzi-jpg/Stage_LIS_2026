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
    assert point == controleur.modele.grille.grille[coordonnee_grille_y][coordonnee_grille_x]
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


def test_attacher_modele():
    ceinture = Objets_jeu()
    adrien = Controleur()
    adrien.attacher_modele(ceinture)
    assert adrien.modele == ceinture


def test_changer_taille():
    barbableu = Joueur(0, 0, configuration.couleur_joueur, configuration.vitesse, 1.5)
    latour = Objets_jeu()
    latour.ajouter_joueur(barbableu)
    controleur = Controleur()
    controleur.attacher_modele(latour)
    grille = Grille(150)
    grille.diviser_ecran()
    latour.ajouter_grille(grille)
    point = controleur.modele.grille.grille[0][0]
    assert point.traversable
    controleur.changer_taille(1)
    assert barbableu.taille == 2.5
    assert not point.traversable


def test_lancer_chemin():
    barbableu = Joueur(0, 0, configuration.couleur_joueur, configuration.vitesse, 1.5)
    latour = Objets_jeu()
    latour.ajouter_joueur(barbableu)
    controleur = Controleur()
    controleur.attacher_modele(latour)
    grille = Grille(150)
    grille.diviser_ecran()
    latour.ajouter_grille(grille) 
    controleur.lancer_chemin(2, 2)
    point_arrivee, _, _ = controleur.selection_point(2, 2)
    assert controleur.traj
    assert controleur.liste_points_d_accroche == [point_arrivee]
    # tester l'appel de l'autre fonction


def test_actualiser_deplacement_points_d_accroche():
    barbableu = Joueur(0, 0, configuration.couleur_joueur, configuration.vitesse, 1.5)
    latour = Objets_jeu()
    latour.ajouter_joueur(barbableu)
    controleur = Controleur()
    controleur.attacher_modele(latour)
    grille = Grille(150)
    grille.diviser_ecran()
    latour.ajouter_grille(grille) 
    point1, _, _ = controleur.selection_point(2, 2)
    point1.traversable = True
    controleur.actualiser_deplacement_point_d_accroche(2, 2)
    assert controleur.liste_points_d_accroche[0] == point1
    assert controleur.bon_point_d_accroche == point1
    point2, _, _ = controleur.selection_point(3, 3)
    point2.traversable = False
    controleur.actualiser_deplacement_point_d_accroche(3, 3)
    assert controleur.bon_point_d_accroche == point1
    assert controleur.liste_points_d_accroche[0] == point1

