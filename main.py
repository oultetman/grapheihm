from tkinter import Tk, Canvas
from thGraph import *


class Dessin_graphe:
    def __init__(self, fenetre, canevas):
        self.g = Graph()
        self.sommets_clique: list[Sommet] = []
        self.arretes_clique: list[Arrete] = []
        canevas.bind('<Button-1>', self.dessine)
        canevas.bind('<Button-3>', self.down_right)
        canevas.bind('<Motion>', self.move)
        canevas.bind('<ButtonRelease>', self.up)
        fenetre.bind('<Delete>', self.delete_down)
        self.downright = False
        self.sommet_en_nouvement = None

    def dessine(self, event):
        s = self.g.sur_sommet(event.x, event.y, 15)
        a = self.g.sur_arrete(event.x, event.y)
        print(s)
        print(a)
        if a is False:
            # on clique pas sur une arrête
            if len(self.arretes_clique) > 0:
                # si arrêtes sélectionnées on les déselectionnent
                self.vide_arretes_clique()
            else:
                if s == -1:
                    # si on est pas sur un sommet on dessine un nouveau sommet
                    self.g.add_sommet(Sommet(event.x, event.y, Graph.nb_sommets))
                    self.g.sommets[-1].draw(canevas)
                else:
                    # on a cliqué sur un sommet non séelectionné
                    # on le selectionne (couleur rouge)
                    if s not in self.sommets_clique:
                        s.itemconfigure(canevas, fill="red", activefill="indian red")
                        self.sommets_clique.append(s)
                    else:
                        # sinom on le déselectionne et on le retire de la
                        # liste des sommets selectionné
                        s.itemconfigure(canevas, fill="white", activefill="grey")
                        self.sommets_clique.remove(s)
        else:
            # on clique sur une arrête
            if a not in self.arretes_clique:
                # si l'arrête n'est pas sélectionné
                # on la sélectionne
                a.itemconfigure(canevas, fill="red")
                self.arretes_clique.append(a)
            else:
                # si l'arrête est sélectionné
                # on la désélectionne
                a.itemconfigure(canevas, fill="black")
                self.arretes_clique.remove(a)

        if len(self.sommets_clique) > 1:
            # si deux sommets sont sélectionnés
            # on les relies par une arrête
            self.g.add_arrete(self.sommets_clique[0].nom, self.sommets_clique[1].nom)
            self.vide_sommets_clique()
            self.g.draw(canevas)

    def down_right(self, event):
        # appuie sur le bonton droit de la souris
        self.downright = True

    def move(self, event):
        # déplacement de la souris
        if self.downright:
            # bouton droit enfoncé
            s = self.g.sur_sommet(event.x, event.y, 15)
            print(s)
            if s != -1:
                # si sur sommet on le déplace
                self.g.deplace_sommet(s.nom, event.x, event.y)
                canevas.delete("all")
                self.g.draw(canevas)
                s.itemconfigure(canevas, fill="green")
                self.sommet_en_nouvement = s

    def up(self, event):
        if self.downright:

            self.downright = False
            if self.sommet_en_nouvement is not None:
                self.sommet_en_nouvement.itemconfigure(canevas, fill="white")
            self.vide_sommets_clique()

    def delete_down(self, event):
        # appuie sur la touche delete
        if len(self.sommets_clique) != 0:
            # on supprime le sommet selectionné
            self.g.del_sommet(self.sommets_clique[0].nom)
            canevas.delete("all")
            self.g.draw(canevas)
        if len(self.arretes_clique) != 0:
            # on supprime les arrtes sélectionnées
            while len(self.arretes_clique) != 0:
                a = self.arretes_clique.pop()
                self.g.del_arrete(a)
            canevas.delete("all")
            self.g.draw(canevas)

    def vide_sommets_clique(self):
        """Vide la liste des sommets cliqués et les désélectionnent"""
        while len(self.sommets_clique) != 0:
            self.sommets_clique.pop().itemconfigure(canevas, fill="white")

    def vide_arretes_clique(self):
        """Vide la liste des arrêtes cliquées et les désélectionnent"""
        while len(self.arretes_clique) != 0:
            self.arretes_clique.pop().itemconfigure(canevas, fill="black")



fenetre = Tk()
fenetre.geometry("480x360")
g = Graph()
nb_sommet = 1

canevas = Canvas(fenetre, width=500, height=400)
canevas.pack()
Dessin_graphe(fenetre, canevas)

fenetre.mainloop()
