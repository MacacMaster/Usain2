#-*- coding: utf-8 -*-

from xmlrpc.server import SimpleXMLRPCServer
import socket
import sqlite3
from IdMaker import *

class ControleurServeurBD():
    def __init__(self):
        self.database = sqlite3.connect('SprintMasterData.db')
        self.curseur = self.database.cursor()
        self.id=0
        
    #test pour envoyer une commande fait a la main -M-A
    #https://stackoverflow.com/questions/21142531/sqlite3-operationalerror-no-such-column
#     def insCustom(self,commande,values):
#         conn= sqlite3.connect('SprintMasterData.db')
#         c = conn.cursor()
#         params = (userName, password, confirmPassword, firstName, lastName,
#           companyName, email, phoneNumber, addressLine1, addressLine2, 
#           addressLine3, zipCode, province, country, regDate)
#         c.execute("INSERT INTO"+ People+"VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params) 
#         self.id+=1
#         c.execute(commande, (self.id, values[0],values[1],values[2],values[3],values[4],values[5],values[6],values[7],))
#         conn.commit()
#         conn.close()

                
    def selDonneesWHERE_DATES(self,nomTable,champs,where,valeur):
        conn= sqlite3.connect( 'SprintMasterData.db',detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        c = conn.cursor()
        
        codeDate = ''' as "[date]"'''
        #batir la chaine sql
        sql = """SELECT """ 
        sql += champs
        sql += " FROM "
        sql += nomTable
        sql += codeDate
        sql += " WHERE "
        
        for i in range(len(where)):
            sql+= where[i] 
            sql+= "='"
            sql+= valeur[i] 
            sql+= "' "
            if (len(where) == i+1):
                pass
            else:
                sql+= "AND "
            
        c.execute(sql)
        laselection=c.fetchall()
        conn.close()
        return laselection

    def commandeAdmin(self,valeurs):
        conn= sqlite3.connect('SprintMasterData.db')
        c = conn.cursor()
        c.execute(valeurs)
        conn.commit()
        conn.close()
    
    def insDonnees(self,nomTable,valeurs):
        conn= sqlite3.connect('SprintMasterData.db')
        c = conn.cursor()
        c.execute('''INSERT into '''+nomTable+''' VALUES ('''+'NULL'+', '+valeurs+''' )''')
        c.execute('''SELECT last_insert_rowid()''')
        id = c.fetchone()[0]
        conn.commit()
        conn.close()
        return id
    
    #M-A id est un argument Facultatif 
    #def insDonneesPlanif(self,id,idprojet,idsprint,idresponsable,priorite,debut,fin):
    def insDonneesPlanif(self,tableau,params):
        conn= sqlite3.connect('SprintMasterData.db')
        c = conn.cursor()
        c.execute('''INSERT into '''+ tableau +''' VALUES (?,?,?,?,?,?,?,?)''',params)
        conn.commit()
        conn.close()
        return self.id
        
    def selDonnees(self,nomTable,champs):
        conn= sqlite3.connect('SprintMasterData.db')
        c = conn.cursor()
        sql = '''SELECT ''' +champs+ ''' from '''+nomTable
        c.execute(sql)
        donnees = c.fetchall()
        conn.close()
        return donnees
        
    def updateDonnees(self,nomTable,champ,description,where,where2,indice1,indice2):
        conn= sqlite3.connect('SprintMasterData.db')
        c = conn.cursor()
        c.execute('''UPDATE '''+ nomTable+ ''' SET '''+ description +''' =? WHERE '''+ where+''' =? and '''+where2 +''' =? ''', (champ,indice1,indice2))
        conn.commit()
        conn.close()
        
    def updateDonnees2(self,nomTable,champ,description,where,indice1):
        conn= sqlite3.connect('SprintMasterData.db')
        c = conn.cursor()
        c.execute('''UPDATE '''+ nomTable+ ''' SET '''+ description +''' =? WHERE '''+ where+''' =?''', (champ,indice1))
        conn.commit()
        conn.close()
        return True
    
    def selDonneesComplexe1(self,nomTable,champs):
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
    
    def selDonnees3(self,nomTable,champs, where, id):
        conn= sqlite3.connect('SprintMasterData.db')
        c = conn.cursor()
        c.execute('''SELECT ''' +champs+ ''' from '''+nomTable + ''' where ''' +where + '''=?''', (id,))
        laselection=c.fetchall()
        conn.close()
        return laselection
    
    def verificationExiste(self, champVerifier, tableVerifier, quoi, egaleQuoi, valeur):
        conn = sqlite3.connect('SprintMasterData.db')
        c = conn.cursor()
        c.execute(''' SELECT ''' + champVerifier + ''' FROM ''' + tableVerifier + ''' WHERE ''' + quoi + '''=?''' , (egaleQuoi,))
        laSelection = c.fetchall()
        conn.close()
        for s in laSelection:
            s=str(s)[2:int(len(s)-4)]
            if s == valeur:
                return False
        return True
    
    def selDonneesWHERE(self,nomTable,champs,where,valeur):
        conn= sqlite3.connect('SprintMasterData.db')
        c = conn.cursor()
        sql = """SELECT """ 
        sql += champs
        sql += " FROM "
        sql += nomTable
        sql += " WHERE "
        
        for i in range(len(where)):
            sql+= where[i] 
            sql+= "='"
            sql+= valeur[i] 
            sql+= "' "
            if (len(where) == i+1):
                pass
            else:
                sql+= "AND "

        c.execute(sql)
        laselection=c.fetchall()
        
        conn.close()
        return laselection
    
    def delete(self, nomTable, where, condition):
        conn= sqlite3.connect('SprintMasterData.db')
        c = conn.cursor()
        c.execute('''DELETE FROM ''' +nomTable + ''' where ''' +where + '''=?''', (condition,))
        conn.commit()
        conn.close()   
    
    def chargerProjet(self, nomprojet, idorga):
        nomProjetBD = ''+nomprojet+''
        idOrgaBD = ''+idorga+''
        idProjet = self.curseur.execute("SELECT id FROM Projets WHERE id_Organisation = ? and nom = ? ", (idOrgaBD, nomProjetBD)).fetchone()
        return str(idProjet)[1:len(idProjet)-3]
        
    
    def chercherClientBD(self, pIdentifiantNom, pIdentifiantOrga, pIdentifiantMotDePasse):
        nomOrgaExiste = False
        nomUsaExiste = False
        mdpExiste = False
        idOrga = None
        idUsager = None
        
        for orga in self.curseur.execute('SELECT nom FROM Organisations'):
            if (str(orga)[2:int(len(orga)-4)] == pIdentifiantOrga):
                nomOrga = (''+pIdentifiantOrga+'',)
                idOrga = self.curseur.execute("SELECT id FROM Organisations WHERE nom = ?", nomOrga).fetchone()
                nomOrgaExiste = True
                break
        
        if nomOrgaExiste:
            sql1="SELECT nom FROM Usagers WHERE id_Organisation = '"+str(idOrga)[1:len(idOrga)-3]+"'"
            for usager in self.curseur.execute(sql1).fetchall():
                if (str(usager)[2:int(len(usager)-4)] == pIdentifiantNom):
                    sqlt = "SELECT id FROM Usagers WHERE nom = '"+pIdentifiantNom+"' and id_Organisation = '"+str(idOrga)[1:len(idOrga)-3]+"'"
                    idUsager = self.curseur.execute(sqlt).fetchone()
                    nomUsaExiste = True
                    break
                
            if nomUsaExiste:
                
                for mdp in self.curseur.execute("SELECT motDePasse FROM Usagers WHERE id = ?", idUsager):
                    if (str(mdp)[2:len(mdp)-4] == pIdentifiantMotDePasse):
                        mdpExiste = True
                        break
                    
                if mdpExiste:
                    return [pIdentifiantNom, str(idOrga)[1:len(idOrga)-3], str(idUsager)[1:len(idUsager)-3]]
                
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
        t = (''+str(id)+'',)
        tabProjet = []
        for projet in self.curseur.execute('SELECT nom FROM Projets WHERE id_Organisation =?', t):
            tabProjet.append(str(projet)[2:len(projet)-4])
        return tabProjet
    
daemon = SimpleXMLRPCServer((socket.gethostbyname(socket.gethostname()),9998),allow_none = 1)
objetControleurServeurBD=ControleurServeurBD()
daemon.register_instance(objetControleurServeurBD)
daemon.serve_forever()



