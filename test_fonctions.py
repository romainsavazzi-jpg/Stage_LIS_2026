from modele import Joueur, Objets_jeu, Obstacle_rect  # Joueur
from controleur import Controleur  # Controleur
import math


def test_mouvement_bord():
    """Test les fonctions de déplacement du joueur et vérifie que les limites de l'écran sont respectées"""
    jim = Joueur(0, 0)
    control = Controleur()
    model = Objets_jeu()
    model.ajouter_joueur(jim)
    control.attacher_modele(model)
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


def test_mouvement():
    """Test les fonctions de déplacement du joueur"""
    jack = Joueur(0, 0)
    jack.bouger(2, 8, 10)
    assert jack.x == 20
    assert jack.y == 80


def test_mouvement_click_souris():
    """Test la fonction de déplacement avec le clic souris"""
    john = Joueur(0, 0)
    controle = Controleur()
    model = Objets_jeu()
    model.ajouter_joueur(john)
    controle.attacher_modele(model)
    coordonnees = 200
    controle.cible_souris = (coordonnees, coordonnees)
    while controle.cible_souris is not None:
        controle.deplacer_vers_cible()
    print(john.x)
    assert john.x > coordonnees - (john.vitesse // 2 + 1) and john.x < coordonnees + (
        john.vitesse // 2 + 1
    )
    assert john.y > coordonnees - (john.vitesse // 2 + 1) and john.y < coordonnees + (
        john.vitesse // 2 + 1
    )


def test_ajout_objet():
    """Test les fonctions d'ajout d'objets au modèle et de récupération d'un joueur"""
    Liste_objet = Objets_jeu()
    jimmy = Joueur(0, 0)
    kouign_amann = Obstacle_rect()
    Liste_objet.ajouter_joueur(jimmy)
    Liste_objet.ajouter_obstacle(kouign_amann)
    assert Liste_objet.liste_joueurs[0] == jimmy
    assert Liste_objet.liste_obstacles[0] == kouign_amann


def test_recup_joueur():
    johnny = Joueur(0, 0)
    cave = Objets_jeu()
    cave.ajouter_joueur(johnny)
    cave.ajouter_joueur(johnny)
    kidnappé = cave.get_joueur(1)
    assert kidnappé == johnny
