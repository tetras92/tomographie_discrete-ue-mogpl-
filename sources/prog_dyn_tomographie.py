# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import time

def T(G, ligneOuColonne, indice):
    """retourne la réponse de la ligne (ligneOuColonne=0) / colonne (ligneOuColonne=1) d'indice indice étant donné
        l'état de la grille G"""
    N = len(G[0]) #N: nombre de lignes 
    M = len(G[1]) #M : nombre de colonnes
    
    
    #TB : tableau des booleéens
    #S : Liste des contraintes
    #L : Etat de la ligne ou colonne considérée      
    S = [0] + (G[ligneOuColonne][indice]).copy() # pour utiliser les indices l tels que définis dans l'énoncé
    
    
    if ligneOuColonne == 0:
        TB = [['#' for k in range(M)] for i in range(len(S))]
        L = G[2][indice, :]
    else:
        TB = [['#' for k in range(N)] for i in range(len(S))]
        L = G[2][:, indice]
    
    #Prédit aucuneCouleurEntre
    def aucuneCouleurEntre(j1, j2, couleur):
        for j in range(j1,j2+1):
            if L[j] == couleur:
                return False
        return True
    #Formule des t(j,l) en interaction avec TB 
    def t(j,l):
        if l == 0:
            TB[l][j] = aucuneCouleurEntre(0, j, 1)
            return TB[l][j]
        if l == 1 and j == S[l]-1:
            TB[l][j] = aucuneCouleurEntre(0,j,0)
            return TB[l][j]
        if j <= S[l]-1:
            TB[l][j] = False
            return TB[l][j]
        if TB[l][j] != '#':
            return TB[l][j]
        TB[l][j] = (L[j] == 0 and t(j-1,l)) or \
    (L[j] == 1 and aucuneCouleurEntre(j-(S[l]-1), j, 0) and \
        L[j-S[l]] != 1 and t(j-S[l]-1, l-1)) or ((L[j] == -1 ) and \
         (t(j-1,l) or (aucuneCouleurEntre(j-(S[l]-1), j, 0) and \
            L[j-S[l]] != 1 and t(j-S[l]-1, l-1))))
        return TB[l][j]
    
#    for l in range(0, len(S)):
#        for j in range(0, len(TB[0])):
#            valeur_de_verite = t(j,l)
#            TB[l][j] = valeur_de_verite
#            
#    
#    print("tb",TB)
    if ligneOuColonne == 0:
        return t(M-1, len(S)-1)#TB[-1][-1]
    else:
        return t(N-1, len(S)-1)

#
def readFile(filename):
    """Lis un fichier et retourne la grille et ses contraintes sous la forme d'un triple
    """
    f = open ( filename, "r" )
    M = f.readlines()
    ROWS_CONSTRAINTS = list() #Liste des contraintes de lignes
    COLUMNS_CONSTRAINTS = list() # Liste des contraintes de colonnes
    ligne = 0
    while M[ligne][0] != '#':
        L = M[ligne].split(' ')
        if M[ligne] == '\n':
            L = list()
        else:
            L = [int(n) for n in L] #Conversion et suprression des '\n'
        ROWS_CONSTRAINTS.append(L)
        ligne += 1
    
    ligne += 1
    while ligne < len(M):
        L = M[ligne].split(' ')
        if M[ligne] == '\n':
            L = list()
        else:
            L = [int(n) for n in L] #Conversion et suprression des '\n'
        COLUMNS_CONSTRAINTS.append(L)
        ligne += 1
    
    return (ROWS_CONSTRAINTS, COLUMNS_CONSTRAINTS, np.ones((len(ROWS_CONSTRAINTS), len(COLUMNS_CONSTRAINTS)))*(-1))
    


def coloration(G):
    """retourne la Grille Coloriée et True si le coloriage est possible et False sinon"""
    N = len(G[0]) #N: nombre de lignes 
    M = len(G[1]) #M : nombre de colonnes
    LignesAVoir = {i for i in range(N)}
    ColonnesAVoir = {j for j in range(M)}
    

    while len(LignesAVoir) != 0 or len(ColonnesAVoir) != 0:

        for i in LignesAVoir:
#            print("ligne à voir", i)
#            print(G[2])
            Nouveaux = set()
            for j in range(M):
                
                if G[2][i,j] != -1: continue
                
                #Coloriage en Blanc
                G[2][i,j] = 0
                #Réponse ligne i
                reponse0 = T(G, 0, i)
                #Coloriage en Noir
                G[2][i,j] = 1
                #Réponse ligne i
                reponse1 = T(G, 0, i)
                if reponse0 and reponse1: #Même Réponse (Vraie) => remettre à -1 (indéterminé)
                    G[2][i,j] = -1
                elif reponse0:
                    G[2][i,j] = 0
#                    print("case", i,":", j, "Blanche")
                    Nouveaux.add(j)
                elif reponse1:
                    G[2][i,j] = 1
#                    print("case", i,":", j, "Noire")
                    Nouveaux.add(j)
                else:
                    return False #Pas de Solution
#                if (i == 3 and j == 3):
#                      print("Nouveaux", NouveauxL)
            ColonnesAVoir = ColonnesAVoir | Nouveaux
#            print("colo",ColonnesAVoir)
        LignesAVoir = set()
        
        for j in ColonnesAVoir:
#              print("colonne à voir", j)
              Nouveaux = set() 
              for i in range(N):
                  
                  if G[2][i,j] != -1: continue
                  
                  #Coloriage en Blanc
                  G[2][i,j] = 0
                    #Réponse ligne i
                  reponse0 = T(G, 1, j)
                    #Coloriage en Noir
                  G[2][i,j] = 1
                    #Réponse ligne i
                  reponse1 = T(G, 1, j)
                  if reponse0 and reponse1: #Même Réponse (Vraie) => remettre à -1 (indéterminé)
                      G[2][i,j] = -1
                  elif reponse0:
                      G[2][i,j] = 0
#                      print("case", i,":", j, "Blanche")
                      Nouveaux.add(i)
                  elif reponse1:
                     G[2][i,j] = 1
#                     print("case", i,":", j, "Noire")
                     Nouveaux.add(i)
                  else:
                     return False
#                  print("nouveaux", Nouveaux)
              LignesAVoir = LignesAVoir | Nouveaux
#              print("lignes",LignesAVoir)
        ColonnesAVoir = set()
#    print(G[2])
    return True

if __name__ == "__main__":
    for i in range(1,11):
        G = readFile("instances/"+str(i)+".txt")
        print ("Instance n° ", i)
#        print("Lignes", G[0])
#        print("Colonnes", G[1])
        t1 = time.clock()
        coloration(G)
        t2 = time.clock()
#        print(G[2])
        print(t2 - t1)
#        print(coloration(G))
        plt.imshow(G[2], cmap='binary', interpolation='none')
        plt.savefig(str(i)+'.png')
    
    
    