import tomllib
import os
import tkinter as tk

root = tk.Tk()

# importe le toml
with open(os.path.join(os.path.dirname(__file__), "données.toml"), "rb") as f:
    tom = tomllib.load(f)


# vérifie si le plein écran est activé et définit la taille de l'écran en conséquence
if tom["ecran"]["plein_ecran"]:
    largeur = root.winfo_screenwidth()
    hauteur = root.winfo_screenheight()
else:
    largeur = tom["ecran"]["largeur_fixe"]
    hauteur = tom["ecran"]["hauteur_fixe"]


FPS: int = tom["ecran"]["fps"]

# Couleurs
couleur_fond = tuple(tom["couleurs"]["fond"])
couleur_joueur = tuple(tom["couleurs"]["joueur"])
couleur_rectangle = tuple(tom["couleurs"]["rectangle"])
couleur_cercle = tuple(tom["couleurs"]["cercle"])
couleur_droite = tuple(tom["couleurs"]["droite"])
couleur_point = tuple(tom["couleurs"]["points"])
couleur_point_intravesable = tuple(tom["couleurs"]["intraversable"])
couleur_points_chemin = tuple(tom["couleurs"]["points_chemin"])
couleur_points_verifie = tuple(tom["couleurs"]["points_verifies"])

# Joueur
vitesse = tom["joueur"]["vitesse"]
taille = tom["joueur"]["taille"]

# Touches — on résout les getattr ici une bonne fois pour toutes
touches = tom["touches"]

# Grille
divisions = tom["grille"]["divisions"]

# Obstacles
nbr_rect = tom["obstacles"]["nombre_rectangles"]
nbr_cercles = tom["obstacles"]["nombre_cercles"]

# User Interface
taille_selec_point_d_accroche = tom["user_interface"]["taille_selec_point_d_accroche"]

root.destroy()
