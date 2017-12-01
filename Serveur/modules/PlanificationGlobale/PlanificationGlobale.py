#-*- coding: utf-8 -*-



from tkinter import *
from tkinter.filedialog import *

from datetime import datetime
from _overlapped import NULL

from xmlrpc.client import ServerProxy

from PlanificationGlobaleVue  import *
from PlanificationGlobaleModele  import *

#debug
from subprocess import Popen    
    
 ##################################################
 #TODO:
 #
 #Find why writeLog doesn't work
 #
 ################################################# 
  


class Controleur():
    def __init__(self):
            
               
        self.saasIP="10.57.47.7" #sys.argv[1]
        self.utilisateur="BOB"  #sys.argv[2]
        self.organisation="Organe"  #sys.argv[3]
        self.idProjet="123"   #sys.argv[4]
        self.clientIP="10.57.47.7"   #sys.argv[5]
        self.portSaas=":9999"
        self.adresseServeur="http://"+self.saasIP+self.portSaas
        
        self.serveur=self.connectionServeurSaas()
        self.modele=Modele(self)
        self.sql=SQL(self)

        self.vue=Vue(self)

        self.writeLog("Ouverture du Module")

        
        self.listeFonctions=self.sql.selDonnees("nom")
        
        #self.sql.creerFonction("Sprint 1","FonctionNom","priorite","debut","fin")
        self.sql.calculPourcent()
        self.vue.root.mainloop()
        
    def fermerProgramme(self):
        self.writeLog("Fermeture du Module")
        self.vue.root.destroy()
        
    def writeLog(self,action):
         #print(self.getTime() + " "+self.organisation + " "+self.user + " "+self.clientip + " "+self.dbip + " "+module + " "+action)
        varwhatev=self.serveur.writeLog(self.modele.getTime(),self.organisation,self.utilisateur,self.clientIP,self.saasIP,"PlanificationGlobale",action)
        if (varwhatev):
            return True
        else :
            return False

    def creerFonction(self,sprint,nom,priorite,debut,fin):
        self.sql.creerFonction(sprint,nom,priorite,debut,fin)
        
    def suppressionFonction(self):
        self.sql.suppressionFonction()
    
    def connectionServeurSaas(self):
        print("Connection au serveur Saas...")
        return ServerProxy(self.adresseServeur)
    
        
if __name__ == '__main__':
    #parent = serveur Saas
    c=Controleur()