import pygame
from configuration import FPS, largeur, hauteur, couleur_fond, couleur_joueur
from Modele import modele  # Obstacle_rect, Joueur


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
            self.boucle_principale()
            self.dessiner()
            self.clock.tick(FPS)

    def boucle_principale(self):
        self.controleur.deplacer_vers_cible(self.joueur)

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
                self.controleur.cible_souris = mx, my
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    self.joueur.change_taille(1)
                if event.key == pygame.K_y:
                    self.joueur.change_taille(-1)
                if event.key == pygame.K_n:
                    self.joueur.change_vitesse(1)
                if event.key == pygame.K_b:
                    self.joueur.change_vitesse(-1)

    def gerer_entrees(self):
        touches = pygame.key.get_pressed()
        if touches[pygame.K_ESCAPE] == 1:
            self.etat = False
        if touches[pygame.K_t] == 1:
            self.joueur.change_taille(0.5)
        if touches[pygame.K_r] == 1:
            self.joueur.change_taille(-0.5)
        if touches[pygame.K_v] == 1:
            self.joueur.change_vitesse(0.3)
        if touches[pygame.K_c] == 1:
            self.joueur.change_vitesse(-0.3)
        dx = touches[pygame.K_RIGHT] - touches[pygame.K_LEFT]
        dy = touches[pygame.K_DOWN] - touches[pygame.K_UP]
        self.controleur.gerer_deplacement(self.joueur, dx, dy)

    def dessiner(self):
        # Dessin : récupère les données du modèle
        self.screen.fill(couleur_fond)

        for obj in self.carte.liste:
            if isinstance(obj, modele.Obstacle_rect):
                pygame.draw.rect(
                    self.screen, obj.couleur, (obj.x, obj.y, obj.largeur, obj.hauteur)
                )

            if isinstance(obj, modele.Joueur):
                pygame.draw.circle(
                    self.screen,
                    couleur_joueur,
                    (int(self.joueur.x), int(self.joueur.y)),
                    self.joueur.taille,
                )

        pygame.display.flip()
