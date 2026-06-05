from Modele import modele  # Joueur, Objet_jeu, Obstacle_rect
from Controleur import controleur  # Controleur
from Vue import vue  # Vue
from configuration import largeur, hauteur, nbr_rect
import random


# créer un joueur au centre de l'écran
joueur = modele.Joueur(largeur // 2, hauteur // 2)

# créer une grille et la diviser
grille1 = modele.Grille(50)
grille1.diviser_ecran()

# ajoute la grille et le joueur au modèle
objets_jeu = modele.Objets_jeu()
objets_jeu.ajouter_joueur(joueur)
objets_jeu.ajouter_grille(grille1)


# créer des obstacles et les ajoute au modèle
for i in range(nbr_rect):
    objets_jeu.ajouter_obstacle(
        modele.Obstacle_rect(
            x=random.randint(0, largeur - 100),
            y=random.randint(0, hauteur - 100),
            largeur=random.randint(50, 100),
            hauteur=random.randint(50, 200),
        ),
    )

# créer un controleur et l'attacher au modèle
controleur1 = controleur.Controleur()
controleur1.attacher_modele(objets_jeu)

# créer une vue et lui attacher le modèle et le contrôleur
vue1 = vue.Vue(largeur, hauteur)
vue1.attacher_modele(objets_jeu)
vue1.attacher_controleur(controleur1)

# lancer la boucle
vue1.run()
