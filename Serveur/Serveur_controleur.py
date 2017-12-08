#-*- coding: utf-8 -*-
######################################################
# Pour utiliser les fonctions de sélection ou d'insertion
# dans les modules
# 1) s'assurer d'avoir un lien avec le serveur (voir client)
#2) appeler la fonction de serveur:
#      ex:  self.serveur.insertionSQL("Organisations", " 4, 'allo' ")
# Premier paramètre est le nom de la table en string, le deuxième est un long string qui est la liste des valeurs à ajouter. Si cette liste a des string, les mettre entre ' ' .
#        self.selDonnees("Organisations","id, nom")
#Les ids uniquies sont pris en charge avec la fonction
# 
# ex: self.serveur.selectionSQL("Projets","id")
#        Premier paramètre est le nom de la table en string, puis la liste des colonnes dont vous voulez les données
#        Cette fonction a encore un print, vous verrez donc son résultat.
#        Cette fonction retourne une liste, il vous faudra donc aller sélectionner spécifiquement le champ recherché
######################################################
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
 #création de l'objet qui écoute  Q
import socket
import sqlite3
from xmlrpc.client import ServerProxy
from subprocess import Popen
import os

class Client(object):
    def __init__(self,nom, idOrga, id):
        self.nom=nom #nom usager
        self.idOrga = idOrga
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

    def creerclient(self,nom, idOrga, id):
        if id in self.clients.keys(): # on assure un nom unique
            return [0,"Simulation deja en cours"]
        # tout va bien on cree le client et lui retourne la seed pour le random
        c=Client(nom, idOrga, id)
        self.clients[id]=c
        tabProjet = self.controleur.rechercheProjetsDispo(idOrga)
        for i in tabProjet:
            self.projetsdisponibles[i] = i
        for i in self.projetsdisponibles:
            print (i)
        
        return [c.id,
                c.nom,
                list(self.modulesdisponibles.keys()),
                list(self.outilsdisponibles.keys()),
                list(self.projetsdisponibles.keys())]
        
class ControleurServeur():
    def __init__(self):
        self.modele= ModeleService(self)
        self.ipServeurBd = None
        self.serveurBD=None
        self.nomUsager=""
        
    def logInServeur(self, pUsagerIP, pIdentifiantNomUsager, pIdentifiantNomOrga, pIdentifiantMotDePasse):
        #Connection au serveurDB
        print("Connexion au serveur BD...")
        self.ipServeurBd = "http://"+pUsagerIP+":9998"
        self.serveurBD=ServerProxy(self.ipServeurBd,allow_none = 1)
        print("Connexion au serveur BD réussie")

       
       
        
        #variables id
        self.nomUsager = pIdentifiantNomUsager
        identifiantNomUsager = pIdentifiantNomUsager
        identifiantNomOrga = pIdentifiantNomOrga
        identifiantMotDePasse = pIdentifiantMotDePasse
		#rep = self.serveurBD.selDonnees("Projets", "Nom")        
        clientTempo = self.chercherClientBD(identifiantNomUsager, identifiantNomOrga, identifiantMotDePasse)
        if (clientTempo == 0):
            return 0
        else:
            print("Recherche du client terminé. Il s'agit de", clientTempo[0], "qui appartient a l'organisation numero ", clientTempo[1])
            client = self.modele.creerclient(clientTempo[0], clientTempo[1], clientTempo[2])
            return [client, clientTempo[1]]
        
        

    def rechercheProjetsDispo(self, id):
        tabProjet = self.serveurBD.rechercheProjetsDispo(id)
        return tabProjet
    
    def chargerProjet(self, nomprojet, idorga):
        idProjet = self.serveurBD.chargerProjet(nomprojet, idorga)
        return idProjet
        
    def fermeture(self, nomUtilisateur):
        print("Ne ferme pas")
        if nomUtilisateur == self.nomUsager:
            self.nomUsager=""
        
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
    
    def insertionSQL(self,nomTable,valeurs):
        return self.serveurBD.insDonnees(nomTable, valeurs)
    
    #Gestion ID Manuelle M-A
    def insDonneesPlanif(self,tableau,params):
        return self.serveurBD.insDonneesPlanif(tableau,params)
    
    def selectionSQL1(self,nomTable,champs,where,indice):
        return self.serveurBD.selDonnees3(self,nomTable,champs,where,indice)
    
    def selectionSQL2(self,nomTable,champs,un,deux,indice1,indice2):
        return self.serveurBD.selDonneesComplexe2(nomTable,champs,un,deux,indice1,indice2)
    
    def selectionSQL3(self,nomTable,champs, where, idProjet):
        return self.serveurBD.selDonnees3(nomTable,champs, where, idProjet)
    
    def selDonneesWHERE(self,nomTable,champs,where,valeur):
        return self.serveurBD.selDonneesWHERE(nomTable,champs,where,valeur)
    
    def selectionSQL(self,nomTable,champs):
        return self.serveurBD.selDonnees(nomTable,champs)
    
    
    def updateSQL(self,nomTable,champs,valeur):
        self.serveurBD.updateDonnes(nomTable,champs,valeur)
        return self.serveurBD.selDonneesComplexe1(nomTable,champs,where,indice)
    
    def updateSQL2(self,nomTable,champ,description,where,indice1):
        return self.serveurBD.updateDonnees2(nomTable,champ,description,where,indice1)
    
    def insCustom(self,commande,values):
        self.serveurBD.insCustom(self,commande,values)    
        
        
    def delete(self, nomTable, where, condition):
        self.serveurBD.delete(nomTable, where, condition)
        
    def verificationExiste(self, champVerifier, tableVerifier, quoi, egaleQuoi, valeur):
        return self.serveurBD.verificationExiste(champVerifier, tableVerifier, quoi, egaleQuoi, valeur)
    
    #Fonction d'écriture du log        
    def writeLog(self,date,org,user,ip,db,module,action):
        logLocation='Logs.sqlite'
        print ("Log Open")
        logdb = sqlite3.connect(logLocation)
        curseur = logdb.cursor()
        curseur.execute("INSERT INTO logs VALUES(?,?,?,?,?,?,?)", (date,org,user,ip,db,module,action,))
        logdb.commit()
        logdb.close()
        print ("Log Close")
        return True 
    
    
print("Création du serveur...")
daemon = SimpleXMLRPCServer((socket.gethostbyname(socket.gethostname()),9999),allow_none = 1)
objetControleurServeur=ControleurServeur()
daemon.register_instance(objetControleurServeur)
print("Création du serveur terminé")
daemon.serve_forever()

