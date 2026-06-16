from modele import Joueur, Objets_jeu, Obstacle_rect, Obstacle_cercle, Grille
from controleur import Controleur  # Controleur
from vue import Vue  # Vue
from Configuration import configuration
import random

# créer un joueur au centre de l'écran
joueur = Joueur(configuration.largeur // 2, configuration.hauteur // 2)

# créer une grille et la diviser
grille1 = Grille(configuration.divisions)
grille1.diviser_ecran()

# ajoute la grille et le joueur au modèle
objets_jeu = Objets_jeu()
objets_jeu.ajouter_joueur(joueur)
objets_jeu.ajouter_grille(grille1)

# créer un controleur et lui attacher le modèle
controleur1 = Controleur()
controleur1.attacher_modele(objets_jeu)

# créer des obstacles et les ajoute au modèle
for i in range(configuration.nbr_rect):
    objets_jeu.ajouter_obstacle(
        Obstacle_rect(
            x=random.randint(0, configuration.largeur),
            y=random.randint(0, configuration.hauteur),
            largeur=random.randint(5, 20),
            hauteur=random.randint(5, 40),
        ),
    )

for i in range(configuration.nbr_cercles):
    objets_jeu.ajouter_obstacle(
        Obstacle_cercle(
            x=random.randint(0, configuration.largeur),
            y=random.randint(0, configuration.hauteur),
            taille=random.randint(5, 20),
        ),
    )


# créer une vue et lui attacher le modèle et le contrôleur
vue1 = Vue(configuration.largeur, configuration.hauteur)
vue1.attacher_modele(objets_jeu)
vue1.attacher_controleur(controleur1)

# lancer la boucleq
vue1.run()
