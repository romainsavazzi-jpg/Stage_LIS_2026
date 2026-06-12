from Utilities import Bresenham, Algo_A_etoile


def test_bresenham_dans_tout_les_sens():
    assert Bresenham.bresenham((0, 0), (4, 0)) == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]  # vers la droite
    assert Bresenham.bresenham((4, 0), (0, 0)) == [(4, 0), (3, 0), (2, 0), (1, 0), (0, 0)]  # vers la gauche
    assert Bresenham.bresenham((0, 0), (0, 4)) == [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]  # vers le haut
    assert Bresenham.bresenham((0, 4), (0, 0)) == [(0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]  # vers le bas
    assert Bresenham.bresenham((0, 0), (3, 3)) == [(0, 0), (1, 1), (2, 2), (3, 3)]  # diagonale
