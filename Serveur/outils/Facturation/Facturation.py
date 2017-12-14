# -*- coding: utf-8 -*-

import os,os.path
import sys
import Pyro4
import socket
from subprocess import Popen 
import math
from xmlrpc.client import ServerProxy
from Facturation_vue import *
from IdMaker import Id

class Controleur():
    def __init__(self):
        print("Controleur")
        self.createurId=Id
        self.modele=None
        
        self.saasIP=  sys.argv[1]
        self.utilisateur=  sys.argv[2]
        self.organisation=  sys.argv[3]
        self.clientIP=  sys.argv[4]
        self.portSaas=":9999"
        self.adresseServeur="http://"+self.saasIP+self.portSaas
        self.serveur = self.connexionSaas()
        self.vue=Vue(self)
        self.vue.root.mainloop()
        
    def connexionSaas(self):
        return ServerProxy(self.adresseServeur, allow_none =1)
        
        
    
if __name__ == '__main__':
    c=Controleur()