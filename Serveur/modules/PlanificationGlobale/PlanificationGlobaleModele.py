# -*- coding: utf-8 -*-

import sqlite3
from time import *
from PlanificationGlobale  import *

#TODO - UPDATE

class Modele():
    def __init__(self, parent):
        self.parent=parent
        
        pass
        
    def importerDonnees(self,projectName):
        #Fonction que lors d'un nouveau projet, va preremplir les cases crc
        pass

    def getTime(self):
        return (datetime.now().strftime('%Y/%m/%d %H:%M:%S'))


class SQL():
    def __init__(self, parent):
        self.parent=parent
        self.Saas=parent.serveur
          
    def selDonnees(self,champ): #WORKS returns [[row]]
        #(self,nomTable,champs,where,indice)   
        self.writeLog("SELECT - Field:"+str(champ),"S66")
        return self.Saas.selectionSQL3('PlanifGlobales',champ,'id_Projet',self.parent.idProjet)
        
        
    def afficherFonctions(self):
        #self.parent.serveur.
        pass
    
    def modifierFonction(self,valeurModifiee,champModifier,id):
       self.Saas.updateSQL2('PlanifGlobales',valeurModifiee,champModifier,'id',id)
       self.writeLog("UPDATE - Field:"+str(champModifier)+" - ID:"+str(id),"S65")
       # UPDATE employees SET lastname = 'Smith' WHERE employeeid = 3;
       pass
    
    def writeLog(self,action,codeid):
        self.parent.writeLog(action,codeid)
    
    #(Numéro Sprint,Nom de la fonction, priorité(basse=3,moyenne=2,haute=1)
    def creerFonction(self,sprint,nomfonction,priorite,debut,fin):
        #id,id_Projet,id_Sprint,responsable,id_Responsable,priorite,date_debut,date_fin
        if (priorite==3):
            priorite="Basse"
        elif (priorite==2):
            priorite="Moyenne"
        elif (priorite==1):
            priorite="Haute"    

        #id,idprojet,idsprint,idresponsable,priorite,debut,fin
        params = (self.parent.id,self.parent.idProjet,sprint,self.parent.utilisateur,nomfonction,priorite,debut,fin)
        self.parent.id+=1
        self.Saas.insDonneesPlanif('''PlanifGlobales''',params)
        self.writeLog("INSERT - Name:"+str(nomfonction)+" - ID:"+str(self.parent.id),"S64")
        #fonction d'ecriture dans la table planification    
        pass
    
    #"INSERT INTO logs VALUES(?,?,?,?,?,?,?)", (date,org,user,ip,db,module,action,)
  
    def supressionFonction(self):
        pass
    
    def previsionHeure(self):
        pass
    
    def calculPourcent(self,debut=time()-50,fin=time()+50):
        tempsNow=time()-debut
        tempsEnd=fin-debut
        pourcent=(tempsNow/tempsEnd)*100
        print("%.2f" % round(pourcent,2)+"%")
        return pourcent
    
    
          