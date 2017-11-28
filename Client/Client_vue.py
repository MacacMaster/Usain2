# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import tix
from tkinter import ttk
from tkinter import messagebox

class Vue():
    def __init__(self,pControleur,pClientIp):
        self.controleur = pControleur
        self.largeur = 800
        self.hauteur = 600
        self.cadreActuel = None
        self.labIDOrga = None
        self.labNomOrga = None
        self.root=tix.Tk()
        self.root.title("SPRINTMASTER")
        self.root.protocol("WM_DELETE_WINDOW", self.controleur.fermerApplication)
        self.cadreApplication = Frame(self.root, width = self.largeur, height = self.hauteur)
        self.cadreApplication.pack()
        self.centrerFenetre()
        
        self.creerCadreModules()
        self.creerCadreLogIn(pClientIp)
        self.changeCadre(self.cadreLogIn)
    
    def centrerFenetre(self):
        self.root.update() # Suivant le WM. A faire dans tous les cas donc.
        fenrw = self.root.winfo_reqwidth()
        fenrh = self.root.winfo_reqheight()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+%d+%d" % (fenrw, fenrh, (sw-fenrw)/2, (sh-fenrh)/2))
    
    def changeCadre(self,cadre):
        if self.cadreActuel:
            self.cadreActuel.pack_forget()
        self.cadreActuel=cadre
        self.cadreActuel.pack()
            
    def creerCadreLogIn(self,ip):
        largeur = self.root.winfo_reqwidth()
        hauteur = self.root.winfo_reqheight()
        self.cadreLogIn=Frame(self.cadreApplication)
        self.canevaLogIn=Canvas(self.cadreLogIn,width=largeur,height=hauteur) 
        labNomOrga=Label(text="Nom organisation",bg="grey",borderwidth=0,relief=RIDGE,fg="black", font=("Helvetica", 12))
        labNomUsager=Label(text="Nom usager",bg="grey",borderwidth=0,relief=RIDGE,fg="black", font=("Helvetica", 12))
        labMDP=Label(text="Mot de passe",bg="grey",borderwidth=0,relief=RIDGE,fg="black", font=("Helvetica", 12))
        self.entrerNomOrga=Entry(bg="white")
        self.entrerNomUsager=Entry(bg="white")
        self.entrerMotDePasse=Entry(bg="white", show="*")
        btnLogInClient=Button(text="Se connecter", command=self.logInClient)
        
        self.canevaLogIn.create_window(largeur/2,250,window=labNomOrga,width=150,height=30)
        self.canevaLogIn.create_window(largeur/2,300,window=self.entrerNomOrga,width=150,height=30)
        self.canevaLogIn.create_window(largeur/2,350,window=labNomUsager,width=150,height=30)
        self.canevaLogIn.create_window(largeur/2,400,window=self.entrerNomUsager,width=150,height=30)
        self.canevaLogIn.create_window(largeur/2,450,window=labMDP,width=150,height=30)
        self.canevaLogIn.create_window(largeur/2,500,window=self.entrerMotDePasse,width=150,height=30)
        self.canevaLogIn.create_window(largeur/2,550,window=btnLogInClient,width=150,height=30) 
        self.canevaLogIn.pack()
        
    def logInClient(self):
        identifiantNomOrga = self.entrerNomOrga.get()
        identifiantNomUsager = self.entrerNomUsager.get()
        identifiantMotDePasse = self.entrerMotDePasse.get()
        print("Nom de l'organisation entré par l'usager:", identifiantNomOrga,"Nom entré par l'usager ", identifiantNomUsager, "Mot de passe entré par l'usager ", identifiantMotDePasse)
        self.controleur.logInClient(identifiantNomUsager, identifiantNomOrga,identifiantMotDePasse)
    
    def logInClientFail(self):
        messagebox.showwarning('Connexion refus�e', 'Nom de compte ou mot de passe incorrect.')
        
    
    def chooseProjectFail(self):
        messagebox.showwarning('Projet inconnu', 'Merci de s�l�ctionner un projet existant.')
    
    def creerCadreCentral(self):
        self.cadreCentral=Frame(self.cadreApplication)
        self.cadreProjet = Frame(self.cadreCentral)
        self.canevaProjet=Canvas(self.cadreProjet,width=400,height=600,bg="green")
        self.canevaProjet.pack()
        self.listeProjets=Listbox(self.cadreProjet, bg="lightblue",borderwidth=0,relief=FLAT,width=40,height=6)
        btnconnecter=Button(self.cadreProjet, text="Choisir un Projet",bg="pink",command=self.chargerProjet)
        btnCreerProjet=Button(self.cadreProjet, text="Creer un Projet",bg="pink",command=self.chargerProjet)
        self.canevaProjet.create_window(200,100,window=self.listeProjets)
        
        self.canevaProjet.create_window(100,20,window=self.labNomOrga,width=100,height=15)
        self.canevaProjet.create_window(250,20,window=self.labIDOrga,width=100,height=15)
        self.canevaProjet.create_window(200,450,window=btnconnecter,width=100,height=30)
        self.canevaProjet.create_window(200,500,window=btnCreerProjet,width=100,height=30)
        self.cadreProjet.pack(side=LEFT)
        
        #----------------------------
        self.cadreOutil = Frame(self.cadreCentral)
        self.canevaOutil=Canvas(self.cadreOutil,width=400,height=600,bg="lightgreen")
        self.canevaOutil.pack()
        
        self.listeOutils=Listbox(self.cadreOutil, bg="lightblue",borderwidth=0,relief=FLAT,width=40,height=6)
        btnconnecter=Button(self.cadreOutil, text="Choisir un outil",bg="pink",command=self.requeteOutil)
        self.canevaOutil.create_window(200,100,window=self.listeOutils)
        self.canevaOutil.create_window(200,450,window=btnconnecter,width=100,height=30)
        
        self.cadreOutil.pack(side=LEFT)
        
    def creerCadreModules(self):
        self.cadreCentral2=Frame(self.cadreApplication)
        self.cadreModules=Frame(self.cadreCentral2)
        self.canevaModules=Canvas(self.cadreModules,width=800,height=600,bg="green")
        self.canevaModules.pack()
        self.listeModules=Listbox(self.cadreModules, bg="lightblue",borderwidth=0,relief=FLAT,width=40,height=6)
        btnconnecter=Button(self.cadreModules, text="Choisir un Module",bg="pink",command=self.requeteModule)
        self.canevaModules.create_window(200,100,window=self.listeModules)
        self.canevaModules.create_window(200,450,window=btnconnecter,width=100,height=30)
        self.cadreModules.pack(side=LEFT)
        
    def chargerProjet(self):
        if self.listeProjets.curselection():
            nomprojet=self.listeProjets.selection_get()
            self.controleur.chargerProjet(nomprojet, self.controleur.idOrga);
            self.changeCadre(self.cadreCentral2)
        else:
            self.chooseProjectFail()
         
    def requeteProjet(self):
        mod=self.listeProjets.selection_get()
        if mod:
            self.controleur.requeteProjet(mod)
        
    def requeteModule(self):
        mod=self.listeModules.selection_get()
        if mod:
            self.controleur.requeteModule(mod)

    def requeteOutil(self):
        mod=self.listeOutils.selection_get()
        if mod:
            self.controleur.requeteOutil(mod)
            
    def chargerCentral(self,repNomClient,repmodules, repoutils, repprojets):
        
        self.labNomOrga=Label(text="Nom usager: "+self.controleur.utilisateur,borderwidth=0,relief=RIDGE,fg="black", font=("Helvetica", 10))
        self.labIDOrga=Label(text="Id organisation: "+self.controleur.idOrga,borderwidth=0,relief=RIDGE,fg="black", font=("Helvetica", 10))
        self.creerCadreCentral()
        
        for i in repprojets:
            self.listeProjets.insert(END,i)
        for i in repmodules:
            self.listeModules.insert(END,i)
        for i in repoutils:
            self.listeOutils.insert(END,i)
        self.changeCadre(self.cadreCentral)