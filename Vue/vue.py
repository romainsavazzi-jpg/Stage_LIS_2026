import pygame
from configuration import couleur_fond, couleur_joueur, touches, FPS
from Modele import modele  # Obstacle_rect, Joueur


class Vue:
    def __init__(self, largeur: int, hauteur: int, FPS=FPS):
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
        """Fait tourner une boucle qui gère toute la vue"""
        while self.etat:
            self.gerer_evenement()
            self.gerer_entrees()
            self.boucle_principale()
            self.dessiner()
            self.clock.tick(self.FPS)

    def boucle_principale(self):
        """boucle principale qui permet de faire tourner les fonctions du contrôle qui nécessite une maj à chaque frame"""
        self.controleur.deplacer_vers_cible()
        self.controleur.se_rendre_aux_points()

    def gerer_evenement(self):
        """Regarde les évènements pygame et agit en conséquence"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.etat = False
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     couleur_clic = self.screen.get_at(event.pos)[:3]
            #     if couleur_clic == (24, 57, 125):
            #         pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.controleur.traj = True

                    mx, my = pygame.mouse.get_pos()
                    self.controleur.cible_souris = mx, my
                    point_arrivee, _, _ = self.controleur.selection_point(mx, my)
                    self.controleur.determiner_chemin(point_arrivee)

                    # (mx_point_arrivee, my_point_arrivee) = self.controleur.selection_point(mx, my)
                    # self.controleur.allumer_points((mx_point_arrivee, my_point_arrivee))
                elif event.button == 1 and self.controleur.traj and self.controleur.cible_souris:
                    self.controleur.aller_vers_point = True
                    # self.controleur.selection_point_cible(self.controleur.cible_souris[0], self.controleur.cible_souris[1])
                    self.controleur.traj = False

                    # self.controleur.cible_souris = mx, my

            if event.type == pygame.KEYDOWN:
                if event.key == touches["agrandir_un_peu"]:
                    self.objets_jeu.liste_joueurs[0].change_taille(1)
                if event.key == touches["retrecir_un_peu"]:
                    self.objets_jeu.liste_joueurs[0].change_taille(-1)
                if event.key == touches["aug_vitesse_un_peu"]:
                    self.objets_jeu.liste_joueurs[0].change_vitesse(1)
                if event.key == touches["red_vitesse_un_peu"]:
                    self.objets_jeu.liste_joueurs[0].change_vitesse(-1)

    def gerer_entrees(self):
        """Gère les entrées du clavier pour le déplacement du joueur et les autres actions liées au clavier"""
        touches_pressees = pygame.key.get_pressed()
        if touches_pressees[touches["quitter"]] == 1:
            self.etat = False
        if touches_pressees[touches["agrandir"]] == 1:
            self.objets_jeu.liste_joueurs[0].change_taille(0.5)
        if touches_pressees[touches["retrecir"]] == 1:
            self.objets_jeu.liste_joueurs[0].change_taille(-0.5)
        if touches_pressees[touches["aug_vitesse"]] == 1:
            self.objets_jeu.liste_joueurs[0].change_vitesse(0.3)
        if touches_pressees[touches["red_vitesse"]] == 1:
            self.objets_jeu.liste_joueurs[0].change_vitesse(-0.3)
        dx = touches_pressees[touches["droite"]] - touches_pressees[touches["gauche"]]
        dy = touches_pressees[touches["bas"]] - touches_pressees[touches["haut"]]
        self.controleur.gerer_deplacement_touches(dx, dy)

    def dessiner(self):
        """Dessine tous les éléments du jeu à partir des données du modèle"""
        # dessine le fond
        self.screen.fill(couleur_fond)

        # dessine les joueurs
        for joueur in self.objets_jeu.liste_joueurs:
            if isinstance(joueur, modele.Joueur):
                pygame.draw.circle(
                    self.screen,
                    couleur_joueur,
                    (int(joueur.x), int(joueur.y)),
                    joueur.taille,
                )

        # dessine les obstacles
        for obj in self.objets_jeu.liste_obstacles:
            if isinstance(obj, modele.Obstacle_rect):
                pygame.draw.rect(
                    self.screen, obj.couleur, (obj.x, obj.y, obj.largeur, obj.hauteur)
                )

        # dessine les points de la grille
        for ligne in self.objets_jeu.grille.grille:
            for point_grille in ligne:
                if isinstance(point_grille, modele.Point):
                    pygame.draw.circle(
                        self.screen,
                        point_grille.couleur,
                        (point_grille.x, point_grille.y),
                        400 / self.objets_jeu.grille.nbr_division,
                    )

        pygame.display.flip()
