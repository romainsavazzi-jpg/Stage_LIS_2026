from modele import Joueur, Jeu, Obstacle_rect, Grille, Point
from controleur import Controleur
from Utilities import Bresenham, Algo_A_etoile
import math

# TESTS MODELE
# Tests classe Jeu


def test_ajout_objet():
    """Test les fonctions d'ajout d'objets au modèle et de récupération d'un joueur"""
    Liste_objet = Jeu()
    jimmy = Joueur(0, 0)
    kouign_amann = Obstacle_rect(10, 10, 20, 20)
    grille = Grille()
    Liste_objet.ajouter_grille(grille)
    Liste_objet.ajouter_joueur(jimmy)
    Liste_objet.ajouter_obstacle(kouign_amann)
    assert Liste_objet.liste_joueurs[0] == jimmy
    assert Liste_objet.liste_obstacles[0] == kouign_amann
    assert Liste_objet.grille == grille


def test_recup_joueur():
    johnny = Joueur(0, 0)
    cave = Jeu()
    cave.ajouter_joueur(johnny)
    cave.ajouter_joueur(johnny)
    kidnappé = cave.get_joueur(1)
    assert kidnappé == johnny

# Tests classe Joueur


def test_tp_bord():
    Joey = Joueur(0, 0)
    Joey.tp_bord(2, "vertical")
    Joey.tp_bord(2, "horizontal")
    assert Joey.y == 2
    assert Joey.x == 2


def test_paramètres_joueurs():
    Joel = Joueur(0, 0)
    Joel.change_taille(10)
    Joel.change_vitesse(10)
    assert Joel.taille == 50
    assert Joel.vitesse == 17.5


def test_mouvement():
    """Test les fonctions de déplacement du joueur"""
    jack = Joueur(0, 0)
    jack.bouger(2, 8, 10)
    assert jack.x == 20
    assert jack.y == 80


# Tests classe points

def test_comparaisons_points():
    assert Point(2, 5) == Point(2, 5)
    assert not Point(2, 5) == Point(15, 67)


def test_hashage_points():
    coccinelle = Point(0, 7)
    scarabée = Point(0, 1)
    chapeau = coccinelle.__hash__
    couvre_chef = coccinelle.__hash__
    casquette = scarabée.__hash__
    assert chapeau == couvre_chef
    assert casquette != chapeau


def test_ecriture_points():
    assert str(Point(6, 7)) == "6 7 True"

# Tests classe Grille 


def test_mouvement_bord():
    """Test les fonctions de déplacement du joueur et vérifie que les limites de l'écran sont respectées"""
    jim = Joueur(0, 0)
    control = Controleur()
    modele = Jeu()
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





# def test_mouvement_click_souris():
#     """Test la fonction de déplacement avec le clic souris"""
#     john = Joueur(0, 0)
#     controle = Controleur()
#     model = Jeu()
#     model.ajouter_joueur(john)
#     controle.attacher_modele(model)
#     coordonnees = 200
#     controle.point_cible = (coordonnees, coordonnees)
#     while controle.point_cible is not None:
#         controle.deplacer_vers_cible()
#     assert john.x > coordonnees - (john.vitesse // 2 + 1) and john.x < coordonnees + (
#         john.vitesse // 2 + 1
#     )
#     assert john.y > coordonnees - (john.vitesse // 2 + 1) and john.y < coordonnees + (
#         john.vitesse // 2 + 1
#     )







def test_bresenham_dans_tout_les_sens():
    assert Bresenham.bresenham((0, 0), (4, 0)) == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]  # vers la droite
    assert Bresenham.bresenham((4, 0), (0, 0)) == [(4, 0), (3, 0), (2, 0), (1, 0), (0, 0)]  # vers la gauche
    assert Bresenham.bresenham((0, 0), (0, 4)) == [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]  # vers le haut
    assert Bresenham.bresenham((0, 4), (0, 0)) == [(0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]  # vers le bas
    assert Bresenham.bresenham((0, 0), (3, 3)) == [(0, 0), (1, 1), (2, 2), (3, 3)]  # diagonale



