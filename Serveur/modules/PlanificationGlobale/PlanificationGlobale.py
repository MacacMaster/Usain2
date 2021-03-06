#-*- coding: utf-8 -*-


from tkinter import *
from tkinter.filedialog import *

from datetime import datetime
from _overlapped import NULL

import socket
from xmlrpc.client import ServerProxy

from PlanificationGlobaleVue  import *
from PlanificationGlobaleModele  import *

#debug
from subprocess import Popen    
    
############################################################################
# Maintainer : M-A Ramsay
# 
############################################################################


class Controleur():
    def __init__(self):
        self.saasIP=        sys.argv[1]
        self.utilisateur=   sys.argv[2]
        self.organisation=  sys.argv[3]
        self.idProjet=      sys.argv[4]
        self.clientIP=      sys.argv[5]
        self.portSaas=":9999"
        self.adresseServeur="http://"+self.saasIP+self.portSaas
        
        self.serveur=self.connectionServeurSaas()
        self.modele=Modele(self)
        
        self.writeLog("Ouverture du Module","2")
        self.sql=SQL(self)

        #[r0=[c1,c2,c3...],R1...]
        self.listeFonctions=self.sql.selDonnees("*")
        #Calcule automatiquement      
        self.id = len(self.listeFonctions)


        self.vue=Vue(self)
        
        
        self.vue.root.mainloop()
        
    def fermerProgramme(self):
        self.writeLog("Fermeture du Module","3")
        self.vue.root.destroy()
        
    def writeLog(self,action,codeid):
         #print(self.getTime() + " "+self.organisation + " "+self.user + " "+self.clientip + " "+self.dbip + " "+module + " "+action)
        varwhatev=self.serveur.writeLog(self.organisation,self.utilisateur,self.clientIP,self.saasIP,"PlanificationGlobale",action,codeid)
        if (varwhatev):
            return True
        else :
            return False

    def creerFonction(self,sprint,nom,priorite,debut,fin):
        self.sql.creerFonction(sprint,nom,priorite,debut,fin)
        
    def suppressionFonction(self, fonct):
        self.sql.supressionFonction(fonct)
    
    def connectionServeurSaas(self):
        return ServerProxy(self.adresseServeur)
    
    def updateListe(self):
        self.listeFonctions=self.sql.selDonnees("*")
    
if __name__ == '__main__':
    #parent = serveur Saas
    c=Controleur()