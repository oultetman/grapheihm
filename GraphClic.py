# -*- coding: UTF-8 -*-
# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      pierre
#
# Created:     03/01/2018
# Copyright:   (c) pierre 2018
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import sys
# importation des blibliotheques Qt
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
# importation du fichier de l'interface graphique (IG)
# créée avec Qt puis compilée
from thGraph import Graph


# class widget graphique

class Graphique(QWidget):
    def __init__(self, parent=None, dimension=(10, 10, 100, 100)):
        super().__init__(parent)
        # redimensionnement du Widget
        self.setGeometry(QRect(dimension[0], dimension[1], dimension[2], dimension[3]))
        # Sauvegarde de l'identifiant de l'objet parent qui à créer le Widget
        self.parent = parent
        # tableau de points qui permet la sauvegarde des possitions cliquées
        self.graph = Graph()
        self.graph.creation_sommets(20, dimension[2], dimension[3], 30)
        self.graph.creation_arrete(20)
        # variable de sauvegarde du nom d'un sommet
        self.nom1 = -1
        self.sx = -1
        self.sy = -1
        # variable de sauvegarde de la position de la souris
        self.mx = -1
        self.my = -1
        # autorise l'evement mousseMoveEvent
        self.setMouseTracking(True)

    def mousePressEvent(self, e):
        x = e.x()
        y = e.y()
        self.parent.setWindowTitle("Position du dernier point x={} y={}".format(x, y))
        if self.parent.dessin == "sommet":
            # dessine sommet
            self.graph.add_sommet(x, y, Graph.nb_sommets)
        elif self.parent.dessin == "arrete":
            # dessine arrête
            nom = self.graph.sur_sommet(x, y)
            sommet = self.graph.sommetExist(nom)
            if nom != -1:
                if self.nom1 == -1:
                    self.nom1 = nom
                    self.sx = sommet.x
                    self.sy = sommet.y
                    self.mx = x
                    self.my = y
            else:
                self.nom1 = -1
                self.sx = -1
                self.sy = -1
        elif self.parent.dessin == "efface":
            # efface sommet ou arrête
            nom = self.graph.sur_sommet(x, y)
            if nom != -1:
                self.graph.del_sommet(nom)
            else:
                nomArrete = self.graph.sur_arrete(x, y, 5)
                if nomArrete:
                    self.graph.del_arrete(nomArrete)

        elif self.parent.dessin == "deplace":
            # déplace sommet ou arrête
            nom = self.graph.sur_sommet(x, y)
            if nom != -1 and self.nom1 == -1:
                self.nom1 = nom
        self.repaint()

    def mouseReleaseEvent(self, e):
        x = e.x()
        y = e.y()
        self.parent.setWindowTitle("Relacher point x={} y={}".format(x, y))
        if self.parent.dessin == "arrete":
            nom = self.graph.sur_sommet(x, y)
            if nom != -1:
                if nom != self.nom1:
                    self.graph.add_arrete(self.nom1, nom)
                    self.nom1 = -1
                    self.repaint()
                else:
                    self.nom1 = -1
        elif self.parent.dessin == "deplace":
            self.nom1 = -1

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()
        self.parent.setWindowTitle("Position point x={} y={}".format(x, y))
        if self.nom1 != -1:
            self.mx = x
            self.my = y
            if self.parent.dessin == "deplace":
                self.graph.deplace_sommet(self.nom1, x, y)
            self.repaint()

    def paintEvent(self, e):
        p = QPainter(self)
        if len(self.graph.arretes) > 0:
            for i in self.graph.arretes:
                try:
                    self.graph.arbre.index(i)
                    p.setPen(QColor(0, 0, 0))
                except:
                    p.setPen(QColor(255, 0, 0))
                p.drawLine(i.x1, i.y1, i.x2, i.y2)
                p.setPen(QColor(0, 0, 0))
                p.drawText((i.x1 + i.x2) // 2, (i.y1 + i.y2) // 2, "{:.0f}".format(i.longueur / self.parent.coef))
        if self.parent.dessin == 'arrete' and self.nom1 != -1:
            p.drawLine(self.sx, self.sy, self.mx, self.my)
        for i in self.graph.sommets:
            # dessin d'un disque de rayon 10 dans l'ojet p (voir biliothèque QPainter)
            p.setBrush(QColor(255, 255, 255))
            p.drawEllipse(i.x - 10, i.y - 10, 20, 20)
            p.drawText(QRect(i.x - 10, i.y - 10, 20, 20), Qt.AlignCenter, str(i.nom))


# classe principale de l'interface graphique
class MainDialog(QDialog, graphe.Ui_Dialog):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        # appel de setupUi créee par Qt
        self.setupUi(self)
        # Création d'un objet Graphique
        self.graph = Graphique(self, (20, 30, 581, 511))
        self.actions()
        # variable parents
        self.dessin = "sommet"
        self.coef = 10

    def actions(self):
        # Connection avec les bouton de l'IG
        self.sommet.clicked.connect(self.sommetClick)
        self.arrete.clicked.connect(self.arreteClick)
        self.effacer.clicked.connect(self.effacerClick)
        self.deplacer.clicked.connect(self.deplacerClick)
        self.ok.clicked.connect(self.okClick)

    def sommetClick(self):
        self.dessin = "sommet"

    def arreteClick(self):
        self.dessin = "arrete"

    def effacerClick(self):
        self.dessin = "efface"

    def deplacerClick(self):
        self.dessin = "deplace"

    def okClick(self):
        try:
            a = int(self.formule.text())
            if a > 0:
                self.coef = a
        except:
            print("la valeur entrée n'est pas un entier")
        if self.formule.text().upper() == "EG":
            self.graph.graph.efface_graphe()
            self.graph.nom1 = -1
        elif self.formule.text().upper() == "EA":
            self.graph.graph.efface_arretes()
        elif self.formule.text().upper() == "CC":
            self.graph.graph.calcul_comp_connexe()
            print(self.graph.graph)
        elif self.formule.text().upper() == "ACM":
            arbre = self.graph.graph.arbre_couvrant_mini()
            for a in arbre:
                print(a)
        elif self.formule.text().upper() == "PP":
            self.graph.graph.parcourt_en_profondeur(0)
            for a in self.graph.graph.arbre:
                print(a)
        elif self.formule.text().upper() == "PL":
            self.graph.graph.parcourt_en_largeur(0)
            for a in self.graph.graph.arbre:
                print(a)
        self.graph.repaint()


# lancement du programme
app = QApplication(sys.argv)
form = MainDialog()
form.show()
app.exec_()
