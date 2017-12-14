# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math


class Vue():
    def __init__(self,parent,largeur=800,hauteur=600):
        self.controleur = parent
        self.root=tix.Tk()
        self.root.title("Facturation d'un client")
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.parent=parent
        self.modele=None
        self.largeur=largeur
        self.hauteur=hauteur
        self.images={}
        self.cadreactif=None
        self.creercadres()
        self.changecadre(self.cadreFact)
        self.centrerFenetre()
        
    def changemode(self,cadre):
        if self.modecourant:
            self.modecourant.pack_forget()
        self.modecourant=cadre
        self.modecourant.pack(expand=1,fill=BOTH)            

    def changecadre(self,cadre,etend=0):
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif=cadre
        if etend:
            self.cadreactif.pack(expand=1,fill=BOTH)
        else:
            self.cadreactif.pack()
        
    def centrerFenetre(self):
        self.root.update() # Suivant le WM. A faire dans tous les cas donc.
        fenrw = self.root.winfo_reqwidth()
        fenrh = self.root.winfo_reqheight()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+%d+%d" % (fenrw, fenrh, (sw-fenrw)/2, (sh-fenrh)/2))
        
    def creercadres(self):
        self.creercadreFact()
         
    def creercadreFact(self):
        self.cadreFact=Frame(self.root)
        self.canevaFact=Canvas(self.cadreFact,width=280,height=520,bg="steelblue")
        self.canevaFact.pack()
        lTitre=Label(text="Facturation",bg="lightgrey",borderwidth=0,relief=RIDGE,fg="steelblue", font=("Helvetica", 18))
        self.canevaFact.create_window(140,40,window=lTitre,width=240,height=40)
        self.listeOrganisation=Listbox(self.cadreFact, bg="lightblue",borderwidth=0,relief=FLAT,width=25,height=8)
        self.canevaFact.create_window(140,140,window=self.listeOrganisation)
        btnconnecter=Button(self.cadreFact, text="Choisir une organisation",bg="lightblue",command=self.afficherFact)
        self.canevaFact.create_window(142,240,window=btnconnecter,width=160,height=30)
        for i in self.controleur.serveur.selectionSQL("Organisations","nom"):
            self.listeOrganisation.insert(END,i[0])
        
    def afficherFact(self):
        self.calculUtilisation()
        val=1.00;
        valSousTotal=round(val+(self.valUtilisation*0.2),2)
        valTPS=round(valSousTotal*0.05,2)
        valTVQ=round(valSousTotal*0.0975,2)
        valTotal = round(valSousTotal+valTPS+valTVQ,2)
        lSousTotal=Label(text="Sous-total : ",bg="steelblue",borderwidth=0,relief=RIDGE,fg="lightblue", font=("Helvetica.BOLD", 14, ))
        self.canevaFact.create_window(120,350,window=lSousTotal,width=100,height=32)
        lValST=Label(text=str(valSousTotal)+" $",bg="steelblue",borderwidth=0,relief=RIDGE,fg="lightblue", font=("Helvetica", 14))
        self.canevaFact.create_window(230,350,window=lValST,width=80,height=32)
        lTPS=Label(text="TPS : ",bg="steelblue",borderwidth=0,relief=RIDGE,fg="lightblue", font=("Helvetica", 14))
        self.canevaFact.create_window(130,390,window=lTPS,width=80,height=32)
        lValTPS=Label(text=str(valTPS)+" $",bg="steelblue",borderwidth=0,relief=RIDGE,fg="lightblue", font=("Helvetica", 14))
        self.canevaFact.create_window(230,390,window=lValTPS,width=80,height=32)
        lTVQ=Label(text="TVQ : ",bg="steelblue",borderwidth=0,relief=RIDGE,fg="lightblue", font=("Helvetica", 14))
        self.canevaFact.create_window(130,430,window=lTVQ,width=80,height=32)
        lValTVQ=Label(text=str(valTVQ)+" $",bg="steelblue",borderwidth=0,relief=RIDGE,fg="lightblue", font=("Helvetica", 14))
        self.canevaFact.create_window(230,430,window=lValTVQ,width=80,height=32)
        lTotal=Label(text="Total : ",bg="steelblue",borderwidth=0,relief=RIDGE,fg="lightblue", font=("Helvetica", 14))
        self.canevaFact.create_window(130,470,window=lTotal,width=80,height=32)
        lValTotal=Label(text=str(valTotal)+" $",bg="steelblue",borderwidth=0,relief=RIDGE,fg="lightblue", font=("Helvetica", 14))
        self.canevaFact.create_window(230,470,window=lValTotal,width=80,height=32)
        
    def calculUtilisation(self):
        self.valUtilisation = 0.00
        indiceRech = self.listeOrganisation.curselection()
        nomOrga = self.listeOrganisation.get(indiceRech)
        for i in self.controleur.serveur.selectBdInterne("logs","Date","ErrorID","Organisation", "2",nomOrga):
            self.valUtilisation+=1
        for i in self.controleur.serveur.selectBdInterne("logs","Date","ErrorID","Organisation", "3",nomOrga):
            self.valUtilisation+=1
        
        
        
        
    def fermerfenetre(self):
        self.root.destroy()
        print("ONFERME la fenetre")
    