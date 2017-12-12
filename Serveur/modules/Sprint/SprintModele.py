# -*- coding: utf-8 -*-

import sqlite3
from time import *
from Sprint  import *

#TODO - UPDATE

class Modele():
    def __init__(self, parent, serveur):
        self.parent=parent
        self.serveur=serveur

    def getTime(self):
        return (datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

    def retournerLesTaches(self,id_sprint,id_utilisateur):
        nomTable = "Taches"
        champs = "tache, reussi, id"
        where = ["id_utilisateur", "id_sprint"]
        valeur = [str(id_utilisateur),str(id_sprint)]
        
        requete = self.parent.serveur.selDonneesWHERE(nomTable,champs,where,valeur)
        return requete
    
    def retournerLesSprints(self,id_projet):
        nomTable = "Sprints"
        champs = "id, nom"
        where = ["id_projet"]
        valeur = [id_projet]
        
        requete = self.parent.serveur.selDonneesWHERE(nomTable,champs,where,valeur)

        
  
        return requete
    
    def retournerLesUtilisateurs(self,id_Organisation):
        nomTable = "Usagers"
        champs = "id, nom"
        where = ["id_Organisation"]
        valeur = [id_Organisation]
        
        requete = self.parent.serveur.selDonneesWHERE(nomTable,champs,where,valeur)
        return requete
    
    def insererNouvelleTache(self, id_projet, id_utilisateur, id_sprint, tache, reussi):
        a1 = id_projet
        a2 = id_utilisateur
        a3 = id_sprint
        a4 = tache
        a5 = reussi
        chaine = "'" + str(a1) + "','" +str(a2) + "','"  + str(a3)+ "','" +str(a4) + "','" +str(a5) +  "'"
        #projet utilisateur sprint tache reussi
        self.serveur.insertionSQL("Taches", chaine)
        
    def enregistrer(self,id_projet,id_utilisateur,id_sprint,list):
        les_id_taches = self.retournerLesTaches(id_sprint,id_utilisateur)
        for element in les_id_taches:
            id_tache = element[2]
            self.parent.serveur.delete("Taches", "id", str(id_tache))
            print(id_tache)
               
        for tacheX in list:
            reussi = tacheX[1].get()
            tache = str(tacheX[3])    
            self.insererNouvelleTache(id_projet,id_utilisateur, id_sprint, tache, reussi)
               
       
       
       