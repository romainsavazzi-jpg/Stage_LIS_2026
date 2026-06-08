import pygame
import tomllib
import os

pygame.init()

# importe le toml
with open(os.path.join(os.path.dirname(__file__), "données.toml"), "rb") as f:
    tom = tomllib.load(f)

info = pygame.display.Info()

# vérifie si le plein écran est activé et définit la taille de l'écran en conséquence
if tom["ecran"]["plein_ecran"]:
    largeur = info.current_w
    hauteur = info.current_h
else:
    largeur = tom["ecran"]["largeur_fixe"]
    hauteur = tom["ecran"]["hauteur_fixe"]

size = largeur, hauteur
screen = pygame.display.set_mode(size)

FPS = tom["ecran"]["fps"]

# Couleurs
couleur_fond = tuple(tom["couleurs"]["fond"])
couleur_joueur = tuple(tom["couleurs"]["joueur"])
couleur_point = tuple(tom["couleurs"]["points"])
couleur_rectangle = tuple(tom["couleurs"]["rectangle"])
couleur_point_intravesable = tuple(tom["couleurs"]["intraversable"])

# Joueur
vitesse = tom["joueur"]["vitesse"]
taille = tom["joueur"]["taille"]

# Touches — on résout les getattr ici une bonne fois pour toutes
touches = {nom: getattr(pygame, val) for nom, val in tom["touches"].items()}

# Grille
divisions = tom["grille"]["divisions"]

# Obstacles
nbr_rect = tom["obstacles"]["nombre_rectangles"]
