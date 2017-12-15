from tkinter import *
from logging.config import listen
from xmlrpc.client import ServerProxy


class Controleur():
    def __init__(self):
        self.saasIP=        sys.argv[1]
        self.utilisateur=   sys.argv[2]
        self.organisation=  sys.argv[3]
        self.idProjet=      sys.argv[4]
        self.clientIP=      sys.argv[5]
        self.portSaas=":9999"
        self.adresseServeur="http://"+self.saasIP+self.portSaas
        self.serveur = self.connectionServeur()
        self.vue = Vue(self)
        self.idScena=0
        self.unReprend=False
        self.remplirListeCas()
        
        self.writeLog("Ouverture du Module","2")
        self.vue.root.mainloop()
   
    def fermerProgramme(self):
        self.writeLog("Fermeture du Module","3")
        self.vue.root.destroy()
        
    def writeLog(self,action,codeid):
        self.serveur.writeLog(self.organisation,self.utilisateur,self.clientIP,self.saasIP,"CasUsage",action,codeid)
   
    def connectionServeur(self):
        serveur=ServerProxy(self.adresseServeur)
        return serveur
    
    def remplirListeCas(self):
        nomTable = "CasUsages"
        champs = "description"
        where = ["id_Projet"]
        valeur = [self.idProjet]

        requete = self.serveur.selDonneesWHERE(nomTable,champs,where,valeur)
        return requete

        
    def remplirListeEtat(self):
        nomTable = "CasUsages"
        champs = "etat"
        where = ["id_Projet"]
        valeur = [self.idProjet]
        requete = self.serveur.selDonneesWHERE(nomTable,champs,where,valeur)
        return requete
    
           
    def envoyerCas(self,cas,usager,machine):
        self.serveur.insertionSQL("CasUsages","'"+str(self.idProjet)+"','"+cas+"','Termine'")
        indiceCas=self.serveur.selectionSQL3("CasUsages","id","description",str(cas))
        indiceCas=str(indiceCas)[2:int(len(indiceCas)-3)]

        self.serveur.insertionSQL("Humains","'"+str(indiceCas)+"','"+usager+"'")
        self.serveur.insertionSQL("Machines","'"+str(indiceCas)+"','"+machine+"'")
        self.vue.mettreAJourListes()
   
    def chercherBdcas(self,indice):

        return self.serveur.selectionSQL3("CasUsages","description","id",indice)
       
    def chercherUtilisateur(self,indice):

        nomTable = "Humains"
        champs = "etat"
        where = ["id_CasUsage"]
        valeur = [indice]

        requete = self.serveur.selDonneesWHERE(nomTable,champs,where,valeur)

        return requete
    
    def chercherMachine(self,indice):
        nomTable = "Machines"
        champs = "etat"
        where = ["id_CasUsage"]
        valeur = [indice]

        requete = self.serveur.selDonneesWHERE(nomTable,champs,where,valeur)
        return requete
    
    def changerEtat(self,indice):
        nomTable = "CasUsages"
        champs = "etat"
        where = ["id","id_Projet"]
        valeur = [indice,self.idProjet]
        Etat = self.serveur.selDonneesWHERE(nomTable,champs,where,valeur)
        nomTableGood=str(Etat)[3:int(len(Etat)-4)]
        
        if(nomTableGood=="NonTermine"): 
            self.serveur.updateSQL2("CasUsages","Termine","etat","id",indice)
        elif(nomTableGood=="Termine"):
            self.serveur.updateSQL2("CasUsages","NonTermine","etat","id",indice)
        elif(nomTableGood=="Reprendre"):
            self.serveur.updateSQL2("CasUsages","NonTermine","etat","id",indice)
        self.unReprend=False;
        self.vue.caneva.forget()
        self.vue.menuInitial()
    
    def modifierCas(self,cas,usager,machine,indice):

        self.serveur.updateSQL2("casUsages",cas,"description","id",indice)
        self.serveur.updateSQL2("Humains",usager,"etat","id_CasUsage",indice)
        self.serveur.updateSQL2("Machines",machine,"etat","id_CasUsage",indice)
   

    def indiceCasModifier(self, nomCas):
        nomTable = "CasUsages"
        champs = "id"
        where = ["description"]
        valeur = [nomCas]
        indice=self.serveur.selDonneesWHERE(nomTable,champs,where,valeur)
        indiceGood=str(indice)[2:int(len(indice)-3)]
        print(indiceGood)
        return indiceGood
    
    def changerReprendre(self,indice):
        self.serveur.updateSQL2("CasUsages","Reprendre","etat","id",indice)
        self.vue.caneva.forget()
        self.vue.menuInitial()
    
class Vue():
    def __init__(self, pControleur):
        self.controleur = pControleur
        self.largeur = 800
        self.hauteur = 600
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.controleur.fermerProgramme)
        self.fenetre = Frame(self.root, width = self.largeur, height = self.hauteur)
        self.fenetre.pack()
        self.listeCas=[]
        self.listeEtat=[]
        self.dejaOuvert=False
        self.indice=0
        self.menuInitial()

    def mettreAJourListes(self):
        self.remplirListeEtat()
        self.remplirListeCas()
        self.remplirListBoxEtat()
        self.remplirListBoxCas()    
    
    def menuInitial(self,indice=0):
        self.caneva = Canvas(self.fenetre, width = self.largeur, height=self.hauteur, bg="steelblue")
        self.caneva.pack()
        self.labnbe=Label(text="Cas d'usage       ",bg="lightblue")
        self.caneva.create_window(150,50,window=self.labnbe)
        self.labelCasUsage=Entry(bg="white")
        self.caneva.create_window(150,120,window=self.labelCasUsage,width=150,height=100)
        
        self.labnbe=Label(text="Action usager    ",bg="lightblue")
        self.caneva.create_window(400,50,window=self.labnbe)
        self.labelActionUsager=Entry(bg="white")
        self.caneva.create_window(400,120,window=self.labelActionUsager,width=150,height=100)
        self.labnbe=Label(text="Action machine",bg="lightblue")
        self.caneva.create_window(650,50,window=self.labnbe)
        self.labelActionMachine=Entry(bg="white")
        self.caneva.create_window(650,120,window=self.labelActionMachine,width=150,height=100)

        self.btnEnvoyerUsager=Button(self.caneva,text="Envoyer",font="Arial 8 ",width=20,command=self.envoyerTexte)
        self.caneva.create_window(400,200,window=self.btnEnvoyerUsager,width=150,height=20)
    
        self.btnModifier=Button(self.caneva,text="Modifier",font="Arial 8 ",width=20,command=self.indiceDeLaBD)
        self.caneva.create_window(150,475,window=self.btnModifier,width=150,height=20)
        
        self.bntSupprimer=Button(self.caneva,text="Terminé/NonTerminé",width=20,font="Arial 8 ",command=self.supprimer)
        self.caneva.create_window(675,475,window=self.bntSupprimer,width=110,height=20)
        
       
        self.bntReprendre=Button(self.caneva,text="Reprendre",width=20,font="Arial 8 ",command=self.reprendre)
        self.caneva.create_window(675,525,window=self.bntReprendre,width=110,height=20)
        
        self.listeetat=Listbox(self.caneva,bg="lightblue",borderwidth=0,relief=FLAT,width=12,height=12)
        self.caneva.create_window(670,350,window=self.listeetat)
       

        self.listecas=Listbox(self.caneva,bg="lightblue",borderwidth=0,relief=FLAT,width=90,height=12)
        self.caneva.create_window(350,350,window=self.listecas)
        self.mettreAJourListes()
        if(self.dejaOuvert==False):
            self.ouvrirReprendre()


    def indiceCas(self, nomCas):
        return self.controleur.indiceCasModifier(nomCas)
   
    def indiceDeLaBD(self):
        position=self.listecas.curselection()[0]
        nomCasSelection=self.listecas.get(position, position)
        if(position!=0):
            nomCasSelectionGood=str(nomCasSelection)[2:int(len(nomCasSelection)-4)]
        else: 
            nomCasSelectionGood=nomCasSelection

        indice =self.indiceCas(nomCasSelectionGood)

        self.menuModifier(indice)
  
    def trouverCasReprendre(self,position):
        nomCasSelection=self.listecas.get(position, position)
        if(position!=0):
            nomCasSelectionGood=str(nomCasSelection)[2:int(len(nomCasSelection)-4)]
        else: 
            nomCasSelectionGood=nomCasSelection
        
        indice=self.indiceCas(nomCasSelectionGood)
        return indice
    def remplirListeCas(self):
        self.listeCas=self.controleur.remplirListeCas()
   
    def remplirListeEtat(self):
        self.listeEtat=self.controleur.remplirListeEtat()
    
    def remplirListBoxCas(self):
        self.listecas.delete(0, END)
        laselection=self.controleur.remplirListeCas()
       
        for i in laselection:
            temp=str(i)[2:int(len(i)-3)]
            self.listecas.insert(END,temp)
        self.listeCas.clear()
            
    def remplirListBoxEtat(self):
        self.listeetat.delete(0, END)
        for i in self.listeEtat:
            temp=str(i)[2:int(len(i)-3)]
            self.listeetat.insert(END,temp)
        self.listeEtat.clear()
        
    def menuModifier(self,indice):
        self.caneva.forget()
        self.canevaMod = Canvas(self.fenetre, width = self.largeur, height=self.hauteur, bg="steelblue")
        self.canevaMod.pack()
        self.labnbe=Label(text="Cas d'usage       ",bg="lightblue")
        self.canevaMod.create_window(150,50,window=self.labnbe)
        self.labelCasUsage=Entry(bg="white")
        self.canevaMod.create_window(150,200,window=self.labelCasUsage,width=150,height=250)
        
        self.labnbe=Label(text="Action usager    ",bg="lightblue")
        self.canevaMod.create_window(400,50,window=self.labnbe)
        self.labelActionUsager=Entry(bg="white")
        self.labelActionMachine=Entry(bg="white")
        self.canevaMod.create_window(650,200,window=self.labelActionMachine,width=150,height=250)
        self.indice=indice
        cas=self.controleur.chercherBdcas(indice,);
        cas=str(cas)[3:int(len(cas)-4)]

        self.labelCasUsage.insert(END, str (cas))
        
        usager=self.controleur.chercherUtilisateur(indice,)#
        usager=str(usager)[3:int(len(usager)-4)]
        self.labelActionUsager.insert(END, str(usager))

        machine=self.controleur.chercherMachine(indice,)
        machine=str(machine)[3:int(len(machine)-4)]
        self.labelActionMachine.insert(END,str(machine))
        
        self.canevaMod.create_window(400,200,window=self.labelActionUsager,width=150,height=250)
        self.labnbe=Label(text="Action machine",bg="lightblue")
        self.canevaMod.create_window(650,50,window=self.labnbe)
        self.btnEnvoyerUsager=Button(self.canevaMod,text="Envoyer",font="Arial 8 ",width=20,command=self.envoyerTexte)
        self.canevaMod.create_window(400,200,window=self.btnEnvoyerUsager,width=150,height=20)
        self.btnRetour=Button(self.canevaMod,text="Retour",font="Arial 8 ",width=20,command=self.menuInitialMod)
        self.canevaMod.create_window(100,550,window=self.btnRetour,width=150,height=20)
        self.bntModifier=Button(self.canevaMod,text="Modifier",font="Arial 8 ",width=20,command=self.modifierTexte)
        self.canevaMod.create_window(150,400,window=self.bntModifier,width=150,height=20)
    
        
    def supprimer(self):
        position=self.listeetat.curselection()[0]
        nomCas=self.listecas.get(position,position) # indice du cas selectionné
        if(position!=0):
           nomCasSelectionGood=str(nomCas)[2:int(len(nomCas)-4)]
        else: 
            nomCasSelectionGood=nomCas
        self.indiceCasModifier=self.controleur.indiceCasModifier(nomCasSelectionGood)
        self.controleur.changerEtat(self.indiceCasModifier)
    
    def menuInitialMod(self):
        self.canevaMod.forget()
        self.menuInitial()
       
    def modifierTexte(self):
        cas=self.labelCasUsage.get()
        usager=self.labelActionUsager.get()
        machine=self.labelActionMachine.get()
        self.controleur.modifierCas(cas,usager,machine,self.indice)
        
    def envoyerTexte(self):
        cas=self.labelCasUsage.get()
        usager=self.labelActionUsager.get()
        machine=self.labelActionMachine.get()
        self.insererCas(cas,usager,machine)
        self.labelActionUsager.delete(0, 'end')
        self.labelCasUsage.delete(0, 'end')
        self.labelActionMachine.delete(0, 'end')

    def insererCas(self,cas,usager,machine):
        self.controleur.envoyerCas(cas,usager,machine)
                             
    def ouvrirReprendre(self):
        for i in range(1,self.listeetat.size()+1):
            etat=self.listeetat.get(ACTIVE)
            self.listeetat.activate(i)
            etat2= str(etat)
            if(etat2=="Reprendre"):
                indice=self.trouverCasReprendre(i-1)
                self.dejaOuvert=True
                self.menuModifier(indice)
             
    
    def unSeulReprendre(self):
        test=False
        for i in range(1,self.listeetat.size()+1):
            etat=self.listeetat.get(ACTIVE)
            self.listeetat.activate(i)
            etat2= str(etat)
            if(etat2=="Reprendre"):
                test=True
        return test   
    
    def reprendre(self):
      #  if(position = self.listeetat.curselection()[0])
        
        reprend=self.unSeulReprendre()
        if(reprend==False):  
            position=self.listeetat.curselection()[0] 
            indice=self.trouverCasReprendre(position)
            self.controleur.changerReprendre(indice)
    
if __name__ == '__main__':
    c = Controleur()