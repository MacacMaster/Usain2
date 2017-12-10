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
        print(row)
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
        
    def changerEtat(self,etat,semaine):  
        for jours in semaine:
            for element in jours:
                element.config(state=etat)
        
    
    def populer(self,frame):
        #Label(frame, text="allo").grid(row=0, column=self.nbColonnes())
        #premiere rangee
        row = self.nbRangees()
        Label(frame, text="Utilisateur", width=10, borderwidth="5", relief="solid").grid(row=row, column=0)
        Label(frame, text="Sprint", width=10, borderwidth="5", relief="solid").grid(row=row, column=4)

        #dropdown menu 1
        OPTIONS = [
            "Usager 1",
            "Usager 2",
            "Usager 3"
        ]

 
        variable = StringVar(frame)
        variable.set(OPTIONS[0])
        w = OptionMenu(frame,variable,*OPTIONS)
        w.grid(row=row, column=1)


        #dropdown menu 2
        OPTIONS = [
            "Sprint 1",
            "Sprint 2",
            "Sprint 3"
        ]

        variable = StringVar(frame)
        variable.set(OPTIONS[0])
        w = OptionMenu(frame,variable,*OPTIONS)
        w.grid(row=row, column=5)
        
        button = Button(frame,text="Confirmer", command = self.updaterVue)
        button.grid(row=row, column=7)

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

        lesTaches = self.retournerLesTaches(1,1)
        self.taille = len(lesTaches)
        
        row = 4
        for element in lesTaches:
            tache = str(element[0])
            reussi = str(element[1])
            
            
            row += 1 
            i = row - 4 
            index = i
            labelTache = Label(frame, text="Tâche %s" % i, width=10, borderwidth="1", relief="solid")
            labelTache.config(bg="ivory3")
            labelTache.grid(row=row, column=0)
            
            #a.config(bg="green")
            #list.append(a)
            
            #t="aller acheter quelque chose au dollarama"
            t = tache
            Label(frame, text=t).grid(row=row, column=1)
            crochetFait = IntVar()
            cb = Checkbutton(frame, command=lambda row=row-5: self.changer(row), variable=crochetFait)
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
            
            self.list.append([labelTache,crochetFait,listeSemaine])
     
    def remplirFenetreSprints(self):
        pass
     
    def updaterVue(self):
        #effacer l'ancienne vue
         for element in self.frame.grid_slaves():
            element.grid_forget()
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
            
if __name__ == '__main__':
    v = Vue(None)
            
