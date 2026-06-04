import pygame
pygame.init()

# Paramètres de l'écran
info = pygame.display.Info()
largeur = info.current_w
hauteur = info.current_h
size = largeur, hauteur
couleur_fond = (227, 255, 80)
couleur_joueur = (24, 57, 125)
screen = pygame.display.set_mode(size)
FPS = 60
Couleur_fond = (30, 30, 30)
