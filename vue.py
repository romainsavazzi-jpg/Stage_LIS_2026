import pygame
from configuration import FPS, largeur, hauteur, couleur_fond, couleur_joueur
from modele import Obstacle_rect, Joueur


class Vue:
    def __init__(self, joueur, controleur, carte):
        self.joueur = joueur
        self.controleur = controleur
        self.etat = True
        self.carte = carte

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
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     couleur_clic = self.screen.get_at(event.pos)[:3]
            #     if couleur_clic == (24, 57, 125):
            #         pygame.quit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     x = event.pos[0]
            #     y = event.pos[1]
            #     self.controleur.gerer_click(self.joueur, x, y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                self.controleur.deplacer(self.joueur, mx, my)

    def gerer_entrees(self):
        touches = pygame.key.get_pressed()
        if touches[pygame.K_ESCAPE] == 1:
            self.etat = False
        dx = touches[pygame.K_RIGHT] - touches[pygame.K_LEFT]
        dy = touches[pygame.K_DOWN] - touches[pygame.K_UP]
        self.controleur.gerer_fleches(self.joueur, dx, dy)

    def dessiner(self):
        # Dessin : récupère les données du modèle
        self.screen.fill(couleur_fond)

        for obj in self.carte.liste:
            if isinstance(obj, Obstacle_rect):
                pygame.draw.rect(
                    self.screen, obj.couleur, (obj.x, obj.y, obj.largeur, obj.hauteur)
                )

            if isinstance(obj, Joueur):
                pygame.draw.circle(
                    self.screen,
                    couleur_joueur,
                    (int(self.joueur.x), int(self.joueur.y)),
                    self.joueur.taille,
                )

        pygame.display.flip()
