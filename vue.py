import pygame
from configuration import FPS, largeur, hauteur, couleur_fond, couleur_joueur


class Vue:
    def __init__(self, joueur, controleur):
        self.joueur = joueur
        self.controleur = controleur
        self.etat = True

        pygame.init()
        self.screen = pygame.display.set_mode((largeur, hauteur))
        self.clock = pygame.time.Clock()

    def run(self):
        while self.etat:
            self.gerer_evenement()
            self.gerer_entrees()
            self.dessiner()
            self.clock.tick(FPS)

    def gerer_evenement(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.etat = False

    def gerer_entrees(self):
        touches = pygame.key.get_pressed()
        if touches[pygame.K_ESCAPE] == 1:
            self.etat = False
        dx = (touches[pygame.K_RIGHT] - touches[pygame.K_LEFT])
        dy = (touches[pygame.K_DOWN] - touches[pygame.K_UP])
        self.controleur.gerer_fleches(self.joueur, dx, dy)

    def dessiner(self):
        # Dessin : récupère les données du modèle
        self.screen.fill(couleur_fond)
        pygame.draw.circle(self.screen, couleur_joueur,
                           (int(self.joueur.x), int(self.joueur.y)), self.joueur.taille)
        pygame.display.flip()
