import pygame
pygame.init()

# Paramètres de l'écran
info = pygame.display.Info()
largeur = info.current_w
hauteur = info.current_h
size = largeur, hauteur
screen = pygame.display.set_mode(size) 
FPS = 60

vitesse_joueur = 4
Taille_joueur = 16
Couleur_joueur = (80, 140, 255)
Couleur_fond = (30, 30, 30)
