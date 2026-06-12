from controleur import Controleur
from modele import Joueur, Objets_jeu
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
