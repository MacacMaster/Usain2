#-*- coding: utf-8 -*-

from xmlrpc.server import SimpleXMLRPCServer
 #création de l'objet qui écoute  Q
import socket
import sqlite3
from IdMaker import *



class ControleurServeurBD():
    def __init__(self):
        self.database = sqlite3.connect('SprintMasterData.db')
        self.curseur = self.database.cursor()
        self.id=0
        
        
        
    def insDonnees(self,nomTable,valeurs):
        conn= sqlite3.connect('SprintMasterData.db')
        c = conn.cursor()
        self.id+=1
        c.execute('''INSERT into '''+nomTable+''' VALUES (''' +str(self.id)+', '+valeurs+''' )''')
        conn.commit()
        conn.close()
    
    def selDonnees(self,nomTable,champs):
        conn= sqlite3.connect('SprintMasterData.db')
        c = conn.cursor()
        c.execute('''SELECT ''' +champs+ ''' from '''+nomTable)
        donnees = c.fetchall()
        print(donnees)
        conn.close()
        return donnees

        
    def updateDonnees(self,nomTable,champ,description,where,where2,indice1,indice2):
        conn= sqlite3.connect('SprintMasterData.db')
        c = conn.cursor()
        c.execute('''UPDATE '''+ nomTable+ ''' SET '''+ description +''' =? WHERE '''+ where+''' =? and '''+where2 +''' =? ''', (champ,indice1,indice2))
        conn.commit()
        conn.close()
    
    def selDonneesComplexe1(self,nomTable,champs,where,indice):
        conn= sqlite3.connect('SprintMasterData.db')
        c = conn.cursor()
        c.execute('''SELECT '''+ champs +''' FROM '''+nomTable+''' WHERE '''+where +'''=?''', (indice))
        donnees = c.fetchall()
        conn.close()
        return donnees
    
    def selDonneesComplexe2(self,nomTable,champs,un,deux,indice1,indice2):
        conn= sqlite3.connect('SprintMasterData.db')
        c = conn.cursor()
        c.execute('''SELECT '''+ champs +''' FROM '''+nomTable+''' WHERE '''+ un +'''=? and '''+deux+''' =?''' , (indice1,indice2))
        donnees = c.fetchall()
        conn.close()
        return donnees
    
    def chargerProjet(self, nomprojet, idorga):
        nomProjetBD = ''+nomprojet+''
        idOrgaBD = ''+idorga+''
        
        print(nomProjetBD)
        print(idOrgaBD)
        idProjet = self.curseur.execute("SELECT id FROM Projets WHERE id_Organisation = ? and nom = ? ", (idOrgaBD, nomProjetBD)).fetchone()
        print("L'id du projet séléctionné est", str(idProjet)[1:len(idProjet)-3])
        return str(idProjet)[1:len(idProjet)-3]
    
    def chercherClientBD(self, pIdentifiantNom, pIdentifiantOrga, pIdentifiantMotDePasse):
        nomOrgaExiste = False
        nomUsaExiste = False
        mdpExiste = False
        idOrga = None
        idUsager = None
        
        for orga in self.curseur.execute('SELECT nom FROM Organisations'):
            #print(str(orga)[2:len(orga)-4])
            if (str(orga)[2:int(len(orga)-4)] == pIdentifiantOrga):
                nomOrga = (''+pIdentifiantOrga+'',)
                idOrga = self.curseur.execute("SELECT id FROM Organisations WHERE nom = ?", nomOrga).fetchone()
                print("id de l'organisation : ", str(idOrga)[1:len(idOrga)-3])
                nomOrgaExiste = True
                break
        
        if nomOrgaExiste:
            
            for usager in self.curseur.execute("SELECT nom FROM Usagers WHERE id_Organisation = ?", idOrga):
                #print(str(usager)[2:len(usager)-4])
                if (str(usager)[2:int(len(usager)-4)] == pIdentifiantNom):
                    nomUsager = (''+pIdentifiantNom+'',)
                    idUsager = self.curseur.execute("SELECT id FROM Usagers WHERE nom = ?", nomUsager).fetchone()
                    print("id de l'usager : ", str(idUsager)[1:len(idUsager)-3])
                    nomUsaExiste = True
                    break
                
            if nomUsaExiste:
                
                for mdp in self.curseur.execute("SELECT motDePasse FROM Usagers WHERE id = ?", idUsager):
                    print(str(mdp)[2:len(mdp)-4])
                    if (str(mdp)[2:len(mdp)-4] == pIdentifiantMotDePasse):
                        mdpExiste = True
                        break
                    
                if mdpExiste:
                    print("Réussite de l'authentification")
                    return [pIdentifiantNom, str(idOrga)[1:len(idOrga)-3]]
                
                else:
                    print("Echec de l'authentification")
                    return 0
                    
            else:
                print("Echec de l'authentification")
                return 0
                
        else:
            print("Echec de l'authentification")
            return 0
        

         

    def rechercheProjetsDispo(self, id):
        print("je cherche des projets")
        t = (''+str(id)+'',)
        tabProjet = []
        for projet in self.curseur.execute('SELECT nom FROM Projets WHERE id_Organisation =?', t):
            print (str(projet)[2:len(projet)-4])
            tabProjet.append(str(projet)[2:len(projet)-4])
        return tabProjet

    
    
print("Création du serveur pour la BD...")
daemon = SimpleXMLRPCServer((socket.gethostbyname(socket.gethostname()),9998),allow_none = 1)
objetControleurServeurBD=ControleurServeurBD()
daemon.register_instance(objetControleurServeurBD)
print("Création du serveur BD terminé")
daemon.serve_forever()



