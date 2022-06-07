# -------------------------------------------------------------------------------
# Nom:        module2
# Description:
#
# Auteur:      pierre
#
# Created:     26/10/2018
# Copyright:   (c) pierre 2018
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import math
from random import randint
from tkinter import Tk, Canvas


class Sommet:
    rayon = 15

    def __init__(self, x, y, nom):
        """cree un sommet dans un plan"""
        self.x = x
        self.y = y
        self.nom = nom
        self.voisins = []
        self.pere = None
        self.compConnexe = None
        self.niveau = None
        self.idg = None

    def add_voisin(self, sommet):
        """ajoute un voisin à un sommet. La liste des voisins
        des deux sommets est modifiée"""
        for v in self.voisins:
            if v == sommet:
                return -1
        self.voisins.append(sommet)
        sommet.voisins.append(self)

    def delVoisin(self, sommet):
        """Suprime un voisin à un sommet. La liste des voisins
        des deux sommets est modifiée"""
        try:
            self.voisins.remove(sommet)
            sommet.voisins.remove(self)
        except:
            pass

    def sur_sommet(self, x, y, delta=10):
        """ retourne le nom du sommet si x et y correspondent aux coordonnées de sommet
        à +- delta près et -1 dans le cas contraire"""
        if self.x - delta <= x <= self.x + delta and self.y - delta <= y <= self.y + delta:
            return self.nom
        return -1

    def voisins_to_str(self):
        s = ""
        for v in self.voisins:
            s += str(v.nom) + ","
        return s[:-1]

    def tri_voisins(self):
        """tri les voisins du sommet par distance"""
        self.voisins = sorted(self.voisins, key=lambda v: math.sqrt((v.x - self.x) ** 2 + (v.y - self.y) ** 2))

    def __str__(self):
        return ("{} : ({},{}) voisins {{{}}} père {} niveau {} comp_connexe {}".format(self.nom, self.x, self.y,
                                                                                       self.voisins_to_str(), self.pere,
                                                                                       self.niveau, self.compConnexe))

    def draw(self, canevas):
        rayon = 15
        self.idg = canevas.create_oval(self.x - rayon, self.y - rayon,
                                       self.x + rayon,
                                       self.y + rayon, fill="white", activefill="grey")
        canevas.create_text(self.x, self.y, text=self.nom)

    def itemconfigure(self, canevas, **kwargs):
        canevas.itemconfigure(self.idg, kwargs)


class Arrete:
    coef = 1
    arrondi = 6

    def __init__(self, sommet1, sommet2):
        self.nom = sommet1, sommet2
        self.x1 = sommet1.x
        self.y1 = sommet1.y
        self.x2 = sommet2.x
        self.y2 = sommet2.y
        self.longueur = self.long()
        self.longeur_visible = True
        sommet1.add_voisin(sommet2)
        self.idg = None

    def set1(self, x1, y1):
        self.x1 = x1
        self.y1 = y1
        self.longueur = self.long()

    def set2(self, x2, y2):
        self.x2 = x2
        self.y2 = y2
        self.longueur = self.long()

    def long(self):
        l = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2) / Arrete.coef
        l = round(l, Arrete.arrondi)
        return l

    def set_longeur(self, long):
        pass

    def __str__(self):
        return "({},{}) : ({},{}) ({},{}) {:.2f}".format(self.nom[0].nom, self.nom[1].nom, self.x1, self.y1, self.x2,
                                                         self.y2, self.longueur)

    def sur_arrete(self, x, y, delta=10):
        """ retourne le nom de l'arrete si x et y correspondent aux coordonnées de sommet
        à +- delta près et False dans le cas contraire"""
        b = self.x1 - self.x2
        a = self.y2 - self.y1
        c = -a * self.x1 - b * self.y1
        long = abs(a * x + b * y + c) / math.sqrt(a ** 2 + b ** 2)
        if long < delta and (self.x1 + self.x2) // 2 - delta <= x <= (self.x1 + self.x2) + delta and (
                self.y1 + self.y2) // 2 - delta <= y <= (self.y1 + self.y2) // 2 + delta:
            return self
        return False

    def draw(self, canevas: Canvas):
        self.idg = canevas.create_line(self.x1, self.y1, self.x2, self.y2, activefill="grey")

    def itemconfigure(self, canevas, **kwargs):
        canevas.itemconfigure(self.idg, kwargs)


class Graph:
    nb_arretes = 0
    nb_sommets = 0

    def __init__(self):
        self.sommets: list[Sommet] = []
        self.arretes: list[Arrete] = []
        self.arbre = []

    def sommet_exist(self, nomSommet) -> Sommet:
        """retourne le sommet si sommet (nom du sommet ou le sommet lui même) est dans le graphe. -1
        dans le cas contraire"""
        if type(nomSommet) == Sommet:
            nomSommet = nomSommet.nom
        for s in self.sommets:
            if nomSommet == s.nom:
                return s
        return -1

    def arrete_exist(self, nomArretes) -> Arrete:
        """retourne l'arrete si arrete designée par son nom ou l'objet lui même
        est dans le graphe. -1 dans le cas contraire"""
        if type(nomArretes) == Arrete:
            nomArretes = nomArretes.nom[0].nom, nomArretes.nom[1].nom
        for a in self.arretes:
            if nomArretes == (a.nom[0].nom, a.nom[1].nom) or (
                    nomArretes[0] == a.nom[1].nom and nomArretes[1] == a.nom[0].nom):
                return a
        return -1

    def add_sommet(self, x, y=None, nom=None):
        """Ajoute un sommet à la liste s'il n'existe pas
        Retourne True si le sommet est ajouté et False dans le
        cas contraire"""
        if type(x) == Sommet:
            sommet = x
        else:
            if type(x) == tuple:
                if y != None:
                    nom = y
                y = x[1]
                x = x[0]
            if nom == None:
                nom = Graph.nb_sommets
            sommet = Sommet(x, y, nom)
        if self.sommet_exist(sommet) == -1:
            self.sommets.append(sommet)
            Graph.nb_sommets += 1
            return True
        return False

    def add_arrete(self, nom_sommet1:[tuple,Sommet], nom_sommet2:[Sommet,None]=None):
        """Ajoute une arrete à la liste si elle n'existe pas
        Retourne True si l'arrete est ajoutée et False dans le
        cas contraire"""
        if type(nom_sommet1) == tuple:
            nom_sommet2 = nom_sommet1[1]
            nom_sommet1 = nom_sommet1[0]
        sommet1 = self.sommet_exist(nom_sommet1)
        sommet2 = self.sommet_exist(nom_sommet2)
        if sommet1 != -1 and sommet2 != -1:
            if self.arrete_exist((nom_sommet1, nom_sommet2)) == -1:
                self.arretes.append(Arrete(sommet1, sommet2))
                Graph.nb_arretes += 1
                return True
        return False

    def del_sommet(self, nom_sommet):
        """suprime un sommet désigné par son nom"""
        s = self.del_arrete_sommet(nom_sommet)
        if s != -1:
            self.sommets.remove(s)

    def del_arrete_sommet(self, nom_sommet):
        """suprime les arrêtes d'un sommet désigné par son nom"""
        s = self.sommet_exist(nom_sommet)
        if s != -1:
            voisins = s.voisins.copy()
            for v in voisins:
                self.del_arrete((nom_sommet, v.nom))
        return s

    def del_arrete(self, nom_arrete):
        """ suprime une arrete à partir de son nom (sommet1.nom,sommet2.nom)
         si elle existe et met à jour la liste de voisins concernés"""
        # on vérifie que l'arrête existe
        a = self.arrete_exist(nom_arrete)
        if a != -1:
            # verifie que les sommets existes
            s1 = self.sommet_exist(a.nom[0])
            s2 = self.sommet_exist(a.nom[1])
            if s1 != -1 and s2 != -1:
                s1.delVoisin(s2)
                if self.arrete_exist(a):
                    self.arretes.remove(a)
                Graph.nb_arretes -= 1

    def sur_sommet(self, x, y=None, delta=10) -> Sommet:
        """retourne le sommet a la position x,y à delta près si il existe
        et -1 dans le cas contraire"""
        if type(x) == tuple:
            if y != None:
                delta = y
            y = x[1]
            x = x[0]
        for s in self.sommets:
            n = s.sur_sommet(x, y, delta)
            if n != -1:
                return s
        return -1

    def sur_arrete(self, x, y, delta=5):
        """retourne l'arrête si elle se trouve à proximité de (x,y)"""
        for s in self.arretes:
            n = s.sur_arrete(x, y, delta)
            if n:
                return n
        return False

    def deplace_sommet(self, nom_sommet, x, y):
        """deplace le sommet de nom nom_sommet à la position (x,y)"""
        s = self.sommet_exist(nom_sommet)
        if s:
            s.x = x
            s.y = y
            for a in self.arretes:
                if a.nom[0] == s:
                    a.set1(x, y)
                elif a.nom[1] == s:
                    a.set2(x, y)

    def remame_sommet(self, ancien_nom, nouveau_nom) -> bool:
        """renome le sommet de nom ancien_nom par nouveau_nom"""
        if ancien_nom != nouveau_nom:
            s = self.sommet_exist(ancien_nom)
            if s != -1 and self.sommet_exist(nouveau_nom) == -1:
                s.nom = nouveau_nom
                return True
        return False

    def __str__(self):
        s = "Sommets : {}\n".format(Graph.nb_sommets)
        for i in self.sommets:
            s += i.__str__() + "\n"
        s += "Arretes : {}\n".format(Graph.nb_arretes)
        for i in self.arretes:
            s += i.__str__() + "\n"
        return s

    def exporte(self):
        res = "graph=["
        coord = "coor=["
        arrete = "arrete=["
        for s in self.sommets:
            res += "{},".format(s.nom)
            coord += "({},{}),".format(s.x, s.y)
        for a in self.arretes:
            arrete += "({},{}):{:.2f},".format(a.nom[0], a.nom[1], a.long())
        res = res[:-1] + "]"
        coord = coord[:-1] + "]"
        arrete = arrete[:-1] + "]"
        return res + "\n" + coord + "\n" + arrete + "\n"

    def creation_sommets(self, n, largeur, hauteur, pas):
        """Cree des n sommets, distants de pas (en x et en y),
        au hasard dans une zone (largeur,hauteur)"""
        xmaxi = (largeur - pas) // pas
        ymaxi = (hauteur - pas) // pas
        for i in range(n):
            point = (randint(0, xmaxi) * pas + pas // 2, randint(0, ymaxi) * pas + pas // 2)
            while self.sur_sommet(point) != -1:
                point = (randint(0, xmaxi) * pas + pas // 2, randint(0, ymaxi) * pas + pas // 2)
            self.add_sommet(point)

    def creation_arrete(self, n):
        """ retourne au hasard une arrete (tupple) x<>y avec x<y"""
        i = 0
        while i < n:
            x, y = 0, 0
            while x == y:
                x = randint(0, len(self.sommets) - 1)
                y = randint(0, len(self.sommets) - 1)
            if x < y:
                a = (x, y)
            else:
                a = (y, x)
            if self.add_arrete(a) == True:
                i += 1

    def efface_arretes(self):
        """vide la liste des arrêtes"""
        while len(self.arretes) > 0:
            self.del_arrete(self.arretes[0].nom)

    def efface_graphe(self):
        """vide la liste des sommets et des arrêtes"""
        Graph.nb_sommets = 0
        Graph.nb_arretes = 0
        self.sommets = []
        self.arretes = []

    def calcul_comp_connexe(self):
        """calcul la composante connexe d'un graphe"""
        for i, s in enumerate(self.sommets):
            s.comp_connexe = i
        for a in self.arretes:
            if a.nom[0].comp_connexe != a.nom[1].comp_connexe:
                s1 = min(a.nom[0].comp_connexe, a.nom[1].comp_connexe)
                s2 = max(a.nom[0].comp_connexe, a.nom[1].comp_connexe)
                for s in self.sommets:
                    if s.comp_connexe == s2:
                        s.comp_connexe = s1

    def tri_arrete(self):
        """ tri les arrêtes par ordre croissant"""
        self.arretes = sorted(self.arretes, key=lambda arrete: arrete.longueur)

    def arbre_couvrant_mini(self):
        arbre = []
        self.tri_arrete()
        for i, s in enumerate(self.sommets):
            s.comp_connexe = i
        for a in self.arretes:
            if a.nom[0].comp_connexe != a.nom[1].comp_connexe:
                s1 = a.nom[0].comp_connexe
                arbre.append(a)
                for s in self.sommets:
                    if s.comp_connexe == s1:
                        s.comp_connexe = a.nom[1].comp_connexe
        self.arbre = arbre
        return arbre

    def tri_voisins(self):
        """trie les voisins de chaque sommets d'un graphe
        en fonction de leur distance"""
        for s in self.sommets:
            s.tri_voisins()

    def profondeur(self, racine, niveau=0):
        racine.niveau = niveau
        niveau += 1
        for v in racine.voisins:
            if v.niveau == -1:
                self.arbre.append(self.arrete_exist((racine.nom, v.nom)))
                self.profondeur(v, niveau)

    def parcourt_en_profondeur(self, racine=0):
        self.arbre = []
        for s in self.sommets:
            s.niveau = -1
        racine = self.sommet_exist(racine)
        self.tri_voisins()
        self.profondeur(racine, 0)

    def parcourt_en_largeur(self, racine):
        """parcour en largeur du graphe partant de racine"""
        racine = self.sommet_exist(racine)
        self.tri_voisins()
        self.arbre = []
        dv = [0 for i in range(len(self.sommets))]
        at = []
        for s in self.sommets:
            s.niveau = -1
            s.pere = s
            dv.append(0)
        dv[racine.nom] = 1
        racine.pere = racine
        racine.niveau = 0
        at.append(racine)
        while len(at) != 0:
            v = at.pop(0)
            for x in v.voisins:
                if dv[x.nom] == 0:
                    dv[x.nom] = 1
                    at.append(x)
                    x.pere = v
                    x.niveau = v.niveau + 1
        for s in self.sommets:
            if s.pere != s:
                self.arbre.append(self.arrete_exist((s.pere.nom, s.nom)))

    def insere_sommet_sur_arrête(self,arrete:[Arrete,tuple]):
        """insère un nouveau sommet sur une arrête"""
        a = self.arrete_exist(arrete)
        if isinstance(a,Arrete):
            s1 = a.nom[0]
            s2 = a.nom[1]
            if self.add_sommet((a.x1+a.x2)//2,(a.y1+a.y2)//2) :
                s3 = self.sommets[-1]
                self.del_arrete(a)
                self.add_arrete(s1, s3)
                self.add_arrete(s3, s2)


    def draw(self, canevas):
        """dessine le graphe sur un canvas tkinter"""
        for a in self.arretes:
            a.draw(canevas)

        for s in self.sommets:
            s.draw(canevas)



def main():
    g = Graph()
    Arrete.arrondi = 0
    g.add_sommet(Sommet(10, 15, 0))
    g.add_sommet(Sommet(25, 30, 1))
    g.add_sommet(Sommet(50, 35, 2))
    g.add_arrete(0, 1)
    g.add_arrete(1, 2)
    g.add_arrete(2, 0)
    print(g)
    # g.deplace_sommet(0, 100, 100)
    # print(g)
    ##    print(g.exporte())
    ##    print(g.surSommet((30,17)))
    ##    g.creationSommets(10,200,150,20)
    ##    print(g)
    ##    g.creationArrete(10)
    ##    print(g)
    ##    g.delArreteSommet(0)
    ##    print(g)
    # print(g.calcul_comp_connexe())
    # g.sommets[0].tri_voisins()
    # print(g)
    print(g.remame_sommet(1, 2))
    print(g)
    g.insere_sommet_sur_arrête((2,0))
    print(g)
if __name__ == '__main__':
    main()
