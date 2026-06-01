from modele import Joueur
from controleur import Controleur
from vue import Vue
from configuration import largeur, hauteur

# Instanciation dans le bon ordre
joueur = Joueur(largeur // 2, hauteur // 2)
controleur = Controleur()
vue = Vue(joueur, controleur)

vue.run()
