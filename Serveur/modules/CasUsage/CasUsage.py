from tkinter import *
from logging.config import listen
from ServeurBDcas import *

class Controleur():
    def __init__(self):
        self.serveur=ServeurBDcas(self)
        self.vue = Vue(self)
        self.modele = Modele(self)
        self.unReprend=False
        self.saasIP=sys.argv[1]
        self.utilisateur=sys.argv[2]
        self.organisation=sys.argv[3]
        self.idProjet=sys.argv[4]
        self.clientIP=sys.argv[5]
        self.etat="Non termine"
        self.adresseServeur="http://"+self.saasIP+":9998"
        self.serveurBd=ServerProxy(self.adresseServeur)
        self.IdCas=0
        self.idUtili=0
        self.idMachine=0
    
    def remplirListeCas(self):
        self.serveur.select("Description","CasUsage",idProjet)
    
    def remplirListeEtat(self):
        self.serveur.select("Etat","CasUsage",idProjet)
    
    def modifierCas(self,cas):#remplacer avec les bons noms
        idCas=self.serveur.chercher(idCas,casUsage,cas)
        self.serveur.update(casUsage,Description,cas,idCas,self.idProjet)
    
    def modifierUsager(self,usagertxt,cas):#remplacer avec les bons noms
        idCas=self.serveur.chercher(idCas,casUsage,cas)
        idUsager=self.serveur.chercher(idUtilisateur,Utilisateur,casUsage,idCas)
        self.serveur.update(utilisateur,Description,usagertxt,idUsager)
    
    def modifierMachine(self,cas,Machinetxt):#remplacer avec les bons noms
        idCas=self.serveur.chercher(idCas,casUsage,cas)
        idMachine=self.serveur.chercher(idUtilisateur,Machine,casUsage,idCas)
        self.serveur.update(machine,Description,machinetxt,idUsager)
         
    def envoyerCas(self,cas,usager,machine):
        self.serveur.insert("CasUSage",self.idProjet,idCas,cas,self.etat)
        self.envoyerScenari(usager, machine)
        self.vue.mettreAJourListes()
        self.IdCas+=1
    def envoyerScenari(self,utlisateurtxt,machinetxt):
        self.serveur.insert(utlisateur,idCas,utlisateurtxt,self.idUtili,self.etat)
        self.serveur.insert(machine,idCas,machinetxt,self.idMachine,self.etat)
        
    def chercherBdcas(self,indice):
        cas=self.serveur.chercher(Description,casUsage,cas)
        return cas

    def chercherUtilisateur(self,indice):
        utilisateur=self.serveur.chercherBdUtilisateur(indice)
        return utilisateur
    
    def chercherMachine(self,indice):
        machine=self.serveur.chercherBdMachine(indice)
        return machine
    
    def changerEtat(self,cas):#a faire
        idCas=self.serveur.chercher(idCas,casUsage,cas)
        etat=self.serveur.chercher("Etat",casUsage,self.idProjet,idcas)
        EtatCompare=Etat.fetchone()[0]
        if(EtatCompare=="NonTerminé"):
            self.serveur.update(CasUsage,"Etat",)
        elif(EtatCompare=="Terminé"):
             self.serveur.update(CasUsage,"Etat",)
        elif(EtatCompare=="Reprendre"):
             self.serveur.update(CasUsage,"Etat",) 
        self.vue.caneva.forget()
        self.vue.menuInitial()
        
    def changerReprendre(self,etat):
        self.serveur.changerEtatReprendre(etat)
        self.vue.caneva.forget()
        self.vue.menuInitial()

class Modele():
    def __init__(self, pControleur):
        self.controleur = pControleur
        print("modele")
        self.cas=[]
        self.Etat=[]

class Cas():
   def __init__(self,text,idcas,etatini):
        self.etat=etatini
        self.description=text
        self.id=idcas

class Vue():
    def __init__(self, pControleur):
        self.controleur = pControleur
        self.largeur = 800
        self.hauteur = 600
        self.root = Tk()
        self.fenetre = Frame(self.root, width = self.largeur, height = self.hauteur)
        self.fenetre.pack()
        self.listeCas=[]
        self.listeEtat=[]
        self.dejaOuvert=False
        self.indiceCasModifier=0
        self.menuInitial()

    def mettreAJourListes(self):
        self.remplirListeEtat()
        self.remplirListeCas()
        self.remplirListBoxEtat()
        self.remplirListBoxCas()    
    
    def menuInitial(self):
        
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

        self.btnEnvoyerUsager=Button(self.caneva,text="Envoyer",width=20,command=self.envoyerTexte)
        self.caneva.create_window(400,200,window=self.btnEnvoyerUsager,width=150,height=20)
    
        self.btnModifier=Button(self.caneva,text="Modifier",width=20,command=self.indiceDeLaBD)
        self.caneva.create_window(700,550,window=self.btnModifier,width=150,height=20)
        
        self.bntSupprimer=Button(self.caneva,text="Terminé/NonTerminé",width=20,command=self.supprimer)#
        self.caneva.create_window(100,550,window=self.bntSupprimer,width=150,height=20)
        
        self.bntReprendre=Button(self.caneva,text="Reprendre",width=20,command=self.reprendre)
        self.caneva.create_window(self.largeur/2,550,window=self.bntReprendre,width=150,height=20)
        
        self.listeetat=Listbox(self.caneva,bg="lightblue",borderwidth=0,relief=FLAT,width=12,height=12)
        self.caneva.create_window(670,350,window=self.listeetat)
       

        self.listecas=Listbox(self.caneva,bg="lightblue",borderwidth=0,relief=FLAT,width=90,height=12)
        self.caneva.create_window(350,350,window=self.listecas)
        self.mettreAJourListes()

        if(self.dejaOuvert==False):
            self.ouvrirReprendre()
            
    def unSeulReprendre(self):
        for i in range(1,self.listeetat.size()+1):
            etat=self.listeetat.get(ACTIVE)
            self.listeetat.activate(i)
            etat2= str(etat)
            if(etat2=="('Reprendre',)"):
                self.controleur.unReprend=True
                
                
    def ouvrirReprendre(self):
        compteur=0
        for i in range(1,self.listeetat.size()+1):
            compteur+=1
            etat=self.listeetat.get(ACTIVE)
            self.listeetat.activate(i)
            etat2= str(etat)
            if(etat2=="('Reprendre',)"):
                self.indiceCasModifier=compteur-1
                self.dejaOuvert=True
                self.menuModifier()
               
        
    def reprendre(self):
        self.unSeulReprendre()
        if(self.controleur.unReprend==False):  
            self.indiceCasModifier=self.listeetat.curselection()[0]
            self.controleur.changerReprendre(self.indiceCasModifier)
    
    
    
    def indiceDeLaBD(self):
        self.indiceCasModifier=self.listecas.curselection().get()[0]
        print("indice a modifier : ",self.indiceCasModifier)
        self.menuModifier()
    def recevoirDonnees(self,liste):
        pass
    
    def remplirListeCas(self):
        self.listeCas=self.controleur.remplirListeCas()
   
    def remplirListeEtat(self):
        self.listeEtat=self.controleur.remplirListeEtat()
    
    def remplirListBoxCas(self):
        self.listecas.delete(0, END)
        for i in self.listeCas:
            self.listecas.insert(END,i)
        self.listeCas.clear()
            
    def remplirListBoxEtat(self):
        self.listeetat.delete(0, END)
        for i in self.listeEtat:
            self.listeetat.insert(END,i)
        self.listeEtat.clear()
        
    def menuModifier(self):
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
    
        cas=self.controleur.chercherBdcas(self.indiceCasModifier,);
        self.labelCasUsage.insert(END, str (cas))
       
        usager=self.controleur.chercherUtilisateur(self.indiceCasModifier+1,)#
        self.labelActionUsager.insert(END, str(usager))
        
        
        machine=self.controleur.chercherMachine(self.indiceCasModifier+1,)#
        self.labelActionMachine.insert(END,str(machine))
        
        self.canevaMod.create_window(400,200,window=self.labelActionUsager,width=150,height=250)
        self.labnbe=Label(text="Action machine",bg="lightblue")
        self.canevaMod.create_window(650,50,window=self.labnbe)
        self.btnEnvoyerUsager=Button(self.canevaMod,text="Envoyer",width=20,command=self.envoyerTexte)
        self.canevaMod.create_window(400,200,window=self.btnEnvoyerUsager,width=150,height=20)
    
        self.btnRetour=Button(self.canevaMod,text="Retour",width=20,command=self.menuInitialMod)
        self.canevaMod.create_window(100,550,window=self.btnRetour,width=150,height=20)
        
        self.bntModifier=Button(self.canevaMod,text="Modifier",width=20,command=self.modifierTexte)
        self.canevaMod.create_window(150,400,window=self.bntModifier,width=150,height=20)
    
        
    def supprimer(self):
        self.indiceCasModifier=self.listeetat.curselection()[0]
        self.controleur.changerEtat(self.indiceCasModifier)
        
    def menuInitialMod(self):
        self.canevaMod.forget()
        self.menuInitial()
        
    def modifierTexte(self):
        cas=self.labelCasUsage.get()
        usager=self.labelActionUsager.get()
        machine=self.labelActionMachine.get()
        self.controleur.modifierCas(cas,usager,machine)
        self.controleur.modifierUtilisateur(cas,usager)
        self.controleur.modifierMachine(cas,machine)
        
    
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
    
if __name__ == '__main__':
    c = Controleur()