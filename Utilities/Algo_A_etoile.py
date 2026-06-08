from math import sqrt
import heapq

# ------------------------------------------------------------------------------------------------------------------------------
# Algorithme A* :


def cheminPlusCourt(controle, grille, depart, objectif):
    """
    A* sur la grille. depart et objectif sont des tuples points Point().
    Retourne une liste de points formant le chemin, ou [] si aucun chemin.
    """
    def heuristique(a, b):
        return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

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
            # chemin.append(depart)
            chemin.reverse()
            if closed_list != []:
                closed_list.pop(0)
            return chemin, closed_list

        _, x, y = controle.selection_point(u.x, u.y)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)]:
            nx, ny = x + dx, y + dy
            nb_colonnes = len(grille[0])
            nb_lignes = len(grille)
            if not (0 <= nx < nb_colonnes and 0 <= ny < nb_lignes):
                continue
            # On ne traverse que les cases vides ou déjà routes
            if not grille[ny][nx].traversable:
                continue

            v = controle.objets_jeu.grille.grille[ny][nx]
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
    return [], []  # Aucun chemin trouvé


# def remplace_chemin_plus_court(grille, depart, objectif):
#     chemin, autre = cheminPlusCourt(grille, depart, objectif)
#     print(len(chemin))
#     for (x, y) in autre:
#         grille[x][y] = VERIF
#     for (x, y) in chemin:
#         grille[x][y] = ROAD
#     return grille
