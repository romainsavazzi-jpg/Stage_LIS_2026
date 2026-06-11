import pygame
from Configuration import configuration
from modele import Joueur, Obstacle_rect, Point  # Obstacle_rect, Joueur


class Vue:
    def __init__(self, largeur: int, hauteur: int, FPS=configuration.FPS):
        self.controleur = None
        self.objets_jeu = None
        self.etat = True
        self.FPS = FPS
        self.non = True

        pygame.init()
        self.screen = pygame.display.set_mode((largeur, hauteur))
        self.clock = pygame.time.Clock()
        self.touches = {nom: getattr(pygame, val) for nom, val in configuration.touches.items()}

    def attacher_modele(self, modele):
        self.objets_jeu = modele

    def attacher_controleur(self, controleur):
        self.controleur = controleur

    def run(self):
        """Initialise et fait tourner une boucle qui gère toute la vue"""
        self.controleur.mettre_les_points_intravesables_rect(
            self.objets_jeu.liste_joueurs[0]
        )
        while self.etat:
            self.gerer_evenement()
            self.gerer_entrees()
            self.boucle_principale()
            self.dessiner()
            self.clock.tick(self.FPS)

    def boucle_principale(self):
        self.controleur.deplacer_vers_cible()
        self.controleur.se_rendre_aux_points()

    def gerer_evenement(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.etat = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.controleur.traj = True

                    self.controleur.mettre_les_points_intravesables_rect(
                        self.objets_jeu.liste_joueurs[0]
                    )

                    mx, my = pygame.mouse.get_pos()
                    point_arrivee, _, _ = self.controleur.selection_point(mx, my)
                    self.controleur.determiner_chemin(point_arrivee)

                    self.controleur.mettre_les_points_intravesables_rect(
                        self.objets_jeu.liste_joueurs[0]
                    )

                elif (
                    event.button == 1 and self.controleur.traj and self.controleur.pixel_chemin  # self.controleur.point_cible  # self.controleur.cible_souris
                ):
                    self.controleur.aller_vers_point = True
                    self.controleur.traj = False

            if event.type == pygame.KEYDOWN:
                if event.key == self.touches["afficher_points"]:
                    if self.non:
                        self.non = False
                    else:
                        self.non = True
                if event.key == self.touches["agrandir_un_peu"]:
                    self.controleur.changer_taille(1)
                if event.key == self.touches["retrecir_un_peu"]:
                    self.controleur.changer_taille(-1)
                if event.key == self.touches["aug_vitesse_un_peu"]:
                    self.objets_jeu.liste_joueurs[0].change_vitesse(1)
                if event.key == self.touches["red_vitesse_un_peu"]:
                    self.objets_jeu.liste_joueurs[0].change_vitesse(-1)

    def gerer_entrees(self):
        """Gère les entrées du clavier pour le déplacement du joueur et les autres actions liées au clavier"""
        touches_pressees = pygame.key.get_pressed()
        if touches_pressees[self.touches["quitter"]] == 1:
            self.etat = False
        if touches_pressees[self.touches["agrandir"]] == 1:
            self.controleur.changer_taille(0.5)
        if touches_pressees[self.touches["retrecir"]] == 1:
            self.controleur.changer_taille(-0.5)
        if touches_pressees[self.touches["aug_vitesse"]] == 1:
            self.objets_jeu.liste_joueurs[0].change_vitesse(0.3)
        if touches_pressees[self.touches["red_vitesse"]] == 1:
            self.objets_jeu.liste_joueurs[0].change_vitesse(-0.3)
        dx = (
            touches_pressees[self.touches["droite"]] - touches_pressees[self.touches["gauche"]]
        )
        dy = (
            touches_pressees[self.touches["bas"]] - touches_pressees[self.touches["haut"]]
        )
        self.controleur.gerer_deplacement_touches(dx, dy)

    def dessiner(self):
        # dessine le fond
        self.screen.fill(configuration.couleur_fond)

        self.dessiner_joueur()

        self.dessiner_obstacles()

        if self.non:
            self.dessiner_points()

        if self.controleur.pixel_chemin:
            self.dessiner_chemin_pixels()

        pygame.display.flip()

    def dessiner_joueur(self):
        for joueur in self.objets_jeu.liste_joueurs:
            if isinstance(joueur, Joueur):
                pygame.draw.circle(
                    self.screen,
                    configuration.couleur_joueur,
                    (int(joueur.x), int(joueur.y)),
                    joueur.taille,
                )

    def dessiner_obstacles(self):
        for obj in self.objets_jeu.liste_obstacles:
            if isinstance(obj, Obstacle_rect):
                pygame.draw.rect(
                    self.screen, obj.couleur, (obj.x, obj.y, obj.largeur, obj.hauteur)
                )

    def dessiner_points(self):
        for ligne in self.objets_jeu.grille.grille:
            for point_grille in ligne:
                if isinstance(point_grille, Point):  # and point_grille.couleur == (20, 250, 100):
                    pygame.draw.circle(
                        self.screen,
                        point_grille.couleur,
                        (point_grille.x, point_grille.y),
                        400 / self.objets_jeu.grille.nbr_division,
                    )

    def dessiner_chemin_pixels(self):
        for x, y in self.controleur.pixel_chemin:
            self.screen.set_at((x, y), configuration.couleur_droite)
