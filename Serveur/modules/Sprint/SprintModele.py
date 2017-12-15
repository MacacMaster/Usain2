# -*- coding: utf-8 -*-

import sqlite3
from time import *
from Sprint  import *

#TODO - UPDATE

class Modele():
    def __init__(self, parent, serveur):
        self.serveur =serveur
        self.parent=parent

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
        champs = "id, nom, date_debut,date_fin"
        #champs = "date_debut,date_fin"
        where = ["id_projet"]
        valeur = [id_projet]
        
        #requete = self.parent.serveur.selDonneesWHERE(nomTable,champs,where,valeur)
        requete = self.parent.serveur.selDonneesWHERE_DATES(nomTable,champs,where,valeur)
        print(requete)
        return requete
    
    def retournerLeSprint(self,id_sprint):
        nomTable = "Sprints"
        champs = "id, nom, date_debut,date_fin"
        #champs = "date_debut,date_fin"
        where = ["id"]
        valeur = [ str(id_sprint)]
        
        #requete = self.parent.serveur.selDonneesWHERE(nomTable,champs,where,valeur)
        requete = self.parent.serveur.selDonneesWHERE(nomTable,champs,where,valeur)
        print(requete)
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
        
    def insererNouveauSprint(self, id_projet,date_debut, date_fin, nom):
        a1 = id_projet
        a2 = date_debut
        a3 = date_fin
        a4 = "Sprint "
        
        numeroNouveauSprint = len(self.retournerLesSprints(id_projet))
        a4 = a4 + str(numeroNouveauSprint)
        
        chaine = "'" + str(a1) + "','" +str(a2) + "','"  + str(a3)+ "','" +str(a4) +  "'"
        #projet utilisateur sprint tache reussi
        self.serveur.insertionSQL("Sprints", chaine)
        
    def enregistrer(self,id_projet,id_utilisateur,id_sprint,list):
        les_id_taches = self.retournerLesTaches(id_sprint,id_utilisateur)
        #effacer les tâches      
        for element in les_id_taches:
            id_tache = element[2]
            self.parent.serveur.delete("Taches", "id", str(id_tache))
               
        #recréer les tâches       
        for tacheX in list:
            reussi = tacheX[1].get()
            tache = str(tacheX[3])    
            self.insererNouvelleTache(id_projet,id_utilisateur, id_sprint, tache, reussi)
            
            semaine = tacheX[2]
            #insérer les données pour chaque jour de la semaine
            for jour in semaine:
                reussi = str(jour[4].get())
                prevu = str(jour[5].get())
                entry = str(jour[2].get())
                date = str(jour[3])
                idTache = tacheX[4]
                chaine = "'" + date + "','" +idTache + "','"  + prevu+ "','" +reussi +  "','" + entry + "'"
                self.serveur.insertionSQL("DateDeSprints",chaine)
       
       