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
        _, ax, ay = controle.selection_point(a.x, a.y)
        _, bx, by = controle.selection_point(b.x, b.y)
        return sqrt((ax - bx) ** 2 + (ay - by) ** 2)

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


def determination_liste_reduite_chemin(liste_points, liste_des_points_verifies):
    liste_finale = []
    if liste_points:
        dx_prec = 0
        dy_prec = 0
        for i in range(len(liste_points) - 1):
            dx = int(liste_points[i + 1].x - liste_points[i].x)
            dy = int(liste_points[i + 1].y - liste_points[i].y)
            if dx != dx_prec or dy != dy_prec:
                liste_finale.append(liste_points[i])
            dx_prec = dx
            dy_prec = dy
        liste_finale.append(liste_points[len(liste_points) - 1])
    return liste_finale, liste_des_points_verifies


# def remplace_chemin_plus_court(grille, depart, objectif):
#     chemin, autre = cheminPlusCourt(grille, depart, objectif)
#     print(len(chemin))
#     for (x, y) in autre:
#         grille[x][y] = VERIF
#     for (x, y) in chemin:
#         grille[x][y] = ROAD
#     return grille


# print(f"Exploration de ({u.x}, {u.y}), f={cout_g[u] + heuristique(u, objectif):.2f}")
