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
        self.root.resizable(width=False, height=False)
        self.root.title("SPRINTMASTER")
        self.root.iconbitmap('Icon.ico')
        self.root.protocol("WM_DELETE_WINDOW", self.controleur.fermerApplication)
        self.cadreApplication = Frame(self.root, width = self.largeur, height = self.hauteur)
        self.cadreApplication.pack()
        self.centrerFenetre()
        self.statut=0
        self.photo=PhotoImage(file=('Logo.gif'))
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
        
        
        
        
        self.canevaLogIn.create_image(0, 0, image=self.photo, anchor=NW)
        

        self.photoLogo=PhotoImage(file='Title2.gif')
        self.panel = Label(image = self.photoLogo)

        
        
        self.canevaLogIn.create_window(largeur/2,65,window=self.panel,width=largeur)
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
        if(identifiantNomUsager == "admin"):
            self.statut=1
        self.controleur.logInClient(identifiantNomUsager, identifiantNomOrga,identifiantMotDePasse)
    
    def logInClientFail(self, code):
        if code == 0:
            messagebox.showwarning('Connexion refus�e', 'Nom de compte ou mot de passe incorrect.')
        elif code == 1:
            messagebox.showwarning('Connexion refus�e', 'Un utilisateur utilise déjà ce compte.')
        elif code == 2:
            messagebox.showwarning('Connexion refus�e', 'Veuillez remplir les champs avant de vous connecter.')
        else:
            messagebox.showwarning('Connexion refus�e', 'Une erreur technique a eu lieu, merci de contacter le staff.')
        
    
    def chooseProjectFail(self):
        messagebox.showwarning('Projet inconnu', 'Merci de s�l�ctionner un projet existant.')
        self.parent.log.writeLog("Projet Inconnu","PE1")
    
    def creerCadreCentral(self):
        
        if(self.statut == 1):
            self.cadreCentral=Frame(self.cadreApplication)
            self.cadreProjet = Frame(self.cadreCentral)
            self.canevaProjet=Canvas(self.cadreProjet,width=400,height=600,bg="steelblue")
            self.canevaProjet.pack()
            self.listeProjets=Listbox(self.cadreProjet, bg="lightblue",borderwidth=0,relief=FLAT,width=40,height=6)
            btnconnecter=Button(self.cadreProjet, text="Choisir un Projet",bg="lightgrey",command=self.chargerProjet)
            btnCreerProjet=Button(self.cadreProjet, text="Creer un Projet",bg="lightgrey",command=self.creerProjet)
            self.canevaProjet.create_window(200,100,window=self.listeProjets)
        
            self.canevaProjet.create_window(200,150,window=self.listeProjets)
            self.canevaProjet.create_window(100,30,window=self.labNomOrga,width=150,height=30)
            self.canevaProjet.create_window(300,30,window=self.labIDOrga,width=150,height=30)
            self.canevaProjet.create_window(200,500,window=btnconnecter,width=100,height=30)
            self.canevaProjet.create_window(200,550,window=btnCreerProjet,width=100,height=30)
            self.cadreProjet.pack(side=LEFT)
        
        #----------------------------
            self.cadreOutil = Frame(self.cadreCentral)
            self.canevaOutil=Canvas(self.cadreOutil,width=400,height=600,bg="lightgrey")
            self.canevaOutil.pack()
            self.listeOutils=Listbox(self.cadreOutil, bg="lightblue",borderwidth=0,relief=FLAT,width=40,height=7)
            btnconnecter=Button(self.cadreOutil, text="Choisir un outil",bg="steelblue",command=self.requeteOutil)
            btnCommande=Button(self.cadreOutil, text="Envoyer une requete SQL",bg="steelblue",command=self.commandeAdmin)
            btnCommandeSaas=Button(self.cadreOutil, text="Envoyer une requete SAAS",bg="steelblue",command=self.commandeAdminSaas)
            self.canevaOutil.create_window(200,100,window=self.listeOutils)
            self.canevaOutil.create_window(200,180,window=btnconnecter,width=100,height=30)
            self.canevaOutil.create_window(200,220,window=btnCommandeSaas,width=200,height=30)
            self.canevaOutil.create_window(200,260,window=btnCommande,width=200,height=30)
            self.cadreOutil.pack(side=LEFT)
        else:
            self.cadreCentral=Frame(self.cadreApplication)
            self.cadreProjet = Frame(self.cadreCentral)
            self.canevaProjet=Canvas(self.cadreProjet,width=800,height=600,bg="steelblue")
            self.canevaProjet.pack()
            self.listeProjets=Listbox(self.cadreProjet, bg="black", fg="white",borderwidth=0,relief=FLAT,width=40,height=6)
            btnconnecter=Button(self.cadreProjet, text="Choisir un Projet",bg="lightgrey",command=self.chargerProjet)
            btnCreerProjet=Button(self.cadreProjet, text="Creer un Projet",bg="lightgrey",command=self.creerProjet)
            self.canevaProjet.create_image(0, 0, image=self.photo, anchor=NW)
            self.canevaProjet.create_window(380,150,window=self.listeProjets)
            self.canevaProjet.create_window(275,30,window=self.labNomOrga,width=150,height=30)
            self.canevaProjet.create_window(525,30,window=self.labIDOrga,width=150,height=30)
            self.canevaProjet.create_window(380,500,window=btnconnecter,width=100,height=30)
            self.canevaProjet.create_window(380,550,window=btnCreerProjet,width=100,height=30)
            self.cadreProjet.pack(side=LEFT)
        
    def creerCadreModules(self):
        self.cadreCentral2=Frame(self.cadreApplication)
        self.cadreModules=Frame(self.cadreCentral2)
        self.canevaModules=Canvas(self.cadreModules,width=800,height=600,bg="steelblue")
        self.canevaModules.pack()
        self.canevaModules.create_image(0, 0, image=self.photo, anchor=NW)
        self.listeModules=Listbox(self.cadreModules, bg="black", fg="white", borderwidth=0,relief=FLAT,width=40,height=7)
        btnconnecter=Button(self.cadreModules, text="Choisir un Module",bg="lightgrey",command=self.requeteModule)
        self.canevaModules.create_window(200,150,window=self.listeModules)
        self.canevaModules.create_window(200,500,window=btnconnecter,width=100,height=30)
        self.cadreModules.pack(side=LEFT)
    
    def creerProjet(self):
        if(self.statut == 0):
            largeur = 380;
        else:
            largeur = 180;
        labNomProjet=Label(text="Nom du projet",bg="darkblue",borderwidth=0,relief=RIDGE,fg="white", font=("Helvetica", 12))
        self.canevaProjet.create_window(largeur,400,window=labNomProjet,width=150,height=30)
        self.entrerNomProjet=Entry(bg="lightblue")
        self.canevaProjet.create_window(largeur,450,window=self.entrerNomProjet,width=150,height=30)
        btnNProjet=Button(self.cadreProjet, text="Ok",bg="lightgrey",command=self.okProjet)
        self.canevaProjet.create_window(largeur+150,450,window=btnNProjet,width=50,height=30) 
        
    def commandeAdmin(self):
        self.affCommande=Text(bg="lightblue")
        self.canevaOutil.create_window(200,475,window=self.affCommande,width=300,height=90)
        btnNEnvoi=Button(self.cadreOutil, text="SQL",bg="steelblue",command=self.envoiSQL)
        self.canevaOutil.create_window(200,560,window=btnNEnvoi,width=50,height=30) 
    
    def commandeAdminSaas(self):
        self.affCommandeSaas=Text(bg="lightblue")
        self.canevaOutil.create_window(200,325,window=self.affCommandeSaas,width=300,height=90)
        btnNEnvoiSaas=Button(self.cadreOutil, text="SAAS",bg="steelblue",command=self.envoiSQLSaas)
        self.canevaOutil.create_window(200,410,window=btnNEnvoiSaas,width=50,height=30)
    
    def envoiSQL(self):
        self.controleur.serveur.commandeAdmin(self.affCommande.get(0.0, END))
        
    def envoiSQLSaas(self):
        self.controleur.serveur.commandeAdminSaas(self.affCommandeSaas.get(0.0, END)) 
        
    def okProjet(self):
        self.nouveauProjet = self.controleur.creerProjet(self.entrerNomProjet.get())
        self.listeProjets.insert(END,self.entrerNomProjet.get())
        
        
    def chargerProjet(self):
            if self.listeProjets.curselection():
                nomprojet=self.listeProjets.selection_get()
                self.controleur.chargerProjet(nomprojet);
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
        if(self.statut ==1):
            for i in repoutils:
                self.listeOutils.insert(END,i)
        self.changeCadre(self.cadreCentral)