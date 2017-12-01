from tkinter import *
from logging.config import listen
from xmlrpc.client import ServerProxy

class Controleur():
    def __init__(self):
        print("jentre das qqch")
        self.saasIP=sys.argv[1]
        self.utilisateur=sys.argv[2]
        self.organisation=sys.argv[3]
        self.idProjet=sys.argv[4]
        self.clientIP=sys.argv[5]
        self.adresseServeur="http://"+self.saasIP+":9999"
        self.serveur = self.connectionServeur()
       # print("utilisateur : " , self.utilisateur)
       # print("organisation : ", self.organisation)
       # print("id projet : ", self.idProjet)
        self.modele= Modele(self)
        self.vue = Vue(self)
        self.vue.root.mainloop()
        
        print("controleur")
    
   
        
    
    def ajoutTableBD(self, nom):
        self.serveur.insertionSQL("Tables","10,"+self.idProjet+",'"+nom+"'")
        self.vue.canevaNouvelleTable.forget()
        self.vue.menuInitial()
        
    def connectionServeur(self):
        print("Connection au serveur BD...")
        serveur=ServerProxy(self.adresseServeur)
        return serveur

class Modele():
    def __init__(self, pControleur):
        self.controleur = pControleur
        self.idTable=None;
        print("modele")
        
    def remplirListBoxTable(self, listBox):
        print("modele remplir list box")
        laselection=self.controleur.serveur.selectionSQL3("Tables", "nom", "id_Projet", self.controleur.idProjet)
        for x in laselection:
            listBox.insert(END,str(x)[2:int(len(x)-3)])
            
    def idTableAjoutChamps(self, nomTable):
        idTable=self.controleur.serveur.selectionSQL3("Tables", "id",  "nom", nomTable)
        idTableGood=str(idTable)[2:int(len(idTable)-3)]
        
        self.idTable=idTableGood
        return idTable
            
    def remplirListBoxChamps(self, listBox):
        laselection=self.controleur.serveur.selectionSQL3("Champs", "nom", "id_Table", self.idTable )
        for x in laselection:
            print(x)
            listBox.insert(END,str(x)[2:int(len(x)-3)])
            
    def remplirListBoxContraintesChamps(self, listBox):
        laselection=self.controleur.serveur.selectionSQL3("Champs", "contrainte", "id_Table", self.idTable )
        for x in laselection:
            print(x)
            listBox.insert(END,str(x)[2:int(len(x)-3)])
        
            
    
class Vue():
    def __init__(self, pControleur):
        self.controleur = pControleur
        print("Vue")
        self.largeur = 800
        self.hauteur = 600
        self.root = Tk()
        self.fenetre = Frame(self.root, width = self.largeur, height = self.hauteur)
        self.fenetre.pack()
        self.menuInitial()
       

          
    def ajouterTable(self):
        pass
    
    def entrerTable(self):
        pass
    
    def menuInitial(self):
        
        
        self.caneva = Canvas(self.fenetre, width = self.largeur, height=self.hauteur, bg="steelblue")
        self.caneva.pack()
        
        self.lblListeTable=Label(text="Liste des tables : ",bg="lightblue")
        self.caneva.create_window(200,90,window=self.lblListeTable)
        
        self.listBoxNomTable=Listbox(self.caneva,bg="lightblue",borderwidth=0,relief=FLAT,width=75,height=20)
        self.caneva.create_window(390,270,window=self.listBoxNomTable)
        
        self.controleur.modele.remplirListBoxTable(self.listBoxNomTable)
        
        self.btnAjouterTable=Button(self.caneva,text="Ajouter une table",width=20,command=self.menuAjouterTable)
        self.caneva.create_window(200,550,window=self.btnAjouterTable,width=150,height=20)
        
        self.btnEntrerTable=Button(self.caneva,text="Voir les champs",width=20,command=self.nomTableAjoutChamp)
        self.caneva.create_window(600,550,window=self.btnEntrerTable,width=150,height=20)
        
    
    def nomTableAjoutChamp(self):
        position=self.listBoxNomTable.curselection()[0]
        nomTable=self.listBoxNomTable.get(position, position)
        if(position!=0):
            nomTableGood=str(nomTable)[2:int(len(nomTable)-4)]
        else:
            nomTableGood=nomTable
        idTable=self.controleur.modele.idTableAjoutChamps(nomTableGood)
        self.menuAffichageChamps()
        
    def menuAjouterTable(self):
        self.caneva.forget()
        self.canevaNouvelleTable = Canvas(self.fenetre, width = self.largeur/1.5 , height=self.hauteur/2, bg="steelblue")
        self.canevaNouvelleTable.pack()
        
        self.lblNom=Label(text="Nom de la table : ", bg="lightblue")
        self.canevaNouvelleTable.create_window(270,75,window=self.lblNom)
        
        self.entryNomTable=Entry(bg="white")
        self.canevaNouvelleTable.create_window(275,130,window=self.entryNomTable,width=300,height=25)
        
        self.btnCreationTable=Button(self.canevaNouvelleTable,text="Ajouter une table",width=20,command=self.ajoutTableBD)
        self.canevaNouvelleTable.create_window(125,225,window=self.btnCreationTable,width=150,height=25)
        
        self.btnAnnulerAjouterTable=Button(self.canevaNouvelleTable,text="Annuler",width=20,command=self.annulerNouvelleTable)
        self.canevaNouvelleTable.create_window(420,225,window=self.btnAnnulerAjouterTable,width=150,height=25)
        
    def menuAffichageChamps(self):
        self.caneva.forget()
        self.canevaAffichageChamps = Canvas(self.fenetre, width = self.largeur , height=self.hauteur, bg="steelblue")
        self.canevaAffichageChamps.pack()
        
        self.lblListeChamps=Label(text="Listes des champs de la table : ",bg="lightblue")
        self.canevaAffichageChamps.create_window(200,90,window=self.lblListeChamps)
        
        self.lblListeContrainteChamps=Label(text="Contrainte : ",bg="lightblue")
        self.canevaAffichageChamps.create_window(500,90,window=self.lblListeContrainteChamps)
        
        self.listBoxContrainteChampsTable=Listbox(self.canevaAffichageChamps,bg="lightblue",borderwidth=0,relief=FLAT,width=20,height=20)
        self.canevaAffichageChamps.create_window(550,270,window=self.listBoxContrainteChampsTable)
        ##################
        self.controleur.modele.remplirListBoxContraintesChamps(self.listBoxContrainteChampsTable)
        ################
        self.listBoxChampsTable=Listbox(self.canevaAffichageChamps,bg="lightblue",borderwidth=0,relief=FLAT,width=50,height=20)
        self.canevaAffichageChamps.create_window(300,270,window=self.listBoxChampsTable)
        
        self.controleur.modele.remplirListBoxChamps(self.listBoxChampsTable)
        
        #self.btnAjouterChamps=Button(self.canevaAffichageChamps,text="Ajouter un champs",width=20,command=self.allezMenuAjouterChamps())
        #self.canevaAffichageChamps.create_window(200,550,window=self.btnAjouterChamps,width=150,height=20)
        
        self.btnAnnulerAffichageChamps=Button(self.canevaAffichageChamps,text="Annuler",width=20,command=self.annulerAffichageChamps)
        self.canevaAffichageChamps.create_window(600,550,window=self.btnAnnulerAffichageChamps,width=150,height=20)
    
    
        
    def allezMenuAjouterChamps(self):
         self.canevaAffichageChamps.forget()
         self.menuAjouterChamps()
     
    def menuAjouterChamps(self):
        print("gasgbsaoidbgsd")
        
        self.canevaAjouterChamps = Canvas(self.fenetre, width = self.largeur*(2/3) , height=self.hauteur, bg="steelblue")
        self.canevaAjouterChamps.pack()
        
        self.lblNom=Label(text="Nom : ",bg="lightblue")
        self.canevaAjouterChamps.create_window(100,85,window=self.lblNom)
        
        self.lblType=Label(text="Type : ",bg="lightblue")
        self.canevaAjouterChamps.create_window(100,150,window=self.lblType)
        
        self.entryNomChamps=Entry(bg="white")
        self.canevaAjouterChamps.create_window(300,85,window=self.entryNomChamps,width=300,height=20)
        
        self.entryType=Entry(bg="white")
        self.canevaAjouterChamps.create_window(300,150,window=self.entryType,width=300,height=20)
        
        self.checkButtonPK=Checkbutton(text="Clé primaire",bg="steelblue")
        self.canevaAjouterChamps.create_window(125,215,window=self.checkButtonPK,width=100,height=20)
        
        self.checkButtonFK=Checkbutton(text="Clé secondaire",bg="steelblue")
        self.canevaAjouterChamps.create_window(130,280,window=self.checkButtonFK,width=100,height=20)
        
        self.lblTableFK=Label(text="Table : ",bg="lightblue")
        self.canevaAjouterChamps.create_window(250,280,window=self.lblTableFK)
        

        self.listBoxTableFK=Listbox(self.canevaAjouterChamps,bg="white",borderwidth=0,relief=FLAT,width=25,height=3)
        self.canevaAjouterChamps.create_window(390,280,window=self.listBoxTableFK)
        self.controleur.modele.remplirListBox(self.listBoxTableFK)
            
        self.listBoxChampsFK=Listbox(self.canevaAjouterChamps,bg="white",borderwidth=0,relief=FLAT,width=25,height=3)
        self.canevaAjouterChamps.create_window(390,360,window=self.listBoxChampsFK)
        
        self.controleur.modele.remplirListBox(self.listBoxChampsFK)
        
        self.lblChampsFK=Label(text="Champs : ",bg="lightblue")
        self.canevaAjouterChamps.create_window(260,360,window=self.lblChampsFK)
        
        self.btnAjouterChamps=Button(self.canevaAjouterChamps,text="Ajouter un champs",width=20,command=self.ajouterChamps)
        self.canevaAjouterChamps.create_window(260,500,window=self.btnAjouterChamps,width=150,height=20)
    
        
        






        
     
    def ajouterChamps(self):
        pass
       
    def annulerNouvelleTable(self):
       
        self.canevaNouvelleTable.forget()
        self.menuInitial()
        
    def annulerAffichageChamps(self):
        self.canevaAffichageChamps.forget()
        self.menuInitial()
        
    def ajoutTableBD(self):
        nom=self.entryNomTable.get()
        self.controleur.ajoutTableBD(nom)
    
    
if __name__ == '__main__':
    c = Controleur()