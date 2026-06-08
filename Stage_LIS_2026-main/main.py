from Modele import modele  # Joueur, Objet_jeu, Obstacle_rect
from Controleur import controleur  # Controleur
from Vue import vue  # Vue
from Configuration import configuration
import random

# créer un joueur au centre de l'écran
joueur = modele.Joueur(configuration.largeur // 2, configuration.hauteur // 2)

# créer une grille et la diviser
grille1 = modele.Grille(configuration.divisions)
grille1.diviser_ecran()

# ajoute la grille et le joueur au modèle
objets_jeu = modele.Objets_jeu()
objets_jeu.ajouter_joueur(joueur)
objets_jeu.ajouter_grille(grille1)
# créer un controleur et lui attacher le modèle
controleur1 = controleur.Controleur()
controleur1.attacher_modele(objets_jeu)
# ajouter le controleur au modèle
# objets_jeu.attacher_controleur(controleur1)

# créer des obstacles et les ajoute au modèle
for i in range(configuration.nbr_rect):
    objets_jeu.ajouter_obstacle(
        modele.Obstacle_rect(
            x=random.randint(0, configuration.largeur - 100),
            y=random.randint(0, configuration.hauteur - 100),
            largeur=random.randint(50, 100),
            hauteur=random.randint(50, 200),
        ),
    )


# créer une vue et lui attacher le modèle et le contrôleur
vue1 = vue.Vue(configuration.largeur, configuration.hauteur)
vue1.attacher_modele(objets_jeu)
vue1.attacher_controleur(controleur1)

# lancer la boucle
vue1.run()
