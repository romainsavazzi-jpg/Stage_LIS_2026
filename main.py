from modele import Joueur, Carte, Obstacle_rect
from controleur import Controleur
from vue import Vue
from configuration import largeur, hauteur
import random

# Instanciation dans le bon ordre
joueur = Joueur(largeur // 2, hauteur // 2)
controleur = Controleur()
carte = Carte()
carte.ajouter(joueur)
for i in range(80):
    carte.ajouter(
        Obstacle_rect(
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
vue = Vue(joueur, controleur, carte)

vue.run()

