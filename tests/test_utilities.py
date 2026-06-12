from Utilities import Bresenham, Algo_A_etoile
from modele import Joueur, Objets_jeu, Grille, Point
from controleur import Controleur


def test_bresenham_dans_tout_les_sens():
    assert Bresenham.bresenham((0, 0), (4, 0)) == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]  # vers la droite
    assert Bresenham.bresenham((4, 0), (0, 0)) == [(4, 0), (3, 0), (2, 0), (1, 0), (0, 0)]  # vers la gauche
    assert Bresenham.bresenham((0, 0), (0, 4)) == [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]  # vers le haut
    assert Bresenham.bresenham((0, 4), (0, 0)) == [(0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]  # vers le bas
    assert Bresenham.bresenham((0, 0), (3, 3)) == [(0, 0), (1, 1), (2, 2), (3, 3)]  # diagonale


def test_A_etoile():
    # Dans cette grille, du point Point(1, 4, True) à Point(8, 4, True), il y a plusieurs chemins et le plus optimal est en passant par le bas
    grille_de_test = [
        [Point(0, 0, True), Point(1, 0, True), Point(2, 0, True), Point(3, 0, True), Point(4, 0, True), Point(5, 0, True), Point(6, 0, True), Point(7, 0, True), Point(8, 0, True), Point(9, 0, True)],
        [Point(0, 1, True), Point(1, 1, True), Point(2, 1, True), Point(3, 1, False), Point(4, 1, True), Point(5, 1, True), Point(6, 1, True), Point(7, 1, True), Point(8, 1, True), Point(9, 1, True)],
        [Point(0, 2, True), Point(1, 2, True), Point(2, 2, True), Point(3, 2, False), Point(4, 2, False), Point(5, 2, True), Point(6, 2, True), Point(7, 2, True), Point(8, 2, True), Point(9, 2, True)],
        [Point(0, 3, True), Point(1, 3, True), Point(2, 3, True), Point(3, 3, True), Point(4, 3, False), Point(5, 3, False), Point(6, 3, True), Point(7, 3, True), Point(8, 3, True), Point(9, 3, True)],
        [Point(0, 4, True), Point(1, 4, True), Point(2, 4, True), Point(3, 4, True), Point(4, 4, True), Point(5, 4, False), Point(6, 4, False), Point(7, 4, True), Point(8, 4, True), Point(9, 4, True)],
        [Point(0, 5, True), Point(1, 5, True), Point(2, 5, True), Point(3, 5, True), Point(4, 5, False), Point(5, 5, False), Point(6, 5, True), Point(7, 5, True), Point(8, 5, True), Point(9, 5, True)],
        [Point(0, 6, True), Point(1, 6, True), Point(2, 6, True), Point(3, 6, False), Point(4, 6, False), Point(5, 6, True), Point(6, 6, True), Point(7, 6, True), Point(8, 6, True), Point(9, 6, True)],
        [Point(0, 7, True), Point(1, 7, True), Point(2, 7, True), Point(3, 7, True), Point(4, 7, True), Point(5, 7, True), Point(6, 7, True), Point(7, 7, True), Point(8, 7, True), Point(9, 7, True)],
        [Point(0, 7, True), Point(1, 8, True), Point(2, 8, True), Point(3, 8, True), Point(4, 8, True), Point(5, 8, True), Point(6, 8, True), Point(7, 8, True), Point(8, 8, True), Point(9, 8, True)],
        [Point(0, 7, True), Point(1, 9, True), Point(2, 9, True), Point(3, 9, True), Point(4, 9, True), Point(5, 9, True), Point(6, 9, True), Point(7, 9, True), Point(8, 9, True), Point(9, 9, True)],
    ]
    jacky = Joueur(0, 0)
    controleur = Controleur()
    modele = Objets_jeu()
    grille1 = Grille()
    modele.ajouter_grille(grille1)
    modele.ajouter_joueur(jacky)
    controleur.attacher_modele(modele)
    controleur.objets_jeu.grille.grille = grille_de_test

    controleur.objets_jeu.grille.ecart = 1

    liste_points, liste_des_points_verifies = Algo_A_etoile.cheminPlusCourt(controleur, grille_de_test, Point(1, 4, True), Point(8, 4, True))
    vraie_liste_points = [Point(2, 5), Point(2, 6), Point(3, 7), Point(4, 7), Point(5, 6), Point(6, 5), Point(7, 5), Point(8, 4)]
    assert liste_points == vraie_liste_points

    # Dans cette grille, du point Point(1, 4, True) à Point(8, 4, True), il n'y a pas de chemin donc l'algorithme devrait rendre une liste vide
    grille_de_test = [
        [Point(0, 0, True), Point(1, 0, True), Point(2, 0, True), Point(3, 0, False), Point(4, 0, True), Point(5, 0, True), Point(6, 0, True), Point(7, 0, True), Point(8, 0, True), Point(9, 0, True)],
        [Point(0, 1, True), Point(1, 1, True), Point(2, 1, True), Point(3, 1, False), Point(4, 1, True), Point(5, 1, True), Point(6, 1, True), Point(7, 1, True), Point(8, 1, True), Point(9, 1, True)],
        [Point(0, 2, True), Point(1, 2, True), Point(2, 2, True), Point(3, 2, False), Point(4, 2, False), Point(5, 2, True), Point(6, 2, True), Point(7, 2, True), Point(8, 2, True), Point(9, 2, True)],
        [Point(0, 3, True), Point(1, 3, True), Point(2, 3, True), Point(3, 3, True), Point(4, 3, False), Point(5, 3, False), Point(6, 3, True), Point(7, 3, True), Point(8, 3, True), Point(9, 3, True)],
        [Point(0, 4, True), Point(1, 4, True), Point(2, 4, True), Point(3, 4, True), Point(4, 4, True), Point(5, 4, False), Point(6, 4, False), Point(7, 4, True), Point(8, 4, True), Point(9, 4, True)],
        [Point(0, 5, True), Point(1, 5, True), Point(2, 5, True), Point(3, 5, True), Point(4, 5, False), Point(5, 5, False), Point(6, 5, True), Point(7, 5, True), Point(8, 5, True), Point(9, 5, True)],
        [Point(0, 6, True), Point(1, 6, True), Point(2, 6, True), Point(3, 6, False), Point(4, 6, False), Point(5, 6, True), Point(6, 6, True), Point(7, 6, True), Point(8, 6, True), Point(9, 6, True)],
        [Point(0, 7, True), Point(1, 7, True), Point(2, 7, True), Point(3, 7, False), Point(4, 7, True), Point(5, 7, True), Point(6, 7, True), Point(7, 7, True), Point(8, 7, True), Point(9, 7, True)],
        [Point(0, 7, True), Point(1, 8, True), Point(2, 8, True), Point(3, 8, False), Point(4, 8, True), Point(5, 8, True), Point(6, 8, True), Point(7, 8, True), Point(8, 8, True), Point(9, 8, True)],
        [Point(0, 7, True), Point(1, 9, True), Point(2, 9, True), Point(3, 9, False), Point(4, 9, True), Point(5, 9, True), Point(6, 9, True), Point(7, 9, True), Point(8, 9, True), Point(9, 9, True)],
    ]

    controleur.objets_jeu.grille.grille = grille_de_test

    liste_points, liste_des_points_verifies = Algo_A_etoile.cheminPlusCourt(controleur, grille_de_test, Point(1, 4, True), Point(8, 4, True))
    assert liste_points == []


def test_determination_liste_reduite_chemin():
    liste_points = [Point(2, 5), Point(2, 6), Point(3, 7), Point(4, 7), Point(5, 6), Point(6, 5), Point(7, 5), Point(8, 4)]  # Dans cette liste, tous les points sont un changement d'angle sauf le point Point(5, 6) qu'on enlève donc de la liste de vérification
    liste_reduite = Algo_A_etoile.determination_liste_reduite_chemin(liste_points)
    vraie_liste_reduite = [Point(2, 5), Point(2, 6), Point(3, 7), Point(4, 7), Point(6, 5), Point(7, 5), Point(8, 4)]
    assert liste_reduite == vraie_liste_reduite
    liste_points = [Point(2, 5), Point(3, 5), Point(4, 5), Point(5, 5), Point(6, 5), Point(7, 5), Point(8, 5), Point(9, 5), Point(10, 5)]
    liste_reduite = Algo_A_etoile.determination_liste_reduite_chemin(liste_points)
    vraie_liste_reduite = [Point(2, 5), Point(10, 5)]
    assert liste_reduite == vraie_liste_reduite
    liste_points = []
    assert Algo_A_etoile.determination_liste_reduite_chemin(liste_points) == []
