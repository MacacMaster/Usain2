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
        self.root.protocol("WM_DELETE_WINDOW", self.parent.fermerProgramme)
        self.fenetre = Frame(master=self.root, width=self.largeurTotale, height=self.hauteurTotale)
        self.fenetre.pack()
                   

        self.barreTaches()
        self.framePrincipal()
        self.frameCommandes()
        self.frameAjoutModif()
        self.afficherListes()
        
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
        
        #creation de listbox non visibles pour debut et fin (pour constance lors de la select dune fonctionnalite
        self.listDebut=Listbox(self.framePrincipal)
        self.listFin=Listbox(self.framePrincipal)
        
        self.listFonct.bind('<<ListboxSelect>>',self.selectFonct)
        
     
    def selectFonct(self, e):
        self.fonctEnCours=self.listFonct.curselection()
        self.tfFonctionnalite.delete(0,END)
        self.tfFonctionnalite.insert(0,str(self.listFonct.get(self.fonctEnCours)))
        self.tfPriorite.delete(0,END)
        self.tfPriorite.insert(0,str(self.listPriorite.get(self.fonctEnCours)))
        self.tfSprint.delete(0,END)
        self.tfSprint.insert(0,str(self.listSprint.get(self.fonctEnCours)))
        self.tfDebut.delete(0,END)
        self.tfDebut.insert(0,str(self.listDebut.get(self.fonctEnCours)))
        self.tfFin.delete(0,END)
        self.tfFin.insert(0,str(self.listFin.get(self.fonctEnCours)))
        self.tfResponsable.delete(0,END)
        self.tfResponsable.insert(0,str(self.listResponsable.get(self.fonctEnCours)))
        
    
    def frameCommandes(self):
        self.frameCommandes = Frame(self.fenetre,width=self.largeurSub, height=self.hauteurSub, padx=10, pady=10, bg="light blue")
        self.frameCommandes.pack(fill=X)
        self.canCommandes=Canvas(self.frameCommandes, width=1000, height=70, bg="light grey", )
        self.canCommandes.pack()
        
        self.btnNouvFonct=Button(self.frameCommandes, text="Ajouter fonctionnalite", width=40, bg="pink", command=self.ajoutFonction)
        self.canCommandes.create_window(100,35,window=self.btnNouvFonct,width=150,height=35)
        self.btnModifFonct=Button(self.frameCommandes, text="Modifier fonctionnalite", width=40, bg="pink", command=self.modifierFonction)
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
        self.canAjoutModif.create_window(90,30, window=self.lblAMFonctionnalite, width=120, height=25)
        
        self.lblAMPriorite=Label(self.frameAjoutModif, text="Priorite: ", width=120, height=25)
        self.canAjoutModif.create_window(90,60, window=self.lblAMPriorite, width=120, height=25)
        
        self.lblAMSprint=Label(self.frameAjoutModif, text="Sprint: ", width=120, height=25)
        self.canAjoutModif.create_window(90,90, window=self.lblAMSprint, width=120, height=25)
        
        self.lblAMDebut=Label(self.frameAjoutModif, text="Debut: ", width=120, height=25)
        self.canAjoutModif.create_window(90,120, window=self.lblAMDebut, width=120, height=25)
        
        self.lblAMFin=Label(self.frameAjoutModif, text="Fin: ", width=120, height=25)
        self.canAjoutModif.create_window(90,150, window=self.lblAMFin, width=120, height=25)
        
        self.lblAMResponsable=Label(self.frameAjoutModif, text="Responsable: ", width=120, height=25)
        self.canAjoutModif.create_window(90,180, window=self.lblAMResponsable, width=120, height=25)
        
        #textfields
        self.tfFonctionnalite=Entry(self.frameAjoutModif, width=700)
        self.canAjoutModif.create_window(550,30, window=self.tfFonctionnalite, width=700, height=25)
        
        self.tfPriorite=Entry(self.frameAjoutModif, width=700)
        self.canAjoutModif.create_window(550,60, window=self.tfPriorite, width=700, height=25)
        
        self.tfSprint=Entry(self.frameAjoutModif, width=700)
        self.canAjoutModif.create_window(550,90, window=self.tfSprint, width=700, height=25)
        
        self.tfDebut=Entry(self.frameAjoutModif, width=700)
        self.canAjoutModif.create_window(550,120, window=self.tfDebut, width=700, height=25)
        
        self.tfFin=Entry(self.frameAjoutModif, width=700)
        self.canAjoutModif.create_window(550,150, window=self.tfFin, width=700, height=25)
        
        self.tfResponsable=Entry(self.frameAjoutModif, width=700)
        self.canAjoutModif.create_window(550,180, window=self.tfResponsable, width=700, height=25)
        
        #bouton
        self.btnEffacer=Button(self.frameAjoutModif, text="Clear", width=100, bg="pink", command=self.effacerChamps)
        self.canAjoutModif.create_window(950,105,window=self.btnEffacer,width=50,height=120)
    
    def effacerChamps(self):
        self.tfFonctionnalite.delete(0,END)
        self.tfPriorite.delete(0,END)
        self.tfSprint.delete(0,END)
        self.tfDebut.delete(0,END)
        self.tfFin.delete(0,END)
        self.tfResponsable.delete(0,END)
    
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
        
    def infosCRC(self):
        print("ENTRE DANS infosCRC")
        kj=self.parent.serveur.selectionSQL3('Classes','id','id_Projet', self.parent.idProjet)
        print(str(kj))
        #nomTable,champs, where, idProjet
    
    def afficherListes(self):
        
         
        self.listFonct.delete(0,END)
        self.listPriorite.delete(0,END)
        self.listSprint.delete(0,END)
        self.listPourcentage.delete(0,END)
        self.listResponsable.delete(0,END)
        
        self.parent.updateListe()
        
        
        for liste in self.parent.listeFonctions:
                self.listFonct.insert(END, liste[4])
                self.listPriorite.insert(END, liste[5])
                self.listSprint.insert(END, liste[2])
                self.listDebut.insert(END, liste[6])
                self.listFin.insert(END, liste[7])
                self.listResponsable.insert(END, liste[3])
        
        if self.listFonct.size()==0:
            self.infosCRC()
        
        """
        for item in fonctions:
            self.listFonct.insert(END, item)
            
        for item in priorites:
            self.listPriorite.insert(END, item)
            
        for item in sprints:
            self.listSprint.insert(END, item)
            
        for item in pourcents:
            self.listPourcentage.insert(END, item)
            
        for item in responsables:
            self.listResponsable.insert(END, item)"""
            
    
    
    def ajoutFonction(self):
        #sprint,nomfonction,priorite,debut,fin
        self.parent.creerFonction(self.tfSprint.get(), self.tfFonctionnalite.get(), self.tfPriorite.get(), self.tfDebut.get(), self.tfFin.get())
        print(self.tfSprint.get() + self.tfFonctionnalite.get() + self.tfPriorite.get() + self.tfDebut.get() + self.tfFin.get())
        self.effacerChamps()
        self.afficherListes()

        
        
    def suppressionFonction(self):
        self.parent.supressionFonction()
        self.effacerChamps()
        self.afficherListes()
    
    
    def modifierFonction(self):
        #valeurModifiee,champModifier,id
        #self,nomTable,champ,description,where,indice1
        id=self.fonctEnCours
        id=str(id)[1:int(len(id)-3)]
        print(str(id))
        self.parent.sql.modifierFonction(self.tfSprint.get(),"id_Sprint", str(id))
        self.parent.sql.modifierFonction(self.tfResponsable.get(),"id_Reponsable", str(id))
        self.parent.sql.modifierFonction(self.tfFonctionnalite.get(),"nom_fonction", str(id))
        self.parent.sql.modifierFonction(self.tfPriorite.get(),"priorite", str(id))
        self.parent.sql.modifierFonction(self.tfDebut.get(),"date_debut", str(id))
        self.parent.sql.modifierFonction(self.tfFin.get(),"date_fin", str(id))
        self.effacerChamps()
        self.afficherListes()
    
    