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
        id_utilisateur = str(1)
        id_sprint = str(1)
        nomTable = "Taches"
        champs = "tache, reussi"
        where = ["id_utilisateur", "id_sprint"]
        valeur = [id_utilisateur,id_sprint]
        
        requete = self.parent.serveur.selDonneesWHERE(nomTable,champs,where,valeur)
        print("fonction sql appelée")
        return requete