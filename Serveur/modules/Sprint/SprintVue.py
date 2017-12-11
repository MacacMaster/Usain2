#-*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import *
import sqlite3
from datetime import datetime
from _overlapped import NULL

class Vue():
    def __init__(self, parent):
        self.jours = ("Lundi","Mardi","Mercredi","Jeudi","Vendredi")
        self.taille = 20
        self.list = []
        self.colonnes = 0
        self.rangees = 0
        self.choixSprint = None
        self.choixUtilisateur = None
        self.id_sprint = None
        self.id_utilisateur = None
        #self.choixSprint = "Sprint 1"
        #self.choixUtilisateur = "t"
        
        self.parent=parent
        self.creerFenetreSprints()
        
        
      
    def creerFenetreSprints(self):
        self.root = Tk()
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))
        
        caneva = Canvas(self.root, borderwidth=0, background="#ffffff")
        
        frame = Frame(caneva, background="#ffffff")
        self.frame=frame
        #mon scrollbar
        scrollbar = Scrollbar(self.root, orient="vertical", command=caneva.yview)
        caneva.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        caneva.pack(side="left", fill="both", expand=True)
        caneva.create_window((4,4), window=frame, anchor="nw")
        
        conteneur= Frame(self.root)
        conteneur.pack()
        
        frame.bind("<Configure>", lambda event, canvas=caneva: self.onFrameConfigure(caneva))
        self.populer(frame)
        
        mainloop()  
                   
    def onFrameConfigure(self,caneva):
        caneva.configure(scrollregion=caneva.bbox("all"))
    
    def creerUneLigne(self,parent, couleur): 
       frame = Frame(parent)
       frame.pack(side=BOTTOM)
       #frame.config(bg=couleur)
       Label(frame,text="la tache").pack(side=LEFT)
       Checkbutton(frame).pack(side=LEFT)
    
    def laSemaine(self,frame,jour,row):
        column = 3 + jour*3
        Label(frame, text=self.jours[jour]).grid(row=row, column=column, columnspan=3)
        Label(frame, text="5 décembre 2015").grid(row=row+1, column=column, columnspan= 3)
        Label(frame, text="Prévu").grid(row=row+2, column=column)
        Label(frame, text="Fait").grid(row=row+2, column=column+1)
        Label(frame, text="Temps").grid(row=row+2, column=column+2)
        
    def changer(self,row):
        try:
            label = self.list[row][0]
            bouton = self.list[row][1]
            semaine = self.list[row][2]
            if bouton.get():
                label.config(bg="green")
                #désactiver tous les autres boutons et entrées
        
                
                self.changerEtat(DISABLED,semaine)
                
        
                
            else:
                self.changerEtat(NORMAL,semaine)
                label.config(bg="ivory3")
        except IndexError:
            pass        
        
    def setSprint(self,var):
        self.choixSprint = var
        self.id_sprint = self.parcourirListe(self.lesSprints,self.choixSprint)
       
        
    def setUtilisateur(self,var):
        self.choixUtilisateur = var
        self.id_utilisateur = self.parcourirListe(self.lesUtilisateurs,self.choixUtilisateur)
       
        
    def changerEtat(self,etat,semaine):  
        for jours in semaine:
            for element in jours:
                element.config(state=etat)
        
    
    
    
    def populer(self,frame):
        self.retournerLesSprints()
        self.lesSprints = None
        self.lesUtilisateurs = None
        self.dicoSprints = None
        #Label(frame, text="allo").grid(row=0, column=self.nbColonnes())
        #premiere rangee
        row = self.nbRangees()
        Label(frame, text="Utilisateur", width=10, borderwidth="5", relief="solid").grid(row=row, column=0)
        Label(frame, text="Sprint", width=10, borderwidth="5", relief="solid").grid(row=row, column=4)

        #dropdown menu 1
        OPTIONS = []
        self.lesUtilisateurs = self.retournerLesUtilisateurs()
        
        for utilisateur in self.lesUtilisateurs:
            OPTIONS.append(utilisateur[1])
 
        variable = StringVar(frame)   
        if (self.choixUtilisateur == None):
            variable.set(OPTIONS[0])
        else:
            variable.set(self.choixUtilisateur)
        
        w = OptionMenu(frame,variable, *OPTIONS, command = self.setUtilisateur)
        w.grid(row=row, column=1)
            
        if (self.id_utilisateur == None):   
            self.setUtilisateur(OPTIONS[0]) 

        #dropdown menu 2
        self.lesSprints = self.retournerLesSprints()
        
        OPTIONS = []
        #OPTIONS.append(self.lesSprints[0][1])
        for sprint in self.lesSprints:
            OPTIONS.append(sprint[1])

        variable = StringVar(frame)  
        if (self.choixSprint == None):
            variable.set(OPTIONS[0])
        else:
            variable.set(self.choixSprint)
     
            
        w = OptionMenu(frame,variable,*OPTIONS, command=self.setSprint)
        w.grid(row=row, column=5)
          
        if (self.id_sprint == None):          
            self.setSprint(OPTIONS[0])       
               
        button = Button(frame,text="Confirmer", command = self.updaterVue)
        button.grid(row=row, column=7)
        
        button = Button(frame,text="Enregistrer", command = self.enregistrer)
        button.grid(row=row, column=9)
        
        #deuxieme rangee
        row = self.nbRangees()
        Label(frame, text="Les tâches", width=10, borderwidth="5", relief="solid").grid(row=row+2, column=0)
        t="Description de la tâche"
        Label(frame, text=t).grid(row=row+2, column=self.nbColonnes())
        Label(frame, text="Fait").grid(row=row+2, column=self.nbColonnes())
        for jour in range(5):
            self.laSemaine(frame,jour,row)
        #les jours de la semaine
        row = self.nbRangees() +3



        
        lesTaches = self.retournerLesTaches(self.id_sprint,self.id_utilisateur)
        self.taille = len(lesTaches)
        
        
        #4e rangee
        row = self.nbRangees()
        Label(frame, text="Nouvelle tâche", width=10, borderwidth="5").grid(row=row+2, column=0)
        entry = Entry(frame)
        entry.bind('<Return>',self.saisirNouvelleTache)
        entry.grid(row=row+2, column=1)
        entry.configure({"background": "Yellow"})
        
        row = 5
        for element in lesTaches:
            tache = str(element[0])
            reussi = element[1]
            
            
            row += 1 
            i = row - 5 
            index = row - 6
            labelTache = Label(frame, text="Tâche %s" % i, width=10, borderwidth="1", relief="solid")
            labelTache.config(bg="ivory3")
            labelTache.grid(row=row, column=0)
            
            #a.config(bg="green")
            #list.append(a)
            
            #t="aller acheter quelque chose au dollarama"
            t = tache
            Label(frame, text=t).grid(row=row, column=1)
            crochetFait = IntVar()
            self.checkParDefaut(crochetFait,reussi)
            cb = Checkbutton(frame, command=lambda row=index: self.changer(row), variable=crochetFait)
            cb.grid(row=row,column=2) #i=i permet d'enregistrer la valeur actuelle du i!!! Nice trick! :)
            
            #print(row, "    ", i)
            
         
            #pour les 5 jours de la semaine
            listeSemaine=[]
            for i in range(5):
                column = 3 + i *3
                fait = Checkbutton(frame)
                fait.grid(row=row,column=column)
                prevu = Checkbutton(frame)
                prevu.grid(row=row,column=column+1)
                entry = Entry(frame)
                entry.grid(row=row,column=column+2)
                listeSemaine.append([fait,prevu,entry])
          
            self.list.append([labelTache,crochetFait,listeSemaine,tache])
            
            #changer l'etat des boutons au loadage
            if (reussi):
                self.changer(index)
    
    def enregistrer(self):
        self.parent.enregistrer(self.list, self.id_utilisateur,self.id_sprint)
     
    def checkParDefaut(self, crochet, reussi):
        if reussi == 1: 
            crochet.set(1)

     
    def remplirFenetreSprints(self):
        pass
     
    def updaterVue(self):
        #effacer l'ancienne vue
         for element in self.frame.grid_slaves():
            element.grid_forget()
         self.list.clear()
         self.rangees = 0
         self.colonnes = 0
         self.populer(self.frame)
             
    def nbColonnes(self):
        self.colonnes += 1
        return self.colonnes  
    
    def nbRangees(self):
        self.rangees +=1
        return self.rangees-1
    
    def retournerLesTaches(self,id_sprint,id_utilisateur):
        return self.parent.retournerLesTaches(id_sprint,id_utilisateur)
    
    def retournerLesSprints(self):
        return self.parent.retournerLesSprints()
    
    def retournerLesUtilisateurs(self):
        return self.parent.retournerLesUtilisateurs()
    
    def parcourirListe(self,liste, recherche):
        index = -1
        for element in liste:
            index += 1
            if (str(element[1]) == str(recherche)):
                return element[0]
        return -1 #aucun id n'est négatif 
    
    def saisirNouvelleTache(self,event):
        saisie = str(event.widget.get())
        if (saisie != "" and self.choixSprint == "Sprint" or  self.choixUtilisateur == "Utilisateur" or self.choixSprint == None or self.choixUtilisateur == None):    
                messagebox.showwarning("Attention", "Veuillez choisir un sprint et un utilisateur")                                                 
                print(saisie)
        else:
            self.insererNouvelleTache(self.id_utilisateur,self.id_sprint,saisie,0)  
            self.updaterVue()  
        #effacer les choses déjà écrites
        event.widget.delete(0, END)
        
    def insererNouvelleTache(self, id_utilisateur, id_sprint, tache, reussi):
        return self.parent.insererNouvelleTache(id_utilisateur, id_sprint, tache, reussi)
        
            
if __name__ == '__main__':
    v = Vue(None)
            
