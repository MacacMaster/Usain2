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
        self.saasIP= socket.gethostbyname(socket.gethostname())     #sys.argv[1]
        self.utilisateur="BOB"          #sys.argv[2]
        self.organisation="Organe"      #sys.argv[3]
        self.idProjet="1"             #sys.argv[4]
        self.clientIP="10.57.47.7"      #sys.argv[5]
        self.portSaas = "9999"
        self.adresseServeur="http://"+self.saasIP+self.portSaas

        '''
        self.saasIP=        sys.argv[1]
        self.utilisateur=   sys.argv[2]
        self.organisation=  sys.argv[3]
        self.idProjet=      sys.argv[4]
        self.clientIP=      sys.argv[5]
        self.portSaas=":9999"
        self.adresseServeur="http://"+self.saasIP+self.portSaas
        '''
        
        self.serveur=self.connectionServeurSaas()
        self.modele=Modele(self)


        self.vue=Vue(self)       
        self.vue.root.mainloop()
        
    def fermerProgramme(self):
        self.writeLog("Fermeture du Module","M63")
        self.vue.root.destroy()
        
    def connectionServeurSaas(self):
        print("Connection au serveur Saas...")
        return ServerProxy(self.adresseServeur)

if __name__ == '__main__':
    #parent = serveur Saas
    c=Controleur()