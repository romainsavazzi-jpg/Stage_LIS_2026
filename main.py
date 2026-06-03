from Modele import modele  # Joueur, Carte, Obstacle_rect
from Controleur import controleur  # Controleur
from Vue import vue  # Vue
from configuration import largeur, hauteur
import random


# Instanciation dans le bon ordre
joueur = modele.Joueur(largeur // 2, hauteur // 2)
controleur = controleur.Controleur()

carte = modele.Carte()
carte.ajouter(joueur)
for i in range(80):
    carte.ajouter(
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
vue = vue.Vue(joueur, controleur, carte)

vue.run()
