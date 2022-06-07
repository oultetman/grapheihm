#-------------------------------------------------------------------------------
# Nom:        GRAPHETP1
# Description:
#
# Auteur:      pierre
#
# Created:     20/09/2018
# Copyright:   (c) pierre 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from random import randint
import time
def connexe(sommets,arretes):
    """ retourne une liste des composantes connexe d'un graphe à partir
     de la liste des sommets et des arrêtes"""
    t=list(sommets)
    parcourt=0
    for arrete in arretes:
        x,y=arrete
        if t[x]!=t[y]:
##            print(arrete,t[x],t[y] )
            y0=max(t[y],t[x])
            for i in range(len(t)):
                # on parcourt tous les sommets
                if t[i]==y0:
                    t[i]=min(t[x],t[y])
                parcourt+=1
##            print(arrete,t)
    print("connexe terminé")
    return t,parcourt

def connexe1(sommets,arretes):
    """ retourne une liste des composantes connexe d'un graphe à partir
     de la liste des sommets et des arrêtes"""
    t=list(sommets)
    parcourt=0
    for arrete in arretes:
        x,y=arrete
        if t[x]!=t[y]:
##            print(arrete,t[x],t[y] )
##            y0=max(t[y],t[x])
            y0=t[y]
##            for i in range(y0,max(x+1,y+1)):
            for i in range(y0,y+1):
                if t[i]==y0:
##                    t[i]=min(t[x],t[y])
                    t[i]=t[x]
                parcourt+=1
##            print(arrete,t)
    print("connexe1 terminé")
    return t,parcourt

def randArrete(n):
    """ retourne au hasard une arrete (tupple) x<>y avec x<y"""
    x,y=0,0
    while x==y:
        x=randint(0,n-1)
        y=randint(0,n-1)
    if x<y:
        return (x,y)
    else:
        return (y,x)

def arreteExiste(arrete,t):
    """ retourne true si arrete est présente dans le tableau (liste) t"""
    for i in t:
        if arrete==i:
            return True
    return False

def trouveVoisin(nbrSommet,arretes):
    voisin=[]
    for i in range(nbrSommet):
        voisin.append(set([i]))
    for a in arretes:
        voisin[a[0]].add(a[1])
        voisin[a[1]].add(a[0])
    return voisin

def compConnexe(nbrSommet,voisin):
    comp=[]
    c=set()
    for i in range(nbrSommet):
        c.add(i)
    while len(c)>0:
        connexe=voisin[c.pop()]
        for i in voisin:
            if len(connexe&i)>0:
                connexe=connexe|i
        comp.append(connexe)
        c=c-connexe
    return comp

def main():
    debug=0
    if debug==0:
        n=int(input("Entrer le nombre de sommets"))
        m=int(input("Entrer le nombre d'arrêtes"))
        comp=[]
        arretes=[]

        for i in range(n):
            comp.append(i)
        for i in range(m):
            a=randArrete(n)
            while arreteExiste(a,arretes):
               a=randArrete(n)
            arretes.append(a)
        arretes.sort()
    else:
        comp=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        arretes=[(0, 13), (1, 6), (1, 9), (1, 14), (3, 7), (3, 10), (3, 14), (4, 15), (4, 16), (4, 18), (5, 18), (6, 16), (6, 19), (7, 16), (8, 12), (8, 13), (11, 14), (11, 19), (14, 15), (18, 19)]
        n=len(comp)
        m=len(arretes)
##    print(comp)
##    print(arretes)
    t=time.time()
    connexe(comp,arretes)

    print(time.time()-t)
    t=time.time()
    connexe1(comp,arretes)
    print(time.time()-t)
    print("")
    t=time.time()
    voisins=trouveVoisin(n,arretes)
##    print(voisins)
    compConnexe(n,voisins)
    print(time.time()-t)

if __name__ == '__main__':
    main()
