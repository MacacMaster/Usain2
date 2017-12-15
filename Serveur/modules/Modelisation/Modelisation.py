from tkinter import *
from logging.config import listen
from xmlrpc.client import ServerProxy
from tkinter import messagebox

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
        self.modele= Modele(self)
        self.vue = Vue(self)
        self.writeLog("Ouverture du Module","2")
        self.vue.root.mainloop()
        print("controleur")

    def fermerProgramme(self):
        self.writeLog("Fermeture du Module","3")
        self.vue.root.destroy()

    def writeLog(self,action,codeid):
        self.serveur.writeLog(self.organisation,self.utilisateur,self.clientIP,self.saasIP,"Modelisation",action,codeid) 

    def ajoutTableBD(self, nom):
        self.serveur.insertionSQL("Tables",str(self.idProjet)+",'"+nom+"'")
        self.vue.canevaNouvelleTable.forget()
        self.vue.menuInitial()
        
    def connectionServeur(self):
        print("Connection au serveur BD...")
        serveur=ServerProxy(self.adresseServeur)
        return serveur
    
    def updateTable(self, nomTableAvant, nomTableApres):
        idTable = self.modele.idTableAjoutChamps(nomTableAvant)
        if(self.verificationExiste("nom", "Tables",  "id_Projet", self.idProjet, nomTableApres) ==  False):
            messagebox.showerror("Table existante","Le nom de votre table existe deja dans la table")
        else:
            self.serveur.updateSQL2("Tables", nomTableApres,"nom", "id",idTable)
           
    
    def changeEtat(self, etat, idChamp, listBox,idTable):
        print("Entre dans la fonction changeEtat")
        if(etat=="Bon"):
            self.serveur.updateSQL("Champs", "Pas bon","etat", "id", "id_Table",idChamp, idTable)
        elif(etat=="Pas bon"):
            self.serveur.updateSQL("Champs", "Bon" , "etat", "id" , "id_Table" , idChamp , idTable)
        self.modele.remplirListBoxEtatChamps(listBox, idTable)
        
    def ajouterChamp(self,nom, contrainte,type):
        self.serveur.insertionSQL("Champs",self.modele.idTableSelec+",'"+nom+"','"+contrainte+"','"+ type + "','Bon'")
        
    def nomTableAvecId(self, id):
        nomTable = self.serveur.selectionSQL3("Tables", "nom" ,  "nom", id)
        nomTableGood=str(nomTable)[2:int(len(nomTable)-3)]
        return nomTableGood
    
    def verificationExiste(self,champAVerifier, tableAVerifier, where, condition,valeur):
        return self.serveur.verificationExiste(champAVerifier, tableAVerifier, where, condition,valeur)
    
    def supprimerTable(self, ouDelete, quoi, egaleAQuoi):
        self.serveur.delete(ouDelete, quoi, egaleAQuoi)
        self.vue.caneva.forget()
        self.vue.menuInitial()
        
    def supprimerChamp(self, ouDelete, quoi, egaleAQuoi, nomTable):
        self.serveur.delete(ouDelete, quoi, egaleAQuoi)
        self.vue.canevaAffichageChamps.forget()
        self.vue.menuAffichageChamps(nomTable)
        

class Modele():
    def __init__(self, pControleur):
        self.controleur = pControleur
        self.idTable2=None
        self.idTableFK=None
        self.idChamp=None
        self.contrainte=""
        self.nomTable=None
        self.idTableSelec=None
        
        
    def remplirListBoxTable(self, listBox):
        laselection=self.controleur.serveur.selectionSQL3("Tables", "nom", "id_Projet", self.controleur.idProjet)
        for x in laselection:
            listBox.insert(END,str(x)[2:int(len(x)-3)])
            
    def idTableAjoutChamps(self, nomTable):
        idTable=self.controleur.serveur.selectionSQL3("Tables", "id",  "nom", nomTable)
        idTableGood=str(idTable)[2:int(len(idTable)-3)]
        return idTableGood
    
    
    def idDuChamp(self, nomChamp, idTable):
        idChamp=self.controleur.serveur.selectionSQL2("Champs", "id",  "nom","id_Table", nomChamp, idTable)
        idChampGood=str(idChamp)[2:int(len(idChamp)-3)]
        self.idChamp=idChampGood
        return idChampGood
    
    def remplirListBoxChamps(self, listBox, idTable):
        listBox.delete(0, END)
        laselection=self.controleur.serveur.selectionSQL3("Champs", "nom", "id_Table", idTable )
        for x in laselection:
            print(x)
            listBox.insert(END,str(x)[2:int(len(x)-3)])
            
    def remplirListBoxContraintesChamps(self, listBox, idTable):
        listBox.delete(0, END)
        laselection=self.controleur.serveur.selectionSQL3("Champs", "contrainte", "id_Table", idTable )
        for x in laselection:
            print(x)
            listBox.insert(END,str(x)[2:int(len(x)-3)])
        
    def remplirListBoxTypeChamps(self, listBox, idTable):
        laselection=self.controleur.serveur.selectionSQL3("Champs", "type", "id_Table", idTable )
        for x in laselection:
            print(x)
            listBox.insert(END,str(x)[2:int(len(x)-3)])
            
    def remplirListBoxEtatChamps(self, listBox, idTable):
        laselection=self.controleur.serveur.selectionSQL3("Champs", "etat", "id_Table", idTable )
        listBox.delete(0, END)
        for x in laselection:
            print(x)
            listBox.insert(END,str(x)[2:int(len(x)-3)])
   
            
    def remplirListBoxFKTable(self,listBoxTable):
        laselection=self.controleur.serveur.selectionSQL3("Tables", "nom", "id_Projet", self.controleur.idProjet)
        for x in laselection:
            listBoxTable.insert(END,str(x)[2:int(len(x)-3)])
            
    def remplirListBoxFKChamp(self, listBoxChamp):
            
        laselection=self.controleur.serveur.selectionSQL3("Champs", "nom", "id_Table", self.idTableFK )
        for x in laselection:
            listBoxChamp.insert(END,str(x)[2:int(len(x)-3)])
            
    def verificationSelection(self, listbox, message):
        if(listbox.curselection()):
            return True
        else:
            messagebox.showerror("Erreur de selection",message)
            
        
        
            
            
            
            
        
            
    
class Vue():
    def __init__(self, pControleur):
        self.controleur = pControleur
        self.largeur = 800
        self.hauteur = 600
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.controleur.fermerProgramme)
        self.fenetre = Frame(self.root, width = self.largeur, height = self.hauteur)
        self.fenetre.pack()
        self.menuInitial()

    def centrerFenetre(self,hauteur, largeur): 
        self.root.update() # Suivant le WM. A faire dans tous les cas donc.
        fenrw = self.root.winfo_reqwidth()/largeur
        fenrh = self.root.winfo_reqheight()/hauteur
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+%d+%d" % (fenrw, fenrh, (sw-fenrw)/2, (sh-fenrh)/2))
        
    def ajouterTable(self):
        pass
    
    def entrerTable(self):
        pass
    
    def menuInitial(self):
        self.centrerFenetre(1,1)
        self.caneva = Canvas(self.fenetre, width = self.largeur, height=self.hauteur, bg="steelblue")
        
        self.caneva.pack()
        self.root.title("Module modélisation")
        
        self.lblModule=Label(text="Module modélisation",bg="steelblue")
        self.lblModule.config(font=("Tahoma", 24))
        self.lblModule.config(foreground='lightblue')
        self.caneva.create_window(self.largeur/2,60,window=self.lblModule)
        
        self.lblListeTable=Label(text="Liste des tables : ",bg="lightblue")
        self.caneva.create_window(200,120,window=self.lblListeTable)
        
        self.listBoxNomTable=Listbox(self.caneva,bg="lightblue",borderwidth=0,relief=FLAT,width=75,height=20)
        self.caneva.create_window(390,320,window=self.listBoxNomTable)
        
        self.controleur.modele.remplirListBoxTable(self.listBoxNomTable)
        
        self.btnAjouterTable=Button(self.caneva,text="Ajouter une table",width=20,command=self.menuAjouterTable)
        self.caneva.create_window(115,550,window=self.btnAjouterTable,width=150,height=20)
        
        self.btnRenommerTable=Button(self.caneva,text="Renommer une table",width=20,command=self.renommerTable)
        self.caneva.create_window(305,550,window=self.btnRenommerTable,width=150,height=20)
        
        self.btnSupprimerTable=Button(self.caneva,text="Supprimer une table",width=20,command=self.supprimerTable)
        self.caneva.create_window(495,550,window=self.btnSupprimerTable,width=150,height=20)
        
        self.btnEntrerTable=Button(self.caneva,text="Voir les champs",width=20,command=self.nomTableAjoutChamp)
        self.caneva.create_window(685,550,window=self.btnEntrerTable,width=150,height=20)
        
    def renommerTable(self):
        ouiOuNon = self.controleur.modele.verificationSelection(self.listBoxNomTable, "Veuillez selectionner un nom de table")
        if(ouiOuNon == True):
            position=self.listBoxNomTable.curselection()[0]
            nomTable=self.listBoxNomTable.get(position, position)
            if(position!=0):
                nomTableGood=str(nomTable)[2:int(len(nomTable)-4)]
            else:
                nomTableGood=nomTable
            idTable=self.controleur.modele.idTableAjoutChamps(nomTableGood)
            self.menuRenommerTable(idTable, nomTableGood)
        
        
        
        
            
    def menuRenommerTable(self, idTable, nomTable):
        self.centrerFenetre(2,1.5)
        self.caneva.forget()
        
        self.canevaRenommerTable = Canvas(self.fenetre, width = self.largeur , height=self.hauteur, bg="steelblue")
        self.canevaRenommerTable.pack()
        self.root.title("Ajouter une table")
        
        self.lblNomTable=Label(text="Renommer la table",bg="steelblue")
        self.lblNomTable.config(font=("Tahoma", 24))
        self.lblNomTable.config(foreground='lightblue')
        self.canevaRenommerTable.create_window(275,60,window=self.lblNomTable)
        
        self.lblNomAvant=Label(text="Nom de la table : *", bg="lightblue")
        self.canevaRenommerTable.create_window(100,115,window=self.lblNomAvant)
        
        self.entryNomTableAvant=Entry(bg="white")
        self.entryNomTableAvant.insert(END, nomTable)
        self.entryNomTableAvant.config(state="disabled")
        self.canevaRenommerTable.create_window(340,115,window=self.entryNomTableAvant,width=300,height=25)
        
        self.lblNomApres=Label(text="Nom de la table : *", bg="lightblue")
        self.canevaRenommerTable.create_window(100,160,window=self.lblNomApres)
        
        self.entryNomTableApres=Entry(bg="white")
        self.canevaRenommerTable.create_window(340,160,window=self.entryNomTableApres,width=300,height=25)
        
        self.lblObligatoire=Label(text="* : Obligatoire", bg="steelblue")
        self.canevaRenommerTable.create_window(95,270,window=self.lblObligatoire)
        
        
        self.btnRenommerTable=Button(self.canevaRenommerTable,text="Renommer la table",width=20,command=self.renommerTableBD)
        self.canevaRenommerTable.create_window(125,225,window=self.btnRenommerTable,width=150,height=25)
        
        self.btnAnnulerRenommerTable=Button(self.canevaRenommerTable,text="Annuler",width=20,command=self.annulerRenommerTable)
        self.canevaRenommerTable.create_window(420,225,window=self.btnAnnulerRenommerTable,width=150,height=25)

    def renommerTableBD(self):
        nomAvant = self.entryNomTableAvant.get()
        nomApres = self.entryNomTableApres.get()
        self.controleur.updateTable(nomAvant, nomApres)
        self.annulerRenommerTable()
    
    
    def supprimerTable(self):
        ouiOuNon = self.controleur.modele.verificationSelection(self.listBoxNomTable, "Veuillez selectionner un nom de table")
        if(ouiOuNon == True):
            position=self.listBoxNomTable.curselection()[0]
            nomTable=self.listBoxNomTable.get(position, position)
            if(position!=0):
                nomTableGood=str(nomTable)[2:int(len(nomTable)-4)]
            else:
                nomTableGood=nomTable
            self.controleur.supprimerTable("Tables", "nom", nomTableGood)
    
    def nomTableAjoutChamp(self):
        ouiOuNon = self.controleur.modele.verificationSelection(self.listBoxNomTable, "Veuillez selectionner un nom de table")
        if(ouiOuNon == True):
            position=self.listBoxNomTable.curselection()[0]
            nomTable=self.listBoxNomTable.get(position, position)
            if(position!=0):
                nomTableGood=str(nomTable)[2:int(len(nomTable)-4)]
            else:
                nomTableGood=nomTable
            idTable=self.controleur.modele.idTableAjoutChamps(nomTableGood)
            self.controleur.modele.idTableSelec=idTable
            self.controleur.modele.nomTable=nomTableGood
            self.caneva.forget()
            self.menuAffichageChamps(nomTableGood)
        
    def menuAjouterTable(self):
        self.centrerFenetre(2,1.5)
        self.caneva.forget()
        self.canevaNouvelleTable = Canvas(self.fenetre, width = self.largeur , height=self.hauteur, bg="steelblue")
        self.canevaNouvelleTable.pack()
        self.root.title("Ajouter une table")
        
        self.lblNomTable=Label(text="Ajouter une table",bg="steelblue")
        self.lblNomTable.config(font=("Tahoma", 24))
        self.lblNomTable.config(foreground='lightblue')
        self.canevaNouvelleTable.create_window(275,60,window=self.lblNomTable)
        
        self.lblNom=Label(text="Nom de la table : *", bg="lightblue")
        self.canevaNouvelleTable.create_window(100,130,window=self.lblNom)
        
        self.lblObligatoire=Label(text="* : Obligatoire", bg="steelblue")
        self.canevaNouvelleTable.create_window(95,270,window=self.lblObligatoire)
        
        self.entryNomTable=Entry(bg="white")
        self.canevaNouvelleTable.create_window(340,130,window=self.entryNomTable,width=300,height=25)
        
        self.btnCreationTable=Button(self.canevaNouvelleTable,text="Ajouter une table",width=20,command=self.ajoutTableBD)
        self.canevaNouvelleTable.create_window(125,225,window=self.btnCreationTable,width=150,height=25)
        
        self.btnAnnulerAjouterTable=Button(self.canevaNouvelleTable,text="Annuler",width=20,command=self.annulerNouvelleTable)
        self.canevaNouvelleTable.create_window(420,225,window=self.btnAnnulerAjouterTable,width=150,height=25)
        
    def menuAffichageChamps(self, nomTable):
        self.centrerFenetre(1,1)
        self.canevaAffichageChamps = Canvas(self.fenetre, width = self.largeur , height=self.hauteur, bg="steelblue")
        self.canevaAffichageChamps.pack()
        self.root.title("Liste des champs de la table "+ nomTable)
        
        self.lblNomTable=Label(text=nomTable,bg="steelblue")
        self.lblNomTable.config(font=("Tahoma", 24))
        self.lblNomTable.config(foreground='lightblue')
        self.canevaAffichageChamps.create_window(self.largeur/2,60,window=self.lblNomTable)
        
        
        self.lblListeChamps=Label(text="Listes des champs de la table : ",bg="lightblue")
        self.canevaAffichageChamps.create_window(145,120,window=self.lblListeChamps)
        
        self.listBoxChampsTable=Listbox(self.canevaAffichageChamps,bg="lightblue",borderwidth=0,relief=FLAT,width=30,height=20)
        self.canevaAffichageChamps.create_window(170,320,window=self.listBoxChampsTable)
        
        self.lblListeContrainteChamps=Label(text="Contrainte : ",bg="lightblue")
        self.canevaAffichageChamps.create_window(325,120,window=self.lblListeContrainteChamps)
        
        self.listBoxContrainteChampsTable=Listbox(self.canevaAffichageChamps,bg="lightblue",borderwidth=0,relief=FLAT,width=20,height=20)
        self.canevaAffichageChamps.create_window(355,320,window=self.listBoxContrainteChampsTable)
        
        self.lblListeTypeChamp=Label(text="Type : ",bg="lightblue")
        self.canevaAffichageChamps.create_window(475,120,window=self.lblListeTypeChamp)
        
        self.listBoxTypeChampsTable=Listbox(self.canevaAffichageChamps,bg="lightblue",borderwidth=0,relief=FLAT,width=20,height=20)
        self.canevaAffichageChamps.create_window(505,320,window=self.listBoxTypeChampsTable)
        
        self.lblListeEtatChamp=Label(text="Etat : ",bg="lightblue")
        self.canevaAffichageChamps.create_window(600,120,window=self.lblListeEtatChamp)
        
        self.listBoxEtatChampsTable=Listbox(self.canevaAffichageChamps,bg="lightblue",borderwidth=0,relief=FLAT,width=20,height=20)
        self.canevaAffichageChamps.create_window(650,320,window=self.listBoxEtatChampsTable)
        id=self.controleur.modele.idTableAjoutChamps(nomTable)
        self.controleur.modele.remplirListBoxEtatChamps(self.listBoxEtatChampsTable,id)
        self.controleur.modele.remplirListBoxTypeChamps(self.listBoxTypeChampsTable,id)

        self.controleur.modele.remplirListBoxContraintesChamps(self.listBoxContrainteChampsTable, id)
        
        self.controleur.modele.remplirListBoxChamps(self.listBoxChampsTable,id)
        
        self.btnNewChamp=Button(self.canevaAffichageChamps,text="Ajouter un champ",width=20,command=self.allezMenuAjouterChamps)
        self.canevaAffichageChamps.create_window(115,550,window=self.btnNewChamp,width=150,height=20)
        
        self.btnChangeEtat=Button(self.canevaAffichageChamps,text="Changer l'état",width=20,command=self.changeEtat)
        self.canevaAffichageChamps.create_window(305,550,window=self.btnChangeEtat,width=150,height=20)
        
        self.btnSupprimerChamp=Button(self.canevaAffichageChamps,text="Supprimer le champ",width=20,command=self.supprimerChamp)
        self.canevaAffichageChamps.create_window(495,550,window=self.btnSupprimerChamp,width=150,height=20)

        self.btnAnnulerAffichageChamps=Button(self.canevaAffichageChamps,text="Annuler",width=20,command=self.annulerAffichageChamps)
        self.canevaAffichageChamps.create_window(685,550,window=self.btnAnnulerAffichageChamps,width=150,height=20)
        
    
    def supprimerChamp(self):
        ouiOuNon = self.controleur.modele.verificationSelection(self.listBoxChampsTable ,"Veuillez selectionner champ")
        if(ouiOuNon == True):
            nomTable=self.lblNomTable.cget("text")
            position=self.listBoxChampsTable.curselection()[0]
            nomChamp=self.listBoxChampsTable.get(position, position)
            if(position!=0):
                nomChampGood=str(nomChamp)[2:int(len(nomChamp)-4)]
            else:
                nomChampGood=nomChamp
            self.controleur.supprimerChamp("Champs", "nom", nomChampGood, nomTable)
    
    def changeEtat(self):
        ouiOuNon = self.controleur.modele.verificationSelection(self.listBoxEtatChampsTable ,"Veuillez selectionner un etat")
        print("OUI OU NONONONONON : ", ouiOuNon)
        if(ouiOuNon == True):
            nomTable=self.lblNomTable.cget('text')
            print("NOMOMOMOM DEEE LLLAAAA TTABEL :  ", nomTable)
            idTable=self.controleur.modele.idTableAjoutChamps(nomTable)
            position=self.listBoxEtatChampsTable.curselection()[0]
            nom=self.listBoxChampsTable.get(position, position)
            etat=self.listBoxEtatChampsTable.get(position, position)
            if(position!=0):
               nomChampGood=str(nom)[2:int(len(nom)-4)]
               etatGood=str(etat)[2:int(len(etat)-4)]
            else:
               nomChampGood=nom
               etatGood=etat
            print("NOM DU CHAMMMPPPPP A CHANGER ETAT : ", nomChampGood)
            idChamp=self.controleur.modele.idDuChamp(nomChampGood, idTable)
            self.controleur.changeEtat(etatGood, idChamp, self.listBoxEtatChampsTable, idTable)
            self.canevaAffichageChamps.forget()
            self.menuAffichageChamps(nomTable)
        
    def allezMenuAjouterChamps(self):
         self.canevaAffichageChamps.forget()
         self.menuAjouterChamps()
     
    def menuAjouterChamps(self):
        self.centrerFenetre(1,3/2)
        self.canevaAjouterChamps = Canvas(self.fenetre, width = self.largeur , height=self.hauteur, bg="steelblue")
        self.canevaAjouterChamps.pack()
        
        self.root.title("Ajouter un champ")
        
        self.lblChamp=Label(text="Ajouter un champ",bg="steelblue")
        self.lblChamp.config(font=("Tahoma", 24))
        self.lblChamp.config(foreground='lightblue')
        self.canevaAjouterChamps.create_window(275,60,window=self.lblChamp)
        
        self.lblNom=Label(text="Nom : *",bg="lightblue")
        self.canevaAjouterChamps.create_window(100,115,window=self.lblNom)
        
        self.lblType=Label(text="Type : *",bg="lightblue")
        self.canevaAjouterChamps.create_window(100,185,window=self.lblType)
        
        self.entryNomChamps=Entry(bg="white")
        self.canevaAjouterChamps.create_window(300,115,window=self.entryNomChamps,width=300,height=20)
        
        self.entryType=Entry(bg="white")
        self.canevaAjouterChamps.create_window(300,185,window=self.entryType,width=300,height=20)
        
        self.checkButtonPK=Checkbutton(text="Clé primaire",bg="steelblue",command=self.contraintePK)
        self.canevaAjouterChamps.create_window(125,250,window=self.checkButtonPK,width=100,height=20)
        
        self.checkButtonFK=Checkbutton(text="Clé secondaire",bg="steelblue",command=self.foreignKey)
        self.canevaAjouterChamps.create_window(130,325,window=self.checkButtonFK,width=100,height=20)
        
        self.lblTableFK=Label(text="Table : ",bg="lightblue")
        self.canevaAjouterChamps.create_window(250,325,window=self.lblTableFK)
        

        self.listBoxTableFK=Listbox(self.canevaAjouterChamps,bg="white",borderwidth=0,relief=FLAT,width=25,height=3)
        self.canevaAjouterChamps.create_window(390,325,window=self.listBoxTableFK)
        
            
        self.listBoxChampsFK=Listbox(self.canevaAjouterChamps,bg="white",borderwidth=0,relief=FLAT,width=25,height=3)
        self.canevaAjouterChamps.create_window(390,445,window=self.listBoxChampsFK)
        
        self.lblChampsFK=Label(text="Champs : ",bg="lightblue")
        self.canevaAjouterChamps.create_window(260,445,window=self.lblChampsFK)
        
        self.btnChoisirChamp=Button(self.canevaAjouterChamps,text="Choisir le champ",width=20,command=self.affichageChampFK)
        self.canevaAjouterChamps.create_window(390,370,window=self.btnChoisirChamp,width=150,height=20)
        
        self.btnAjouterChamps=Button(self.canevaAjouterChamps,text="Ajouter un champs",width=20,command=self.ajouterChamps)
        self.canevaAjouterChamps.create_window(160,525,window=self.btnAjouterChamps,width=150,height=20)
        
        self.btnRetourChamps=Button(self.canevaAjouterChamps,text="Annuler",width=20,command=self.retourMenuChamps)
        self.canevaAjouterChamps.create_window(375,525,window=self.btnRetourChamps,width=150,height=20)
        
        self.lblObligatoire=Label(text="* : Obligatoire",bg="steelblue")
        self.canevaAjouterChamps.create_window(100,560,window=self.lblObligatoire)
        
        
        
    def retourMenuChamps(self):
        idTable=self.controleur.modele.idTableAjoutChamps(self.lblNomTable.cget("text"))
        nomTable=self.controleur.nomTableAvecId(idTable)
        self.canevaAjouterChamps.forget()
        self.menuAffichageChamps(self.controleur.modele.nomTable)
        
    def contraintePK(self):
        self.controleur.modele.contrainte = "PK"
        
    def affichageChampFK(self):
        position=self.listBoxTableFK.curselection()[0]
        nomTable=self.listBoxTableFK.get(position, position)
        if(position!=0):
            nomTableGood=str(nomTable)[2:int(len(nomTable)-4)]
        else:
            nomTableGood=nomTable
        
        self.controleur.modele.contrainte+=" "+nomTableGood
        idTable=self.controleur.modele.idTableAjoutChamps(nomTableGood)
        self.controleur.modele.remplirListBoxChamps(self.listBoxChampsFK, idTable)
    
    
    def foreignKey(self):
        if(self.controleur.modele.contrainte==""):
            self.controleur.modele.contrainte = "FK"
        else:
            self.controleur.modele.contrainte += ", FK"
        self.controleur.modele.remplirListBoxFKTable(self.listBoxTableFK)
     
    def ajouterChamps(self):
        idTable=self.controleur.modele.idTableAjoutChamps(self.lblNomTable.cget("text"))
        if(self.entryType.get()=="" or self.entryNomChamps.get()==""):
            messagebox.showerror("Donnée(s) manquante(s)","Veuillez entrer un nom et un type")
        elif(self.controleur.verificationExiste("nom", "Champs", "id_Table", idTable, self.entryNomChamps.get())==False):
             messagebox.showerror("Champ existante","Le nom du champ existe deja dans la table")
        else:    
            if("FK" in self.controleur.modele.contrainte):
                position=self.listBoxChampsFK.curselection()[0]
                nomChamp=self.listBoxChampsFK.get(position, position)
                if(position!=0):
                    nomChampGood=str(nomChamp)[2:int(len(nomChamp)-4)]
                else:
                    nomChampGood=nomChamp
                self.controleur.modele.contrainte+="("+nomChampGood+")"
            nom=self.entryNomChamps.get()
            type=self.entryType.get()
            self.controleur.ajouterChamp(nom, self.controleur.modele.contrainte,type)
            self.canevaAjouterChamps.forget()
            self.controleur.modele.contrainte=""
            self.menuAffichageChamps(self.controleur.modele.nomTable)
            
    def annulerRenommerTable(self):
        self.canevaRenommerTable.forget()
        self.menuInitial()
       
    def annulerNouvelleTable(self):
       
        self.canevaNouvelleTable.forget()
        self.menuInitial()
        
    def annulerAffichageChamps(self):
        self.canevaAffichageChamps.forget()
        self.menuInitial()
        
    def ajoutTableBD(self):
        nom=self.entryNomTable.get()
        if(nom==""):
            messagebox.showerror("Nom de table manquant a l'appel","Veuillez entrer un nom de table")
        elif(self.controleur.verificationExiste("nom", "Tables", "id_Projet", self.controleur.idProjet, nom)==False):
            messagebox.showerror("Table existante","Le nom de la table existe deja")
        else:
            self.controleur.ajoutTableBD(nom)
    
if __name__ == '__main__':
    c = Controleur()