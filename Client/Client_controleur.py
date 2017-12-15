# -*- coding: utf-8 -*-

from Client_modele  import *
from Client_vue import *
from Client_log import *
import socket
from xmlrpc.client import ServerProxy
from subprocess import Popen
import os


class Controleur():
    def __init__(self):
        #Debug: Ouvre automatiquement le Serveur Controleur  
        pid1 = Popen(["C:\\Python34\\Python.exe", "../Serveur/Serveur_controleur.py"],cwd='../Serveur',shell=1).pid
        pid2 = Popen(["C:\\Python34\\Python.exe", "../SQL Serveur/ServeurBD_controleur.py"],cwd='../SQL Serveur',shell=1).pid 

        
        self.clientIP = self.chercherIP()
        #IP Saas
        self.saasIP=self.clientIP
        self.serveur=None
        self.log=Log(self,self.clientIP)#,self.serveur)
        #string utilisateur et organisation
        self.utilisateur="None"
        self.organisation=None
        self.idOrga=None
        self.utilisateurId = None
        #id du projet selectionne
        self.idProjet=None
        self.vue=Vue(self,self.clientIP)
        
        self.vue.root.mainloop()

    
    def chargerProjet(self, nomprojet):
        idProjet = self.serveur.chargerProjet(nomprojet, self.idOrga)
        self.idProjet = idProjet
        self.log.writeLog("Projet ID: "+str(idProjet),"PE0")
        return idProjet
    
    #trouve l'IP du client
    def chercherIP(self):
        clientIP = socket.gethostbyname(socket.gethostname())
        return clientIP

    def fermerApplication(self):
        if self.serveur:
            self.log.writeLog("Fermeture du Client","L03")
            self.serveur.fermeture(self.utilisateurId)
        self.vue.root.destroy()

    def logInClient(self, pIdentifiantNomUsager, pIdentifiantNomOrga, pIdentifiantMotDePasse):
        #Vérification des informations avant l'envoi au serveur
        if (pIdentifiantNomOrga !="" and pIdentifiantNomUsager !="" and pIdentifiantMotDePasse !="" ):
            #connection au Serveur
            ad="http://"+self.saasIP+":9999"
            self.serveur=ServerProxy(ad,allow_none = 1)
            #Needs those Var for LOGS
            self.log.setLog( pIdentifiantNomOrga, pIdentifiantNomUsager, )
            reponseServeur = self.serveur.logInServeur(self.clientIP, pIdentifiantNomUsager, pIdentifiantNomOrga, pIdentifiantMotDePasse)
    
            
            if (reponseServeur == 0):
                self.log.writeLog("Login Fail")
                self.vue.logInClientFail(0)
            elif reponseServeur == "Simulation deja en cours":
                self.log.writeLog("Tentative de connexions multiple")
                self.vue.logInClientFail(1)
            else:
                self.utilisateurId = reponseServeur[0][0]
                self.utilisateur=pIdentifiantNomUsager
                self.organisation=pIdentifiantNomOrga
                self.log.writeLog("Login Successful","L00")
                self.idOrga = reponseServeur[1]
                self.vue.chargerCentral(reponseServeur[0][1],reponseServeur[0][2],reponseServeur[0][3],reponseServeur[0][4])
        else:
            self.vue.logInClientFail(2)

        
    def creerProjet(self,nom):
        
            self.serveur.insertionSQL("Projets","'"+str(self.idOrga)+"','"+nom+"'")
            
    def requeteModule(self,mod):
        rep=self.serveur.requeteModule(mod)
        if rep:
            cwd=os.getcwd()
            lieuApp="/"+rep[0]
            lieu=cwd+lieuApp
            if not os.path.exists(lieu):
                os.mkdir(lieu) #plante s'il existe deja
            reso=rep[1]
            for i in rep[2]:
                if i[0]=="fichier":
                    nom=reso+i[1]
                    rep=self.serveur.requeteFichier(nom)
                    fiche=open(lieu+"/"+i[1],"wb")
                    fiche.write(rep.data)
                    fiche.close()
            chaineappli="."+lieuApp+lieuApp+".py"
            #Arguments####################################################################################
            # self.saasIP=      sys.argv[1]
            # self.utilisateur= sys.argv[2]
            # self.organisation=sys.argv[3]
            # self.idProjet=    sys.argv[4]
            # self.clientIP=    sys.argv[5]
            ############################################################
            #argumentsServeur=[self.saasIP," ",self.utilisateur,self.organisation,self.idProjet]
            
            #Ouvre le programme telecharge
            pid = Popen(["C:\\Python34\\Python.exe", chaineappli,self.saasIP,self.utilisateur,self.organisation,self.idProjet,self.clientIP],shell=1).pid 
            #pid = Popen(["C:\\Python34\\Python.exe", chaineappli,argumentsServeur],shell=1).pid 
            #pid = Popen(["C:\\Python34\\Python.exe", chaineappli],shell=1).pid
        else:
            print("Pas de connexion")
            
               
    def requeteOutil(self,mod):
        rep=self.serveur.requeteOutil(mod)
        if rep:
            cwd=os.getcwd()
            lieuApp="/"+rep[0]
            lieu=cwd+lieuApp
            if not os.path.exists(lieu):
                os.mkdir(lieu) #plante s'il exist deja
            reso=rep[1]
            for i in rep[2]:
                if i[0]=="fichier":
                    nom=reso+i[1]
                    rep=self.serveur.requeteFichier(nom)
                    fiche=open(lieu+"/"+i[1],"wb")
                    fiche.write(rep.data)
                    fiche.close()
            chaineappli="."+lieuApp+lieuApp+".py"
            pid = Popen(["C:\\Python34\\Python.exe", chaineappli,self.saasIP,self.utilisateur,self.organisation,self.clientIP],shell=1).pid 
        else:
            print("Pas de connexion")
            
if __name__=="__main__":
    c=Controleur()
    