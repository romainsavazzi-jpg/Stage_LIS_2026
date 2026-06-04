from Modele import modele  # Joueur, Objet_jeu, Obstacle_rect
from Controleur import controleur  # Controleur
from Vue import vue  # Vue
from configuration import largeur, hauteur, FPS
import random


# Instanciation dans le bon ordre
joueur = modele.Joueur(largeur // 2, hauteur // 2)
objets_jeu = modele.Objets_jeu()
objets_jeu.ajouter_joueur(joueur)
for i in range(80):
    objets_jeu.ajouter_obstacle(
        modele.Obstacle_rect(
            x=random.randint(0, largeur - 100),
            y=random.randint(0, hauteur - 100),
            largeur=random.randint(50, 100),
            hauteur=random.randint(50, 100),
            couleur=(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            ),
        )
    )
controleur1 = controleur.Controleur()
controleur1.attacher_modele(objets_jeu)

grille1 = modele.Grille(100)
grille1.diviser_ecran()

vue1 = vue.Vue(largeur, hauteur, FPS)
vue1.attacher_modele(objets_jeu)
vue1.attacher_controleur(controleur1)
vue1.attacher_grille(grille1)

vue1.run()
