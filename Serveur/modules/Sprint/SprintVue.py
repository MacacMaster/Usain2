#-*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import *
import sqlite3
import datetime
from _overlapped import NULL

class Vue():
    def __init__(self, parent):
        self.parent=parent
        self.jours = ("Lundi","Mardi","Mercredi","Jeudi","Vendredi")
        self.mois = ("Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre")
        self.datePrevu = None
        self.color = "light blue"
        self.changementDeSemaine = False
        self.joursSemaineValides= []
        self.lesCinqJours = []
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.fermerProgramme)
        self.taille = 20
        self.list = []
        self.colonnes = 0
        self.rangees = 0
        self.choixSprint = None
        self.choixUtilisateur = None
        self.id_sprint = None
        self.id_utilisateur = None
        self.creerFenetreSprints()

        
        
        try:
            pass
        except:
            pass
        #self.choixSprint = "Sprint 1"
        #self.choixUtilisateur = "t"
        
    def fermerProgramme(self):
        self.parent.writeLog("Fermeture du Module","M73")
        self.root.destroy()
        
    def setDate(self,premier,deuxieme, date):
        
        if deuxieme == 1: #si on choisit un mois
            compteur = 0
            for mois in self.mois:
                if (str(mois) == date.get()):
                    compteur = compteur + 1
                    self.matriceDates[premier][deuxieme] = compteur
                    return
                    break
        
        else:
            self.matriceDates[premier][deuxieme] = int(date.get())
        
      
    def creerFenetreSprints(self):
        

        
        

        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))
        
        caneva = Canvas(self.root, borderwidth=0, background=self.color)
        
        frame = Frame(caneva, background=self.color)
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
       Checkbutton(frame,bg= self.color).pack(side=LEFT)
    
    def laSemaine(self,frame,jour,row, i):
        
        self.lesCinqJours.append(self.datePrevu)
 
        column = 3 + jour*3
        taille = 3
        if column % 2 == 0:
            couleur = "lightskyblue"
            Label(frame, text=self.jours[jour], bg = "lightskyblue").grid(row=row, column=column, columnspan=taille)
        else:
            couleur = "steelblue"
            Label(frame, text=self.jours[jour], bg = "steelblue").grid(row=row, column=column, columnspan=taille)
        if self.aucunSprint == False:
            try:
                dateDebut = self.dateEnFormatUtilisable(self.leSprint[0][2])
                dateFin = self.dateEnFormatUtilisable(self.leSprint[0][3])
            except IndexError:
                dateDebut = dateFin = self.datePrevu
            #vérifier que la date à afficher se trouve dans l'interval
            if dateDebut <= self.datePrevu and dateFin >= self.datePrevu:
                self.joursSemaineValides.append(True)
                Label(frame, text=self.datePrevu,bg= couleur).grid(row=row+1, column=column, columnspan= 3)
            else:
                self.joursSemaineValides.append(False)
          
                Label(frame, text=self.datePrevu,bg= couleur).grid(row=row+1, column=column, columnspan= 3)
        
            Label(frame, text="Prévu",bg= self.color).grid(row=row+2, column=column)
            Label(frame, text="Fait",bg= self.color).grid(row=row+2, column=column+1)
            Label(frame, text="Temps", bg= self.color).grid(row=row+2, column=column+2)
                
        else:
            Label(frame, text="").grid(row=row+1, column=column, columnspan= 3)
            Label(frame, text="Prévu",bg= self.color).grid(row=row+2, column=column)
            Label(frame, text="Fait",bg= self.color).grid(row=row+2, column=column+1)
            Label(frame, text="Temps",bg= self.color).grid(row=row+2, column=column+2)

        self.datePrevu += datetime.timedelta(days=1)
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
        #changer l'état seulement pour les jours de la semaine qui font partie du sprint
        compteur = 0
        for jours in semaine:
            if self.joursSemaineValides[compteur]:
                for element in jours:
                    try:
                        element.config(state=etat)
                    except AttributeError:
                        pass
            compteur = compteur + 1
        
    
    
    def ajouterUnSprint(self):
        
        
        self.window =  Toplevel(self.root)
        
        #frame 1
        #drop down 1
        self.matriceDates = []
        self.matriceDates.append([2016,1,1])
        self.matriceDates.append([2016,1,1])
        for i in range(2):
            self.creerUneLigneSaisie(self.window,i)
        frameBouton = Frame(self.window)
        frameBouton.pack()
        bouton = Button(frameBouton,text="Créer le sprint", command = self.creerLeSprint)
        bouton.pack()
        
    def creerLeSprint(self):
        #debut = datetime.date(self.matriceDates[0][0],5,1)
        try:
            debut = datetime.date(self.matriceDates[0][0],self.matriceDates[0][1],self.matriceDates[0][2])
            fin = datetime.date(self.matriceDates[1][0],self.matriceDates[1][1],self.matriceDates[1][2])
            #date= 8
            #d = datetime.date(2017,12,date)
            
            self.insererNouveauSprint(debut,fin, "Sprint n")
            self.on_closing()
        except TypeError:
            messagebox.showwarning("Échec", "La date entrée est invalide!")
            return    
       
        
    def creerUneLigneSaisie(self,window, nb):

        frameDebut = Frame(self.window)
        frameDebut.pack()

        #année
        OPTIONS = ["Année"]
        for i in range (2017,2022):
            OPTIONS.append(i)
        
        annee = StringVar(self.window)   
        annee.set(OPTIONS[0])
        w = OptionMenu(frameDebut,annee, *OPTIONS, command = lambda y=nb  :self.setDate(nb,0,annee))

        w.pack(side=LEFT)
        
        #mois
        
        OPTIONS = self.mois
        

        
        mois = StringVar(self.window)   
        mois.set(OPTIONS[0])
        w = OptionMenu(frameDebut,mois, *OPTIONS, command = lambda y=nb  :self.setDate(nb,1,mois))
        w.pack(side=LEFT)
        
        #jours
        OPTIONS = ["Jour"]
        for i in range (1,32):
            OPTIONS.append(i)
        
        jour = StringVar(self.window)   
        jour.set(OPTIONS[0])
        w = OptionMenu(frameDebut,jour, *OPTIONS, command = lambda y=nb  :self.setDate(nb,2,jour))
        w.pack(side=LEFT)
        


        self.matriceDates.append([annee.get(),mois.get(),jour.get()])
 
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        self.updaterVue()
        self.window.destroy()

    def prochain(self):
        #passer a la prochaine semaine
        self.enregistrer()
        self.datePrevu = self.lesCinqJours[0]+ datetime.timedelta(days=7)
        self.changementDeSemaine = True
        self.updaterVue()
        #self.populer(self.frame)
        pass
    
    def precedent(self):
        #passer a la prochaine semaine
        self.enregistrer()
        self.datePrevu = self.lesCinqJours[0]- datetime.timedelta(days=7)
        self.changementDeSemaine = True
        self.updaterVue()
        #self.populer(self.frame)
        pass
    
    def populer(self,frame):
        self.aucunSprint = False
        self.retournerLesSprints()
        self.lesSprints = None
        self.lesUtilisateurs = None
        self.dicoSprints = None

        #premiere rangee
        row = self.nbRangees()
        Label(frame, text="Utilisateur", width=10, borderwidth="1", relief="solid",bg= self.color).grid(row=row, column=0, rowspan = 1)
        b  = Button(frame, text="+", width=10, borderwidth="5", command = self.ajouterUnSprint)
        
        
        b.grid(row=row, column=3)
        Label(frame, text="Sprint", width=10, borderwidth="5", relief="solid").grid(row=row, column=4)
        
        #bouton pour passer a la prochaine semaine
        Button(frame, text="Prochain", bg= "blue", fg = "white", command = self.prochain).grid(row=1, column=18)
        Button(frame, text="Précédent", bg= "blue", fg = "white", command = self.precedent).grid(row=1, column=3)

        #try:
            #dropdown menu 1
        
        OPTIONS = []
        self.lesUtilisateurs = self.retournerLesUtilisateurs()
        
        for utilisateur in self.lesUtilisateurs:
            OPTIONS.append(utilisateur[1])

        
        variable = StringVar(frame)   
        if (self.choixUtilisateur == None):
            try:
                variable.set(OPTIONS[0])
            except IndexError:
                variable.set("")
        else:
            variable.set(self.choixUtilisateur)
      
        try:
            w = OptionMenu(frame,variable, *OPTIONS, command = self.setUtilisateur)
        except TypeError:
            #OPTIONS = [1]
            w = OptionMenu(frame,variable, *OPTIONS, command = self.setUtilisateur)
        w.grid(row=row, column=1)
            
        if (self.id_utilisateur == None):   
            self.setUtilisateur(OPTIONS[0]) 
    
        #dropdown menu 2
        self.lesSprints = self.retournerLesSprints()   
        OPTIONS = []
        #OPTIONS.append(self.lesSprints[0][1])
        for sprint in self.lesSprints:
            self.aucunSprint = False
            OPTIONS.append(sprint[1])

        variable = StringVar(frame)  
        if (self.choixSprint == None):
            try:
                variable.set(OPTIONS[0])
            except IndexError:
                self.aucunSprint = True
                variable.set("")
        else:
            variable.set(self.choixSprint)
     
        try:
            w = OptionMenu(frame,variable,*OPTIONS, command=self.setSprint)
        except TypeError:
            OPTIONS = [" "]
            w = OptionMenu(frame,variable,*OPTIONS, command=self.setSprint)
            w.configure(state="disabled")
            self.aucunSprint = True
       
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
        Label(frame, text=t,bg= self.color).grid(row=row+2, column=self.nbColonnes())
        Label(frame, text="Fait",bg= self.color).grid(row=row+2, column=self.nbColonnes())
        i = 0 
        self.leSprint = (self.retournerLeSprint(self.id_sprint))
       
       
#         try:
#             self.retournerLeSprint(self.id_sprint)
#       
#         except IndexError:
#             pass
        
        if self.aucunSprint == False:
            if self.datePrevu == None:
                try:
                    self.datePrevu = self.dateEnFormatUtilisable(self.leSprint[0][2])
                except IndexError:
                    self.datePrevu = datetime.date.today()
        else:
            self.datePrevu = datetime.date.today()

        
        for jour in range(5):       
            self.laSemaine(frame,jour,row, i)
            i = i + i 
        #les jours de la semaine
        row = self.nbRangees() +3



        
        lesTaches = self.retournerLesTaches(self.id_sprint,self.id_utilisateur)
        self.taille = len(lesTaches)
        
        
        #4e rangee
        row = self.nbRangees()
        Label(frame, text="Nouvelle tâche", width=10, borderwidth="5",bg= self.color).grid(row=row+2, column=0)
        if (self.aucunSprint == True):
            entry = Entry(frame, state = DISABLED)
            b.config(bg = "yellow")
        else:
            entry = Entry(frame, state = NORMAL)
            b.config(bg = "gainsboro")
        entry.bind('<Return>',self.saisirNouvelleTache)
        entry.grid(row=row+2, column=1)
        entry.configure({"background": "Yellow"})
        
        if self.aucunSprint == True:
            l = Label(frame, text="----------------------------Ajouter un sprint svp!!!----------------------------")
            l.config(bg = "yellow")
            l.grid(row=6, column=4, columnspan = 5)
     
        
        row = 5
        for element in lesTaches:

            tache = str(element[0])
            reussi = element[1]
            id_tache = str(element[2])
            
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
            Label(frame, text=t,bg= self.color).grid(row=row, column=1)
            crochetFait = IntVar()
            self.checkParDefaut(crochetFait,reussi)
            cb = Checkbutton(frame, command=lambda row=index: self.changer(row), variable=crochetFait,bg= self.color)
            cb.grid(row=row,column=2) #i=i permet d'enregistrer la valeur actuelle du i!!! Nice trick! :)
            
            #print(row, "    ", i)
            
         
            #pour les 5 jours de la semaine
            listeSemaine=[]
            for i in range(5):
                try:
                    dateSprint =  self.retournerUneDateSprint(str(self.lesCinqJours[i]), id_tache)
                    reqJourFait = dateSprint[0][0]         
                    reqJourPrevu = dateSprint[0][1]
                    texteDefaut = dateSprint[0][2]
           
                except:
                    reqJourFait = 0
                    reqJourPrevu =0    
                    texteDefaut = ""
                
                if (self.joursSemaineValides[i]):
                    state = NORMAL
                 
                else:
                    state = DISABLED
               
                column = 3 + i *3
                jourFait = IntVar()
                jourPrevu = IntVar()
                #jourEntry = IntVar()
                self.checkParDefaut(jourFait, reqJourFait)
                self.checkParDefaut(jourPrevu, reqJourPrevu)
                fait = Checkbutton(frame, state = state, variable=jourFait,bg= self.color)
                fait.grid(row=row,column=column)
                prevu = Checkbutton(frame, state = state, variable = jourPrevu,bg= self.color)
                prevu.grid(row=row,column=column+1)
                entry = Entry(frame,state = state)
                entry.insert(END,texteDefaut)
                entry.grid(row=row,column=column+2)
                
                listeSemaine.append([fait,prevu,entry,self.datePrevu, jourFait, jourPrevu])

          
            self.list.append([labelTache,crochetFait,listeSemaine,tache,id_tache])
            
            #changer l'etat des boutons au loadage
            if (reussi):
                self.changer(index)
      
                
          
    def dateEnFormatUtilisable(self,date):
        try:
            nouvelleDate = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except IndexError:
            nouvelleDate = datetime.date.today()
        return nouvelleDate
   
    def enregistrer(self):
        self.parent.enregistrer(self.list, self.id_utilisateur,self.id_sprint, self.joursSemaineValides, self.lesCinqJours)
     
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
         self.lesCinqJours = []
         self.joursSemaineValides= []
         if self.changementDeSemaine == False:
            self.datePrevu = None
         else:
            self.changementDeSemaine = False
         self.populer(self.frame)
             
    def nbColonnes(self):
        self.colonnes += 1
        return self.colonnes  
    
    def nbRangees(self):
        self.rangees +=1
        return self.rangees-1
    
    def retournerUneDateSprint(self,date, id_tache):
        return self.parent.retournerUneDateSprint(date, id_tache)
    
    def retournerLesTaches(self,id_sprint,id_utilisateur):
        return self.parent.retournerLesTaches(id_sprint,id_utilisateur)
    
    def retournerLeSprint(self,id_sprint):
        return self.parent.retournerLeSprint(id_sprint)
    
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
              
        else:
            self.insererNouvelleTache(self.id_utilisateur,self.id_sprint,saisie,0)  
            self.updaterVue()  
        #effacer les choses déjà écrites
        event.widget.delete(0, END)
        
    def insererNouvelleTache(self, id_utilisateur, id_sprint, tache, reussi):
        return self.parent.insererNouvelleTache(id_utilisateur, id_sprint, tache, reussi)
    
    def insererNouveauSprint(self,date_debut, date_fin, nom):
        self.parent.insererNouveauSprint(date_debut, date_fin, nom)
        
            
if __name__ == '__main__':
    v = Vue(None)
            
