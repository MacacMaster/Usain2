#-*- coding: utf-8 -*-

from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
 #création de l'objet qui écoute  Q
import socket
import sqlite3
from xmlrpc.client import ServerProxy
from subprocess import Popen
import os

class Client(object):
    def __init__(self,nom, id):
        self.nom=nom #nom usager
        self.id = id #id orga
        self.cadreCourant=0
        self.cadreEnAttenteMax=0
        self.actionsEnAttentes={}
        
        
class ModeleService(object):
    def __init__(self,pControleur):
        self.controleur=pControleur
        #{Clé outils disponible:}
        self.projetsdisponibles={}
        self.modulesdisponibles={"Mandat":"Mandat",
                                 "CasUsage":"CasUsage",
                                 "Maquette":"Maquette",
                                 "Modelisation":"Modelisation",
                                 "CRC":"CRC",
                                 "PlanificationGlobale":"PlanificationGlobale"}

        self.outilsdisponibles={"meta_sql": "meta_sql"}
        self.clients={}

    def creerclient(self,nom, id):
        if nom in self.clients.keys(): # on assure un nom unique
            return [0,"Simulation deja en cours"]
        # tout va bien on cree le client et lui retourne la seed pour le random
        c=Client(nom, id)
        self.clients[nom]=c
        tabProjet = self.controleur.rechercheProjetsDispo(id)
        for i in tabProjet:
            self.projetsdisponibles[i] = i
        for i in self.projetsdisponibles:
            print (i)
        
        return [c.id,
                c.nom,
                list(self.modulesdisponibles.keys()),
                list(self.outilsdisponibles.keys()),
                list(self.projetsdisponibles.keys())
                ]
        
class ControleurServeur():
    def __init__(self):
        self.modele= ModeleService(self)
        self.ipServeurBd = None
        self.serveurBD=None
        
    def logInServeur(self, pUsagerIP, pIdentifiantNomUsager, pIdentifiantNomOrga, pIdentifiantMotDePasse):
        #Connection au serveurDB
        self.ipServeurBd="http://"+pUsagerIP+":9998"
        print("Connection au serveur BD...")
        self.serveurBD=ServerProxy(self.ipServeurBd,allow_none = 1) #self.serveurBD=ServerProxy(ad,allow_none = 1)        print("Connection serveur BD réussi")
        
        #variables id
        identifiantNomUsager = pIdentifiantNomUsager
        identifiantNomOrga = pIdentifiantNomOrga
        identifiantMotDePasse = pIdentifiantMotDePasse
		#rep = self.serveurBD.selDonnees("Projets", "Nom")        clientTempo = self.chercherClientBD(identifiantNomUsager, identifiantNomOrga, identifiantMotDePasse)
        clientTempo = self.chercherClientBD(identifiantNomUsager, identifiantNomOrga, identifiantMotDePasse)
        if (clientTempo == 0):
            return 0
        else:
            print("Recherche du client terminé. Il s'agit de", clientTempo[0], "qui appartient a l'organisation numero ", clientTempo[1])
            client = self.modele.creerclient(clientTempo[0], clientTempo[1])
            return [client, clientTempo[1]]

    def rechercheProjetsDispo(self, id):
        tabProjet = self.serveurBD.rechercheProjetsDispo(id)
        return tabProjet
    
    def chargerProjet(self, nomprojet, idorga):
        idProjet = self.serveurBD.chargerProjet(nomprojet, idorga)
        return idProjet
        
        
    def finDuProgramme(self):
        daemon.shutdown()
        
    def chercherClientBD(self, pIdentifiantNom, pIdenfiantOrga, pIdentifiantMotDePasse):
        nomClientTempo = self.serveurBD.chercherClientBD(pIdentifiantNom, pIdenfiantOrga, pIdentifiantMotDePasse)
        return nomClientTempo
    
    def requeteModule(self,mod):
        if mod in self.modele.modulesdisponibles.keys():
            cwd=os.getcwd()
            #print(mod,os.getcwd())
            if os.path.exists(cwd+"/modules/"):
                dirmod=cwd+"/modules/"+self.modele.modulesdisponibles[mod]+"/"
                if os.path.exists(dirmod):
                    #print("TROUVE")
                    listefichiers=[]
                    for i in os.listdir(dirmod):
                        if os.path.isfile(dirmod+i):
                            val=["fichier",i]
                        else:
                            val=["dossier",i]
                            
                        listefichiers.append(val)
                    return [mod,dirmod,listefichiers]
                
    def requeteOutil(self,mod):
        if mod in self.modele.outilsdisponibles.keys():
            cwd=os.getcwd()
            #print(mod,os.getcwd())
            if os.path.exists(cwd+"/outils/"):
                dirmod=cwd+"/outils/"+self.modele.outilsdisponibles[mod]+"/"
                if os.path.exists(dirmod):
                    #print("TROUVE")
                    listefichiers=[]
                    for i in os.listdir(dirmod):
                        if os.path.isfile(dirmod+i):
                            val=["fichier",i]
                        else:
                            val=["dossier",i]
                            
                        listefichiers.append(val)
                    return [mod,dirmod,listefichiers]
                
                
    def requeteFichier(self,lieu):
        fiche=open(lieu,"rb")
        contenu=fiche.read()
        fiche.close()
        return xmlrpc.client.Binary(contenu)
    
    #Fonction d'écriture du log        
    def writeLog(self,date,org,user,ip,db,module,action):
        logLocation='Logs.sqlite'
        logdb = sqlite3.connect(logLocation)
        curseur = logdb.cursor()
        curseur.execute("INSERT INTO logs VALUES(?,?,?,?,?,?,?)", (date,org,user,ip,db,module,action,))
        logdb.commit()
        logdb.close()
        return True 
    
print("Création du serveur...")
daemon = SimpleXMLRPCServer((socket.gethostbyname(socket.gethostname()),9999),allow_none = 1)
objetControleurServeur=ControleurServeur()
daemon.register_instance(objetControleurServeur)
print("Création du serveur terminé")
daemon.serve_forever()
