
# ------------------------------------------------------------------------------------------------------------------------------
# Algorithme A* :

def cheminPlusCourt(grille, depart, objectif):
    """
    A* sur la grille. depart et objectif sont des tuples (x, y).
    Retourne une liste de tuples (x, y) formant le chemin, ou [] si aucun chemin.
    """
    def heuristique(a, b):
        return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    closed_list = []
    open_list = []
    compteur = 0
    heapq.heappush(open_list, (0, compteur, depart))

    parent = {}          # (x,y) -> (x,y) parent
    cout_g = {}             # coût réel depuis le départ
    cout_g[depart] = 0

    while open_list:
        _, _, u = heapq.heappop(open_list)

        if u == objectif:
            # Reconstituer le chemin
            chemin = []
            while u in parent:
                chemin.append(u)
                u = parent[u]
            # chemin.pop(0)
            chemin.append(depart)
            chemin.reverse()
            return chemin, closed_list

        x, y = u
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)]:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE):
                continue
            # On ne traverse que les cases vides ou déjà routes
            if grille[nx][ny] != EMPTY and grille[nx][ny] != ROAD and grille[nx][ny] != 1:
                continue

            v = (nx, ny)
            if (dx, dy) in set([(-1, -1), (-1, 1), (1, 1), (1, -1)]):
                nouveau_cout = cout_g[u] + sqrt(2)
            else:
                nouveau_cout = cout_g[u] + 1

            if v not in cout_g or nouveau_cout < cout_g[v]:
                cout_g[v] = nouveau_cout
                priorite = nouveau_cout + heuristique(v, objectif)
                compteur += 1
                heapq.heappush(open_list, (priorite, compteur, v))
                parent[v] = u
        closed_list.append(u)
    print("Pas de chemin")
    return []  # Aucun chemin trouvé


def remplace_chemin_plus_court(grille, depart, objectif):
    chemin, autre = cheminPlusCourt(grille, depart, objectif)
    print(len(chemin))
    for (x, y) in autre:
        grille[x][y] = VERIF
    for (x, y) in chemin:
        grille[x][y] = ROAD
    return grille