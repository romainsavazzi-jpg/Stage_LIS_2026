from modele import Joueur, Objets_jeu, Obstacle_rect, Grille, Point

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
    assert Point(0, 0)

# Tests classe Grille