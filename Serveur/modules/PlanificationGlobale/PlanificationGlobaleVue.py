#-*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import *
import sqlite3
from datetime import datetime
from _overlapped import NULL



class Vue():
    def __init__(self, parent):
        print("in vue")
        self.parent=parent
        self.root=Tk() #Fenetre
        self.root.title("Planification Globale")
        self.hauteurTotale=600
        self.largeurTotale=800
        self.hauteurSub=500
        self.largeurSub=800
        self.fenetre = Frame(master=self.root, width=self.largeurTotale, height=self.hauteurTotale)
        self.fenetre.pack()
                   

        self.barreTaches()
        self.framePrincipal()
        self.frameCommandes()
        self.frameAjoutModif()
        
    def barreTaches(self):
        #menu deroulante

        self.menubar = Menu(self.root)
        self.menubar.add_command(label="Enregistrer", command= NULL)
        self.menubar.add_command(label="Charger un fichier")
        self.menubar.add_separator()
        #self.menubar.add_command(label=self.parent.modele.getTime())#, command= lambda: self.parent.modele.enregistrer(self.text))
        self.root.config(menu=self.menubar)

    def framePrincipal(self):
        self.framePrincipal = Frame(self.fenetre,width=self.largeurSub, height=self.hauteurSub, padx=10, pady=10, bg="light blue")
        self.framePrincipal.pack(fill=X)
        self.canPrincipal=Canvas(self.framePrincipal, width=1000, height=530, bg="steelblue", )
        self.canPrincipal.pack()
        
        self.lblProchain=Label(self.framePrincipal, text="Prochaine action: ", width=150, height=30, bg="light blue")
        self.canPrincipal.create_window(90,40, window=self.lblProchain, width=120, height=30)
        self.StrAction="Ici sera affichee la prochaine action a effectuer par l'utilisateur"
        self.lblAction=Label(self.framePrincipal, text=self.StrAction, width=800, height=30, bg="pink")
        self.canPrincipal.create_window(575,40, window=self.lblAction, width=800, height=30)
        
        
        self.lblFonct=Label(self.framePrincipal, text="Fonctionnalite", width=600, height=25, bg="white", relief=RAISED )
        self.canPrincipal.create_window(330,90,window=self.lblFonct, width=600, height=25)
        self.lblPriorite=Label(self.framePrincipal, text="Priorite", width=60, height=25, bg="white", relief=RAISED )
        self.canPrincipal.create_window(660,90,window=self.lblPriorite, width=60, height=25)
        self.lblSprint=Label(self.framePrincipal, text="Sprint", width=60, height=25, bg="white", relief=RAISED )
        self.canPrincipal.create_window(720,90,window=self.lblSprint, width=60, height=25)
        self.lblPourcentage=Label(self.framePrincipal, text="%", width=70, height=25, bg="white", relief=RAISED )
        self.canPrincipal.create_window(785,90,window=self.lblPourcentage, width=70, height=25)
        self.lblResponsable=Label(self.framePrincipal, text="Responsable", width=160, height=25, bg="white", relief=RAISED )
        self.canPrincipal.create_window(900,90,window=self.lblResponsable, width=160, height=25)
        
        self.listFonct=Listbox(self.framePrincipal, width=599, height=400)
        self.canPrincipal.create_window(330,305,window=self.listFonct, width=599, height=400)
        self.listPriorite=Listbox(self.framePrincipal, width=59, height=400)
        self.canPrincipal.create_window(660,305,window=self.listPriorite, width=59, height=400)
        self.listSprint=Listbox(self.framePrincipal, width=59, height=400)
        self.canPrincipal.create_window(720,305,window=self.listSprint, width=59, height=400)
        self.listPourcentage=Listbox(self.framePrincipal, width=69, height=400)
        self.canPrincipal.create_window(785,305,window=self.listPourcentage, width=69, height=400)
        self.listResponsable=Listbox(self.framePrincipal, width=159, height=400)
        self.canPrincipal.create_window(900,305,window=self.listResponsable, width=159, height=400)
        
        #A RETIRER!
        self.listFonct.insert(END, "Hello")
        self.listFonct.insert(END, "World")
        print("cur:"+str(self.listFonct.get(ACTIVE)))
        
      
    
    def frameCommandes(self):
        self.frameCommandes = Frame(self.fenetre,width=self.largeurSub, height=self.hauteurSub, padx=10, pady=10, bg="light blue")
        self.frameCommandes.pack(fill=X)
        self.canCommandes=Canvas(self.frameCommandes, width=1000, height=70, bg="light grey", )
        self.canCommandes.pack()
        
        self.btnNouvFonct=Button(self.frameCommandes, text="Ajouter fonctionnalite", width=40, bg="pink")
        self.canCommandes.create_window(100,35,window=self.btnNouvFonct,width=150,height=35)
        self.btnModifFonct=Button(self.frameCommandes, text="Modifier fonctionnalite", width=40, bg="pink",)
        self.canCommandes.create_window(300,35,window=self.btnModifFonct,width=150,height=35)
        self.btnSuppFonct=Button(self.frameCommandes, text="Supprimer fonctionnalite", width=40, bg="pink", command=self.fenetreConfirmation)
        self.canCommandes.create_window(500,35,window=self.btnSuppFonct,width=150,height=35)
        self.btnChangerProjet=Button(self.frameCommandes, text="Changer de projet", width=40, bg="light blue")
        self.canCommandes.create_window(900,35,window=self.btnChangerProjet,width=150,height=35)
    
    
    def frameAjoutModif(self):
        self.frameAjoutModif = Frame(self.fenetre,width=self.largeurSub, height=self.hauteurSub, padx=10, pady=10, bg="light blue")
        self.frameAjoutModif.pack(fill=X)
        self.canAjoutModif=Canvas(self.frameAjoutModif, width=1000, height=200, bg="steelblue")
        self.canAjoutModif.pack()
        
        self.lblAMFonctionnalite=Label(self.frameAjoutModif, text="Fonctionnalite: ", width=120, height=25)
        self.canAjoutModif.create_window(90,40, window=self.lblAMFonctionnalite, width=120, height=25)
        
        self.lblAMPriorite=Label(self.frameAjoutModif, text="Priorite: ", width=120, height=25)
        self.canAjoutModif.create_window(90,70, window=self.lblAMPriorite, width=120, height=25)
        
        self.lblAMSprint=Label(self.frameAjoutModif, text="Sprint: ", width=120, height=25)
        self.canAjoutModif.create_window(90,100, window=self.lblAMSprint, width=120, height=25)
        
        self.lblAMPourcent=Label(self.frameAjoutModif, text="%: ", width=120, height=25)
        self.canAjoutModif.create_window(90,130, window=self.lblAMPourcent, width=120, height=25)
        
        self.lblAMResponsable=Label(self.frameAjoutModif, text="Responsable: ", width=120, height=25)
        self.canAjoutModif.create_window(90,160, window=self.lblAMResponsable, width=120, height=25)
        
        self.tfFonctionnalite=Entry(self.frameAjoutModif, width=750)
        self.canAjoutModif.create_window(575,40, window=self.tfFonctionnalite, width=750, height=25)
        
        self.tfPriorite=Entry(self.frameAjoutModif, width=750)
        self.canAjoutModif.create_window(575,70, window=self.tfPriorite, width=750, height=25)
        
        self.tfSprint=Entry(self.frameAjoutModif, width=750)
        self.canAjoutModif.create_window(575,100, window=self.tfSprint, width=750, height=25)
        
        self.tfPourcent=Entry(self.frameAjoutModif, width=750)
        self.canAjoutModif.create_window(575,130, window=self.tfPourcent, width=750, height=25)
        
        self.tfResponsable=Entry(self.frameAjoutModif, width=750)
        self.canAjoutModif.create_window(575,160, window=self.tfResponsable, width=750, height=25)
        
    def fenetreConfirmation(self):
        self.topConfirm=Toplevel(height=200)
        self.topConfirm.title("Confimation de supression")
        msg = Message(self.topConfirm, text="Voulez-vous vraiment supprimer cette fonctionnalité?")
        msg.pack()
        btnConfirmation=Button(self.topConfirm, text="Oui", command=self.optionAnnuler)
        btnConfirmation.pack()
        btnAnnuler=Button(self.topConfirm, text="Annuler", command=self.topConfirm.destroy)
        btnAnnuler.pack()
        
    def optionAnnuler(self):
        print("Envoi de la fonction supression du controleur avec listFonct.get(ACTIVE) en parametre")
        index=self.listFonct.index(ACTIVE)
        
        #suppression dans les listbox
        self.listFonct.delete(index)
        self.listPriorite.delete(index)
        self.listSprint.delete(index)
        self.listPourcentage.delete(index)
        self.listResponsable.delete(index)
        
        self.topConfirm.destroy()
        
    
    def afficherListes(fonctions, priorites, sprints, pourcents, responsables):
        
        listFonct.delete(0,END)
        listPriorite.delete(0,END)
        listSprint.delete(0,END)
        listPourcentage.delete(0,END)
        listResponsable.delete(0,END)
        
        for item in fonctions:
            self.listFonct.insert(END, item)
            
        for item in priorites:
            self.listPriorite.insert(END, item)
            
        for item in sprints:
            self.listSprint.insert(END, item)
            
        for item in pourcents:
            self.listPourcentage.insert(END, item)
            
        for item in responsables:
            self.listResponsable.insert(END, item)
            
    
    
    
    