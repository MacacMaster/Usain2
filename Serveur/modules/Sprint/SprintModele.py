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
        champs = "tache, reussi"
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