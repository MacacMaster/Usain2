# -*- coding: utf-8 -*-

import sqlite3
from time import *
from PlanificationGlobale  import *

class Modele():
    def __init__(self, parent):
        self.parent=parent
        pass
        
    def importerDonnees(self,projectName):
        #Fonction que lors d'un nouveau projet, va preremplir les cases crc
        pass

    def getTime(self):
        return (datetime.now().strftime('%Y/%m/%d %H:%M:%S'))


class SQL():
    def __init__(self, parent):
        self.parent=parent
        self.Saas=parent.serveur
          
    def selDonnees(self,champ):
        #(self,nomTable,champs,where,indice)
        
        return self.Saas.selectionSQL1('PlanifGlobales',champ,'id_Projet',self.parent.idProjet)
        
        
    def afficherFonctions(self):
        #self.parent.serveur.
        pass
    
    #(Numéro Sprint,Nom de la fonction, priorité(basse=3,moyenne=2,haute=1)
    def creerFonction(self,sprint,nom,priorite,debut,fin):
        #id,id_Projet,id_Sprint,nom,id_Responsable,priorite,date_debut,date_fin
        if (priorite==3):
            priorite="Basse"
        elif (priorite==2):
            priorite="Moyenne"
        elif (priorite==1):
            priorite="Haute"    
        print("PlanifGlobales",self.parent.idProjet+","+sprint+","+nom+","+ self.parent.utilisateur+","+priorite+","+debut+","+fin)
        self.Saas.insertionSQL('PlanifGlobales',self.parent.idProjet+","+sprint+","+nom+","+ self.parent.utilisateur+","+priorite+","+debut+","+fin)
        #fonction d'ecriture dans la table planification
        
        pass
    
    #"INSERT INTO logs VALUES(?,?,?,?,?,?,?)", (date,org,user,ip,db,module,action,)
    #test
    def insCustom(self,sprint,nom,priorite,debut,fin):
        self.Saas.insCustom("INSERT INTO PlanifGlobales VALUES (?,?,?,?,?,?,?,?)",[self.parent.idProjet,sprint,nom,self.parent.utilisateur,priorite,debut,fin])
    def supressionFonction(self):
        pass
    
    def previsionHeure(self):
        pass
    
    def calculPourcent(self,debut=time()-50,fin=time()+50):
        tempsNow=time()-debut
        tempsEnd=fin-debut
        pourcent=(tempsNow/tempsEnd)*100
        print("%.2f" % round(pourcent,2)+"%")
        return pourcent
    
    
          