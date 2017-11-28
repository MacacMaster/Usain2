#-*- coding: utf-8 -*-

from tkinter import *
from tkinter.filedialog import *

from datetime import datetime
from _overlapped import NULL

from PlanificationGlobaleVue  import *
from PlanificationGlobaleModele  import *
    
    
  
  


class Controleur():
    def __init__(self):
        for x in sys.argv:
            print (x)
        """
        self.saasIP=sys.argv[1]
        self.utilisateur=sys.argv[2]
        self.organisation=sys.argv[3]
        self.idProjet=sys.argv[4]
        self.clientIP=sys.argv[5]
        self.adresseServeur="http://"+self.saasIP+":9998"
"""
        self.modele=Modele(self)
        #self.serveur = self.connectionServeur()
        self.vue=Vue(self)
        self.vue.root.mainloop()
    
    def fermerProgramme(self):
        
        exit
        
    def writeLog(self,action="Actionman",module="Client"):
        #print(self.getTime() + " "+self.organisation + " "+self.user + " "+self.clientip + " "+self.dbip + " "+module + " "+action)
        self.parent.serveur.writeLog(self.modele.getTime(),self.organisation,self.user,self.clientip,self.dbip,module,action)

        
    
    def connectionServeurDB(self):
        print("Connection au serveur BD...")
        serveur=ServerProxy(self.adresseServeur)
        return serveur
        
if __name__ == '__main__':
    #parent = serveur Saas
    c=Controleur()