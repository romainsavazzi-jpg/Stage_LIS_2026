
def bresenham(
    coordonees_point_a,
    coordonnees_point_b,
):  # Test
    """Retourne les points de la grille sur la droite discrète entre coordonees_point_a et coordonnees_point_b"""
    # On initialise les points de départs et d'arrivée
    xA, yA = int(coordonees_point_a[0]), int(coordonees_point_a[1])
    xB, yB = int(coordonnees_point_b[0]), int(coordonnees_point_b[1])  # on prends des entiers car sinon on risque de ne pas trouver les pixels

    pixels = []
    dx = abs(xB - xA)
    dy = abs(yB - yA)
    # sens de parcours (haut/bas droite/gauche)
    sx = 1 if xA < xB else -1
    sy = 1 if yA < yB else -1
    # erreur initiale
    err = dx - dy  # l'écart entre la droite réelle et la droite de pixel

    while True:
        pixels.append((xA, yA))
        if xA == xB and yA == yB:  # on s'arrête quand on atteint le point final
            break
        e2 = 2 * err  # évite d'avoir des nombres flottant
        if e2 > -dy:  # On vérifie si l'erreur est assez grande pour justifier un pas en X ou en Y
            err -= dy
            xA += sx
        if e2 < dx:  #
            err += dx
            yA += sy

    return pixels
