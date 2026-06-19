from modele import Joueur, Objets_jeu, Obstacle_rect, Obstacle_cercle, Grille, Point
from Configuration import configuration

# Tests classe Jeu


def test_ajout_objet():
    """Test les fonctions d'ajout d'objets au modèle et de récupération d'un joueur"""
    Liste_objet = Objets_jeu()
    jimmy = Joueur(0, 0)
    kouign_amann = Obstacle_rect(10, 10, 20, 20)
    grille = Grille()
    Liste_objet.ajouter_grille(grille)
    Liste_objet.ajouter_joueur(jimmy)
    Liste_objet.ajouter_obstacle(kouign_amann)
    assert Liste_objet.liste_joueurs[0] == jimmy
    assert Liste_objet.liste_obstacles[0] == kouign_amann
    assert Liste_objet.grille == grille


def test_recup_joueur():
    johnny = Joueur(0, 0)
    cave = Objets_jeu()
    cave.ajouter_joueur(johnny)
    cave.ajouter_joueur(johnny)
    kidnappé = cave.get_joueur(1)
    assert kidnappé == johnny


# Tests classe Joueur


def test_tp_bord():
    Joey = Joueur(0, 0)
    Joey.tp_bord(2, "vertical")
    Joey.tp_bord(2, "horizontal")
    assert Joey.y == 2
    assert Joey.x == 2


def test_paramètres_joueurs():
    Joel = Joueur(0, 0)
    Joel.change_taille(10)
    Joel.change_vitesse(10)
    assert Joel.taille == 50
    assert Joel.vitesse == 17.5


def test_mouvement():
    """Test les fonctions de déplacement du joueur"""
    jack = Joueur(0, 0)
    jack.bouger(2, 8, 10)
    assert jack.x == 20
    assert jack.y == 80


# Tests classe points


def test_comparaisons_points():
    assert Point(2, 5) == Point(2, 5)
    assert not Point(2, 5) == Point(15, 67)


def test_hashage_points():
    coccinelle = Point(0, 7)
    scarabée = Point(0, 1)
    chapeau = coccinelle.__hash__
    couvre_chef = coccinelle.__hash__
    casquette = scarabée.__hash__
    assert chapeau == couvre_chef
    assert casquette != chapeau


def test_ecriture_points():
    assert str(Point(6, 7)) == "6 7 True"


def test_changer_couleur_point():
    libellule = Point(0, 0)
    libellule.changer_couleur_point((67, 67, 67))
    assert libellule.couleur == (67, 67, 67)


def test_traversavilité():
    mur = Point(3, 2)
    mur.associer_traversabilité(True)
    assert mur.traversable
    assert mur.couleur == configuration.couleur_point
    mur.associer_traversabilité(False)
    assert not mur.traversable
    assert mur.couleur == configuration.couleur_point_intravesable


# Tests classe Grille


def test_grille_nombre_colonnes():
    grille = Grille()
    grille.diviser_ecran()
    for ligne in grille.grille:
        assert len(ligne) == grille.nbr_division


def test_allumer_points():
    grille_pain = Grille()
    grille_pain.diviser_ecran()
    a = Point(0, 0)
    b = Point(5, 6)
    c = Point(1, 2)
    chemin = [a, b]
    verif = [c]
    grille_pain.allumer_points(chemin, verif)
    assert a.couleur == configuration.couleur_points_chemin
    # assert c.couleur == configuration.couleur_points_verifie


# Tests classe collision


def test_collisions_rect_rect():
    gerbille = Obstacle_rect(5, 5, 3, 2)
    souris = Obstacle_rect(3, 3, 2, 3)
    rat = Obstacle_rect(9, 1, 1, 2)
    assert souris.collision_rect_rect(gerbille, 1, 0, 1)
    assert not souris.collision_rect_rect(gerbille, 0, 1, 1)
    assert souris.collision_rect_rect(gerbille, 1, 1, 1)
    assert not souris.collision_rect_rect(gerbille, 1, 1, 0)
    assert not rat.collision_rect_rect(gerbille, -1, -1, 1)


def test_collisions_cercle_cercle():
    lune = Obstacle_cercle(8, 4, 1)
    terre = Obstacle_cercle(7, 2, 1)
    boule_de_petanque = Obstacle_cercle(1, 1, 1)
    assert terre.collision_cercle_cercle(lune, 1, 1, 1)
    assert not terre.collision_cercle_cercle(lune, 1, 0, 1)
    assert not boule_de_petanque.collision_cercle_cercle(lune, 1, 1, 2)


def test_collisions_cercle_points():
    frisbee = Obstacle_cercle(8, 4, 1)
    grenouille = Point(8, 4)
    crapaud = Point(8, 5)
    tétard = Point(8, 2)
    assert frisbee.collision_cercle_point(grenouille.x, grenouille.y, frisbee.taille, frisbee.x, frisbee.y)
    assert frisbee.collision_cercle_point(crapaud.x, crapaud.y, frisbee.taille, frisbee.x, frisbee.y)
    assert not frisbee.collision_cercle_point(tétard.x, tétard.y, frisbee.taille, frisbee.x, frisbee.y)


def test_collisions_cercle_rect():
    jerry = Joueur(4, 3, configuration.couleur_joueur, configuration.vitesse, 2)
    bus = Obstacle_rect(1, 0, 2, 6)
    velo = Obstacle_rect(8, 3, 1, 2)
    quad = Obstacle_rect(5, 4, 2, 2)
    voiture = Obstacle_rect(5.5, 0, 3, 1.2)
    assert jerry.collision_cercle_rect(bus, 0, 0, 0)  # test collisions avec un côté du rectangle
    assert jerry.collision_cercle_rect(quad, 0, 0, 0)  # test collisions avec le coin du rectangle
    assert not jerry.collision_cercle_rect(velo, 0, 0, 0)  # test pas de collisions lorsque les deux hitboxs ne sont pas en contact
    assert not jerry.collision_cercle_rect(voiture, 0, 0, 0)  # test pas de collisions quand les hitbox se touchent mais qu'on est dans le coin de la hitbox
