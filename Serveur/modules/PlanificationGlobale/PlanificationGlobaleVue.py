#-*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import *
import sqlite3
from datetime import datetime
from _overlapped import NULL



class Vue():
    def __init__(self, parent):
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
        self.canPrincipal=Canvas(self.framePrincipal, width=1000, height=800, bg="steelblue", )
        self.canPrincipal.pack()
        
        self.lblProchain=Label(self.framePrincipal, text="Prochaine action: ", width=150, height=30, bg="light blue", relief=RAISED)
        self.canPrincipal.create_window(100,40, window=self.lblProchain, width=120, height=30)
        StrAction="Ici sera affichee la prochaine action a effectuer par l'utilisateur"
        self.lblAction=Label(self.framePrincipal, text=StrAction, width=750, height=30, bg="white", relief=RAISED)
        self.canPrincipal.create_window(575,40, window=self.lblAction, width=750, height=30)
        
        
        #self.lblFonctionnalite=Label(self.framePrincipal, text="Fonctionnalite", width=100, height=80, bg="white", relief=RAISED )
        #self.canAnalyse.create_window(75,120,window=self.labelExplicite, width=100, height=120)
        
        
        
        
        
        
        """self.fentrecreationplanif.pack()
        self.btnSauvegarder=Button(self.fentrecreationplanif)
        
        self.lbltemps=Label(self.fentrecreationplanif,font=("Arial",15,"bold"), bg="white")
        self.lbltemps.configure(text=" " + str(self.parent.modele.getTime))
        self.lblcrc= Label(master=self.fentrecreationplanif,text="")
        pass"""
    
    
    def fenetreConfirmation(self):
        
        pass
    
    
    