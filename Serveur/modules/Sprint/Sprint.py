#-*- coding: utf-8 -*-



from tkinter import *
from tkinter.filedialog import *

from datetime import datetime
from _overlapped import NULL

import socket
from xmlrpc.client import ServerProxy

from SprintModele  import *
from SprintVue  import *

#debug
from subprocess import Popen    
    
 ##################################################
 #TODO:
 #
 #
 #
 #
 ################################################# 
  


class Controleur():
    def __init__(self):
        '''
        #vraie version
        self.saasIP=sys.argv[1]
        self.utilisateur=sys.argv[2]
        self.organisation=sys.argv[3]
        self.idProjet=sys.argv[4]
        self.clientIP=sys.argv[5]
        self.adresseServeur="http://"+self.saasIP+":9999"
        
        self.modele=Modele(self)
        self.serveur = self.connectionServeur()
        self.vue=Vue(self)
        self.vue.root.mainloop()   
        '''
        #version debug
        self.saasIP=socket.gethostbyname(socket.gethostname())
        self.adresseServeur="http://"+self.saasIP+":9999"
        self.idProjet= 1
        self.serveur = self.connectionServeur()
        self.modele=Modele(self,self.serveur)
        self.vue=Vue(self)
        self.vue.root.mainloop()
        
        
    def fermerProgramme(self):
        self.writeLog("Fermeture du Module","M63")
        self.vue.root.destroy()
        
    def connectionServeur(self):
        print("Connection au serveur BD...")
        serveur=ServerProxy(self.adresseServeur)
        return serveur
    
    def retournerLesTaches(self,id_sprint,id_utilisateur):
        return self.modele.retournerLesTaches(id_sprint,id_utilisateur)
        
if __name__ == '__main__':
    #parent = serveur Saas
    c=Controleur()