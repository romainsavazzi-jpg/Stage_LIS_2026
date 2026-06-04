import pygame
from configuration import couleur_fond, couleur_joueur, touches
from Modele import modele  # Obstacle_rect, Joueur


class Vue:
    def __init__(self, largeur, hauteur, FPS=60):
        self.controleur = None
        self.objets_jeu = None
        self.etat = True
        self.FPS = FPS

        pygame.init()
        self.screen = pygame.display.set_mode((largeur, hauteur))
        self.clock = pygame.time.Clock()

    def attacher_modele(self, modele):
        self.objets_jeu = modele

    def attacher_controleur(self, controleur):
        self.controleur = controleur

    def run(self):
        while self.etat:
            self.gerer_evenement()
            self.gerer_entrees()
            self.boucle_principale()
            self.dessiner()
            self.clock.tick(self.FPS)

    def boucle_principale(self):
        self.controleur.deplacer_vers_cible()

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
        touches_pressees = pygame.key.get_pressed()
        if touches_pressees[touches["quitter"]] == 1:
            self.etat = False
        if touches_pressees[touches["agrandir"]] == 1:
            self.joueur.change_taille(0.5)
        if touches_pressees[touches["retrecir"]] == 1:
            self.joueur.change_taille(-0.5)
        if touches_pressees[touches["aug_vitesse"]] == 1:
            self.joueur.change_vitesse(0.3)
        if touches_pressees[touches["red_vitesse"]] == 1:
            self.joueur.change_vitesse(-0.3)
        dx = touches_pressees[touches["droite"]] - touches_pressees[touches["gauche"]]
        dy = touches_pressees[touches["bas"]] - touches_pressees[touches["haut"]]
        self.controleur.gerer_deplacement(self.joueur, dx, dy)

    def dessiner(self):
        # Dessin : récupère les données du modèle
        self.screen.fill(couleur_fond)

        for joueur in self.objets_jeu.liste_joueurs:
            if isinstance(joueur, modele.Joueur):
                pygame.draw.circle(
                    self.screen,
                    couleur_joueur,
                    (int(joueur.x), int(joueur.y)),
                    joueur.taille,
                )

        for obj in self.objets_jeu.liste_obstacles:
            if isinstance(obj, modele.Obstacle_rect):
                pygame.draw.rect(
                    self.screen, obj.couleur, (obj.x, obj.y, obj.largeur, obj.hauteur)
                )

        pygame.display.flip()
