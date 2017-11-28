import sqlite3
from _overlapped import NULL
    
class ServeurBDcas():
    def __init__(self,pControleur):
        self.Etat="NonTerminé"
        self.database = None
        self.curseur = None
        self.creeBd()
        
        self.curseur.execute("select * from CasUsage")
        self.Id = len(self.curseur.fetchall())
        self.IdScenari=0
   
    
    def creeBd(self):
        self.database = sqlite3.connect('cas.db')
        
        self.curseur = self.database.cursor()
        
        self.curseur.execute('''CREATE TABLE if NOT EXISTS CasUsage (Id integer,Description text ,Etat text,ScenarioUtilisation_Id integer)''')
        self.curseur.execute('''CREATE TABLE if NOT EXISTS ScenarioUtilisation (Id integer,Actions text,ProchaineAction integer,ScenarioUtilisation_Id integer)''')

        self.database.commit()
        
    def fermerBd(self):
        self.database.close()
    
    def modifierCas(self,cas,usager,machine,indice):

        self.curseur.execute("UPDATE CasUsage SET Description=? WHERE Id=?", (cas,indice,))
        self.curseur.execute("UPDATE ScenarioUtilisation SET Actions=? WHERE ScenarioUtilisation.Id=? and ScenarioUtilisation.ScenarioUtilisation_Id=(Select ScenarioUtilisation_Id from CasUsage)", (usager,1,))
        self.curseur.execute("UPDATE ScenarioUtilisation SET Actions=? WHERE ScenarioUtilisation.Id=? and ScenarioUtilisation.ScenarioUtilisation_Id=(Select ScenarioUtilisation_Id from CasUsage)", (machine,2,))
        self.database.commit()
        
        
    def envoyerCas(self,cas):
        self.Id+=1
        self.curseur.execute("INSERT INTO CasUsage VALUES (?,?,?,?);", (self.Id,cas,self.Etat,self.Id))
        
        self.database.commit()
   
    def envoyerScenari(self,utlisateur,machine):
        self.IdScenari+=1
        self.curseur.execute("INSERT INTO ScenarioUtilisation VALUES (?,?,?,?);", (self.IdScenari,utlisateur,NULL,self.Id))
        self.curseur.execute("INSERT INTO ScenarioUtilisation VALUES (?,?,?,?);", (self.IdScenari+1,machine,NULL,self.Id))
        self.IdScenari=0
        self.database.commit()
    
    def chercherBdcas(self,Id):

        cas=self.curseur.execute("SELECT Description FROM CasUsage WHERE Id=?", (Id,))
        return cas.fetchone()[0]
    
    def chercherBdUtilisateur(self,indice):
        print("Indice",indice)
        
        usager=self.curseur.execute("SELECT Actions FROM ScenarioUtilisation,CasUsage WHERE ScenarioUtilisation.Id=?  and CasUsage.ScenarioUtilisation_Id=? and CasUsage.ScenarioUtilisation_Id=ScenarioUtilisation.ScenarioUtilisation_Id", (1,indice,))
        
        return usager.fetchone()[0]
    
    def chercherBdMachine(self,indice):
        machine=self.curseur.execute("SELECT Actions FROM ScenarioUtilisation,CasUsage WHERE ScenarioUtilisation.Id=?  and CasUsage.ScenarioUtilisation_Id=? and CasUsage.ScenarioUtilisation_Id=ScenarioUtilisation.ScenarioUtilisation_Id", (2,indice))
        
        return machine.fetchone()[0] 
    
    def changerEtat(self,EtatInitial):
        Etat=self.curseur.execute('SELECT Etat FROM CasUsage WHERE Id=?',(EtatInitial+1,))
        EtatCompare=Etat.fetchone()[0]
        if(EtatCompare=="NonTerminé"):
            self.curseur.execute("UPDATE CasUsage SET Etat=? WHERE Id=? AND Etat=?", ("Terminé",EtatInitial+1,"NonTerminé",))
        elif(EtatCompare=="Terminé"):
            self.curseur.execute("UPDATE CasUsage SET Etat=? WHERE Id=? AND Etat=?", ("NonTerminé",EtatInitial+1,"Terminé",))
        elif(EtatCompare=="Reprendre"):
            self.curseur.execute("UPDATE CasUsage SET Etat=? WHERE Id=? AND Etat=?", ("NonTerminé",EtatInitial+1,"Reprendre",))
            self.database.commit()
            return False
   
        self.database.commit()
    
    def changerEtatReprendre(self,EtatInitial):
        Etat=self.curseur.execute('SELECT Etat FROM CasUsage WHERE Id=?',(EtatInitial+1,))
        EtatCompare=Etat.fetchone()[0]
        if(EtatCompare=="NonTerminé"):
            self.curseur.execute("UPDATE CasUsage SET Etat=? WHERE Id=? AND Etat=?", ("Reprendre",EtatInitial+1,"NonTerminé",))
            self.database.commit()
            return True
        elif(EtatCompare=="Terminé"):
            self.curseur.execute("UPDATE CasUsage SET Etat=? WHERE Id=? AND Etat=?", ("Reprendre",EtatInitial+1,"Terminé",))
            self.database.commit()
            return True
        self.database.commit()
        
        
    def remplirListeUsager(self):
        listeUsager=[]
        for cas in self.curseur.execute('SELECT Actions FROM ScenarioUtilisation Where Id=1'):
            listeUsager.append(cas)
        return listeUsager
    def remplirListeMachine(self):
        listeMachine=[]
        for cas in self.curseur.execute('SELECT Actions FROM ScenarioUtilisation Where Id=2'):
            listeMachine.append(cas)   
        return listeUsager
        
    def remplirListeCas(self):
        listeCas=[]
        for cas in self.curseur.execute('SELECT Description FROM CasUsage'):
            listeCas.append(cas)
        return listeCas
        
    def remplirListeEtat(self):
        listeEtat=[]
        for Etat in self.curseur.execute('SELECT Etat FROM CasUsage'):
            listeEtat.append(Etat)
        return listeEtat