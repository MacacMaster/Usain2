#-*- coding: utf-8 -*-



from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox

from datetime import datetime
from _overlapped import NULL

import socket
from xmlrpc.client import ServerProxy

from SprintModele  import *
from SprintVue  import *
 
    
 ##################################################
 #TODO:
 #
 #
 #
 #
 ################################################# 
  


class Controleur():
    def __init__(self):
        #try:
        '''
            #vraie version
        self.saasIP=str(sys.argv[1])
        self.utilisateur=sys.argv[2]
        self.id_Organisation=str(sys.argv[3])
        self.idProjet=str(sys.argv[4])
        self.clientIP=      sys.argv[5]
        self.portSaas=":9999"
        self.adresseServeur="http://"+self.saasIP+self.portSaas

        self.serveur = self.connectionServeur()
        
        
        self.modele=Modele(self)
        self.vue=Vue(self)
        
        self.writeLog("Ouverture du Module","2")
        self.vue.root.mainloop()
        '''     

       
        #version debug
        self.saasIP=socket.gethostbyname(socket.gethostname())
        self.adresseServeur="http://"+self.saasIP+":9999"
        self.idProjet= str(1)
        self.utilisateur=str(1)
        self.clientIP=socket.gethostbyname(socket.gethostname())
        self.id_Organisation = str(1)
        self.serveur = self.connectionServeur()
        self.modele=Modele(self, self.serveur)
        self.vue=Vue(self)
        self.vue.root.mainloop()


    def writeLog(self,action,codeid):
        self.serveur.writeLog(self.id_Organisation,self.utilisateur,self.clientIP,self.saasIP,"Sprint",action,codeid) 
        
    def connectionServeur(self):
        print("Connection au serveur BD...")
        serveur=ServerProxy(self.adresseServeur)
        return serveur
    
    def retournerLesTaches(self,id_sprint,id_utilisateur):
        return self.modele.retournerLesTaches(id_sprint,id_utilisateur)
    
    def retournerLesSprints(self):
        return self.modele.retournerLesSprints(self.idProjet)
    
    def retournerLesUtilisateurs(self):
        return self.modele.retournerLesUtilisateurs(self.id_Organisation)
    
    def insererNouvelleTache(self,id_utilisateur, id_sprint, tache, reussi):
        return self.modele.insererNouvelleTache(self.idProjet, id_utilisateur, id_sprint, tache, reussi)
    
    def enregistrer(self,list,id_utilisateur,id_sprint,jourSemaineValides):
        self.modele.enregistrer(self.idProjet,id_utilisateur,id_sprint,list, jourSemaineValides)
        
    def insererNouveauSprint(self,date_debut, date_fin, nom):
        self.modele.insererNouveauSprint(self.idProjet,date_debut, date_fin, nom)
        
    def retournerLeSprint(self,id_sprint):
        return self.modele.retournerLeSprint(id_sprint)
        
if __name__ == '__main__':
    #parent = serveur Saas
    c=Controleur()