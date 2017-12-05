#-*- coding: utf-8 -*-

from tkinter import *
from tkinter.filedialog import *
import sqlite3
import time
from _overlapped import NULL
from xmlrpc.client import ServerProxy
from sqlite3.test.userfunctions import AggregateTests
from tkinter import messagebox

#pour débugger plus facilement
import socket
from xmlrpc.client import ServerProxy
from subprocess import Popen




class Vue():
    def __init__(self, parent):
        self.parent=parent
        self.root=Tk() #Fenetre
        self.root.title("MANDAT")
        self.hauteurTotale=200
        self.largeurTotale=200
        self.hauteurMandat=200
        self.largeurMandat=200
        self.fenetre = Frame(master=self.root, width=self.largeurTotale, height=self.hauteurTotale, bg="steelblue")
        self.fenetre.pack()
        self.text = ""
        self.mot=""
        
        #listes de types et de natures
        self.types = ["Explicite", "Implicite", "Supplementaire"]
        self.natures = ["Objet", "Action", "Attribut"]
        
        #contiendra tous mes listbox
        self.matrix = []
        self.matrix.append([])
        self.matrix.append([])
        self.matrix.append([])
        
        #pour le bouton confirmer
        self.choixNatureFait = False
        self.choixTypeFait = False
                      
        self.ecranMandat()
        self.ecranCommande()
        self.ecranAnalyse()   
        self.barreTaches()
    
    def barreTaches(self):
        #menu deroulant

        self.menubar = Menu(self.root)
        self.menubar.add_command(label="Enregistrer", command= lambda: self.parent.modele.enregistrer(self.text))
        self.menubar.add_command(label="Charger un fichier", command= lambda: self.parent.modele.explorateurFichiers(self.text))
        self.root.config(menu=self.menubar)
        
    def choisirMot(self,event):
        start = self.text.index('@%s,%s wordstart' % (event.x, event.y))
        stop = self.text.index('@%s,%s wordend' % (event.x, event.y))
        self.mot = repr(self.text.get(start, stop))
        #pour enlever les guillemets au debut et a la fin du mot
        self.mot = mot[1:-1]
        return self.mot
      
    def dragging(self,event):
        #start = self.text.index('@%s,%s wordstart' % (event.x, event.y))
        #end = self.text.index('@%s,%s wordend' % (event.x, event.y)) 
        #start = self.text.index("sel.first")
        #end = self.text.index("sel.last")
        fonctionne = True
        try:
            self.mot = self.text.selection_get()
        except BaseException:
            fonctionne = False
            
        if fonctionne:
                
            self.mot = self.text.selection_get()
            self.tfExpression.delete(0,END)
            self.tfExpression.insert(0,self.mot)
            self.canCommande.create_window(400,30,window=self.tfExpression,width=600,height=20)
            '''
        # obtenir l'index du click
        index = self.text.index("@%s,%s" % (event.x, event.y))
        # objenir la caractere qui correspond au click
        char = (self.parent.vue.text.get(index))
        if (char != '\n'):
            tag_indices = list(self.text.tag_ranges("jaune"))
            #enlever le tag "jaune" qui se trouve dans l'index choisi
            #index2 = index+1 
            #self.text.tag_remove(str("jaune"),str(index),str(index+1))
             
            self.text.tag_add("jaune", "@%d,%d" % (event.x, event.y))   
            self.propagateTag(event)
            self.specialEffect()
            self.parent.modele.ajouter(self.frameMandat)
            mot = self.choisirMot(event)
            self.tfExpression.delete(0,END)
            self.tfExpression.insert(0,mot)           
            self.canCommande.create_window(400,30,window=self.tfExpression,width=600,height=20)
            '''
    
    def ecranMandat(self):
        self.frameMandat = Frame(self.fenetre, width = self.largeurMandat, height=self.hauteurMandat, bg="steelblue", relief=RAISED, padx=10, pady=10)
        self.frameMandat.pack()
        self.text = Text(self.frameMandat, width=100, height=20)
        #le texte initial est le texte pr�load� de la derniere enregistrement
        #texteInitial = self.texteInitial()
        texteInitial = self.parent.modele.loaderTexte()
        self.text.insert("%d.%d" %(0,1),texteInitial)
        #self.text.bind("<Button-1>",self.tagging)
        self.text.bind("<ButtonRelease-1>", self.dragging)
        self.text.pack()
           
    def ecranCommande(self):
        self.frameCommande=Frame(self.fenetre, width=self.largeurMandat, height=self.hauteurTotale/2, bg="steelblue", padx=10,pady=10)
        self.frameCommande.pack(fill=X)
        self.canCommande=Canvas(self.frameCommande, height=135, bg="light gray")
        self.canCommande.pack(fill=X)
        
        #Entree de l'expression
        self.tfExpression=Entry(self.canCommande, width=100)
        self.tfExpression.insert(0, "Cliquer sur un mot")
        self.canCommande.create_window(400,30,window=self.tfExpression,width=600,height=20)
        
        #Boutons de nature
        self.btnObjet=Button(self.frameCommande, text="Objet", width=30, command=lambda:self.choixNature(1))
        self.canCommande.create_window(150,70,window=self.btnObjet,width=110,height=30)
        self.btnAction=Button(self.frameCommande, text="Action", width=30, command=lambda:self.choixNature(2))
        self.canCommande.create_window(275,70,window=self.btnAction,width=110,height=30)
        self.btnAttribut=Button(self.frameCommande, text="Attribut", width=30, command=lambda:self.choixNature(3))
        self.canCommande.create_window(400,70,window=self.btnAttribut,width=110,height=30)
        
        #Boutons de type
        self.btnImplicite=Button(self.frameCommande, text="Implicite", width=30, bg="light blue", command=lambda:self.choixType(1))
        self.canCommande.create_window(150,110,window=self.btnImplicite,width=110,height=30)
        self.btnSupplementaire=Button(self.frameCommande, text="Explicite", width=30, bg="light blue", command=lambda:self.choixType(2))
        self.canCommande.create_window(275,110,window=self.btnSupplementaire,width=110,height=30)
        self.btnSupplementaire=Button(self.frameCommande, text="Supplementaire", width=30, bg="light blue", command=lambda:self.choixType(3))
        self.canCommande.create_window(400,110,window=self.btnSupplementaire,width=110,height=30)
        
    
        #deux labels pour identifier les expression
        self.labelChoixNature = Label(self.frameCommande, text="-----")
        self.canCommande.create_window(525,70,window=self.labelChoixNature,width=110,height=30)

        self.labelChoixType = Label(self.frameCommande, text="-----", bg="light blue")
        self.canCommande.create_window(525,110,window=self.labelChoixType,width=110,height=30)
    
        #bouton confirmer
        #self.btnConfirmer=Button(self.frameCommande, text="Confirmer", width=30, command=lambda:self.choixNature(3))
        self.btnConfirmer=Button(self.frameCommande, text="Confirmer", width=30, command=self.confirmer)
        self.canCommande.create_window(650,90,window=self.btnConfirmer,width=110,height=30)
    
    def confirmer(self):
        if (self.choixNatureFait and self.choixTypeFait):
            self.parent.modele.uneExpression.contenu=self.mot    
            self.parent.modele.confirmer()
            self.resetVue()
            self.updateExpressions()
           
        else:
            # message avertissement
            messagebox.showinfo("SVP", "Informations manquantes")
            

        
    def choixNature(self,choix):
        self.choixNatureFait = True #utiliser pour la confirmation plus tard
        if choix==1:
            self.parent.modele.uneExpression.nature="Objet"
            self.labelChoixNature.config(text="Objet")
            print("Envoie de la nature Objet dans l'expression: "+self.parent.modele.uneExpression.nature)
        elif choix==2:
            self.labelChoixNature.config(text="Action")
            self.parent.modele.uneExpression.nature="Action"
        #elif choix==3:
            #self.labelChoixNature.config(text="Attribut")
            #self.parent.modele.uneExpression.nature="Attribut"
        
        self.parent.modele.uneExpression.contenu=self.mot
        
        if self.mot==self.tfExpression.get():
            self.parent.modele.insertionSQL()
            #self.afficheListBox()
            
            
    
    def choixType(self,choix):
        self.choixTypeFait = True #utiliser pour la confirmation plus tard
        #if self.parent.modele.uneExpression.nature!=NULL: 
        if choix==1:
            self.labelChoixType.config(text="Implicite")
            self.parent.modele.uneExpression.type="Implicite"
        elif choix==2:
            self.labelChoixType.config(text="Explicite")
            self.parent.modele.uneExpression.type="Explicite"
        elif choix==3:
            self.labelChoixType.config(text="Supplémentaire")
            self.parent.modele.uneExpression.type="Supplementaire"
        
        self.parent.modele.uneExpression.contenu=self.mot
        #self.parent.modele.updateExpressions()
        self.afficheListBox()
          
        #else:
        #    print("Entrez une nature de mot ") #Remplcer par une fenetre avertissement ou autre 
        #appel de la fonction SQL pour enregistrer dans la BD
        
        #self.parent.modele.insertionSQL(self.parent.modele.uneExpression)         
        #self.parent.modele.insertionSQL(self.parent.modele.uneExpression) 
        
    def afficheListBox(self):
        for item in self.parent.modele.listeExpObj:
            self.listExpObj.append(item)
        for item in self.parent.modele.listeExpAct:
            self.listExpAct.append(item)
        for item in self.parent.modele.listeExpAtt:
            self.listExpAtt.append(item)
        for item in self.parent.modele.listeImpObj:
            self.listImpObj.append(item)
        for item in self.parent.modele.listeImpAct:
            self.listImpAct.append(item)
        for item in self.parent.modele.listeImpAtt:
            self.listImpAtt.append(item)
        for item in self.parent.modele.listeSupObj:
            self.listSupObj.append(item)
        for item in self.parent.modele.listeSupAct:
            self.listSupAct.append(item)
        for item in self.parent.modele.listeSupAtt:
            self.listSupAtt.append(item)
   
    def ecranAnalyse(self):
        self.frameAnalyse=Frame(self.fenetre, width=self.largeurMandat, height=self.hauteurTotale/2, bg="steelblue", padx=10,pady=10)
        self.frameAnalyse.pack(fill=X)
        self.canAnalyse=Canvas(self.frameAnalyse, height=500, bg="light gray")
        self.canAnalyse=Canvas(self.frameAnalyse, height=450, bg="light gray")
        self.canAnalyse.pack(fill=X)
        

        #1ere ligne grille
        self.labelVide=Label(self.frameAnalyse, text="", width=100, height=50, bg="white", relief=RAISED )
        self.canAnalyse.create_window(75,40,window=self.labelVide, width=100, height=40)
        self.labelObjet=Label(self.frameAnalyse, text="Objet", width=220, height=50, bg="white",relief=RAISED )
        self.canAnalyse.create_window(235,40,window=self.labelObjet, width=220, height=40)
        self.labelAction=Label(self.frameAnalyse, text="Action", width=220, height=50, bg="white",relief=RAISED )
        self.canAnalyse.create_window(455,40,window=self.labelAction, width=220, height=40)
        self.labelAttribut=Label(self.frameAnalyse, text="Attribut", width=220, height=50, bg="white",relief=RAISED )
        self.canAnalyse.create_window(675,40,window=self.labelAttribut, width=220, height=40)
        
        #2e ligne grille
        self.labelExplicite=Label(self.frameAnalyse, text="Explicite", width=100, height=80, bg="white", relief=RAISED )
        self.canAnalyse.create_window(75,120,window=self.labelExplicite, width=100, height=120)
        self.listExpObj=Listbox(self.frameAnalyse,width=220,height=120)
        self.canAnalyse.create_window(235,120,window=self.listExpObj, width=220, height=120)
        self.listExpAct=Listbox(self.frameAnalyse,width=220,height=120)
        self.canAnalyse.create_window(455,120,window=self.listExpAct, width=220, height=120)
        self.listExpAtt=Listbox(self.frameAnalyse,width=220,height=120)
        self.canAnalyse.create_window(675,120,window=self.listExpAtt, width=220, height=120)
        
        #3e ligne grille
        self.labelImplicite=Label(self.frameAnalyse, text="Implicite", width=100, height=80, bg="white", relief=RAISED )
        self.canAnalyse.create_window(75,240,window=self.labelImplicite, width=100, height=120)
        self.listImpObj=Listbox(self.frameAnalyse,width=220,height=120)
        self.canAnalyse.create_window(235,240,window=self.listImpObj, width=220, height=120)
        self.listImpAct=Listbox(self.frameAnalyse,width=220,height=120)
        self.canAnalyse.create_window(455,240,window=self.listImpAct, width=220, height=120)
        self.listImpAtt=Listbox(self.frameAnalyse,width=220,height=120)
        self.canAnalyse.create_window(675,240,window=self.listImpAtt, width=220, height=120)
        
        #4e ligne grille
        self.labelSupplementaire=Label(self.frameAnalyse, text="Supplementaire", width=100, height=80, bg="white", relief=RAISED )
        self.canAnalyse.create_window(75,360,window=self.labelSupplementaire, width=100, height=120)
        self.listSupObj=Listbox(self.frameAnalyse,width=220,height=120)
        self.canAnalyse.create_window(235,360,window=self.listSupObj, width=220, height=120)
        self.listSupAct=Listbox(self.frameAnalyse,width=220,height=120)
        self.canAnalyse.create_window(455,360,window=self.listSupAct, width=220, height=120)
        self.listSupAtt=Listbox(self.frameAnalyse,width=220,height=120)
        self.canAnalyse.create_window(675,360,window=self.listSupAtt, width=220, height=120)
        
        
        
        #mettre dans une matrice, pour faciliter le parcours des listbox
        self.matrix[0].append(self.listExpObj)
        self.matrix[0].append(self.listExpAct)
        self.matrix[0].append(self.listExpAtt)
        
        self.matrix[1].append(self.listImpObj)
        self.matrix[1].append(self.listImpAct)
        self.matrix[1].append(self.listImpAtt)
        
        self.matrix[2].append(self.listSupObj)
        self.matrix[2].append(self.listSupAct)
        self.matrix[2].append(self.listSupAtt)
        
        
        self.loaderLesListe()
         
    def loaderLesListe(self):
        
         
        #for i in self.parent.modele.selectionLesExpressions():
        #    self.matrix[0][0].insert(END,i[0])
        for i in range(3):
            for j in range(3):
                    self.loaderUneListe(self.matrix[i][j], self.types[i],self.natures[j])   
            
    def loaderUneListe(self,liste, type,nature):
        for i in self.parent.modele.selectionLesExpressions(type, nature):
            liste.insert(END,i[0])
        pass
        
    def resetVue(self):
        #enlever les elements entres (reset)
        self.labelChoixNature.config(text = "-----")
        self.labelChoixType.config(text = "-----")   
        
        #reset les variables
        self.choixNatureFait = False
        self.choixTypeFait = False    

    def texteInitial(self):
        conn = sqlite3.connect('donnees.db')
        c = conn.cursor()
        
        c.execute('SELECT * FROM mandats')
        texteMandat = c.fetchone()[0]
               
        conn.close()
        return texteMandat
        
              
    def tagging(self,event):
        # obtenir l'index du click
        index = self.text.index("@%s,%s" % (event.x, event.y))
        # objenir la caractere qui correspond au click
        char = (self.parent.vue.text.get(index))
        if (char != '\n'):
            tag_indices = list(self.text.tag_ranges("jaune"))
            #enlever le tag "jaune" qui se trouve dans l'index choisi
            #index2 = index+1 
            #self.text.tag_remove(str("jaune"),str(index),str(index+1))
             
            self.text.tag_add("jaune", "@%d,%d" % (event.x, event.y))   
            self.propagateTag(event)
            self.specialEffect()
            self.parent.modele.ajouter(self.frameMandat)
            self.mot = self.choisirMot(event)
            self.tfExpression.delete(0,END)
            self.tfExpression.insert(0,self.mot)
            
            self.canCommande.create_window(400,30,window=self.tfExpression,width=600,height=20)
        
    def propagateTag(self, event):
        
        start = self.text.index('@%s,%s wordstart' % (event.x, event.y))
        end = self.text.index('@%s,%s wordend' % (event.x, event.y))
        self.text.tag_add("jaune",start, end)    
  
    def specialEffect(self):
        self.text.tag_config('jaune', background='yellow')
  
    def updateExpressions(self):
        self.parent.modele.updateExpressions()

class Expression():
    def __init__(self):
        self.id=NULL
        self.contenu=NULL
        #self.type="Explicite"
        self.type= NULL
        self.nature=NULL
        self.emplacement=NULL
    """    
    def reinitier(self):
        self.id=NULL
        self.contenu=NULL
        #self.type="Explicite"
        self.type= NULL
        self.nature=NULL
        self.emplacement=NULL
        """
class Modele():
    def __init__(self, parent):
        self.parent=parent
        #Connection à la bd temporaire
        #database = sqlite3.connect('BDD.sqlite')
        #Création du curseur de la bd temporaire
        #self.curseur = database.cursor()
        self.uneExpression=Expression()
        #self.tupleBD=self.lectureSQL()
        self.listeExpObj=[]
        self.listeExpAct=[]
        self.listeExpAtt=[]
        self.listeImpObj=[]
        self.listeImpAct=[]
        self.listeImpAtt=[]
        self.listeSupObj=[]
        self.listeSupAct=[]
        self.listeSupAtt=[]
        
    
    def ajoutListe(self):
        tupleBD = self.tupleBD
        for i in range(0,len(tupleBD)): 
            if tupleBD[i][1]=="Explicite":
                if tupleBD[i][4]=="Objet":
                    self.listeExpObj.append(tupleBD[i][3])
                if tupleBD[i][4]=="Action":
                    self.listeExpAct.append(tupleBD[i][3])
                if tupleBD[i][4]=="Attribut":
                    self.listeExpAtt.append(tupleBD[i][3])
                
            if tupleBD[i][1]=="Implicite":
                if tupleBD[i][4]=="Objet":
                    self.listeImpObj.append(tupleBD[i][3])
                if tupleBD[i][4]=="Action":
                    self.listeImpAct.append(tupleBD[i][3])
                if tupleBD[i][4]=="Attribut":
                    self.listeImpAtt.append(tupleBD[i][3])
                
            if tupleBD[i][1]=="Supplementaire":
                if tupleBD[i][4]=="Objet":
                    self.listeSupObj.append(tupleBD[i][3])
                if tupleBD[i][4]=="Action":
                    self.listeSupAct.append(tupleBD[i][3])
                if tupleBD[i][4]=="Attribut":
                    self.listeSupAtt.append(tupleBD[i][3])
        
    """def ajouter(self,canva):
        self.mots = []
        lesTags = self.parent.vue.text.tag_ranges("jaune")
        temp = ""
        #data = self.text.get("1.0",END)
        avant = 0   
        ranges = self.parent.vue.text.tag_ranges("jaune")        
        for i in range(0, len(ranges), 2):
            start = ranges[i]
            stop = ranges[i+1]
            self.mots.append(( (repr(self.parent.vue.text.get(start, stop))) ))"""
    
    def ajouterNouveauTexte(self,texteMandat):
        chaine = "'" + str(self.parent.idProjet) + "','" + str(texteMandat) + "'"
        self.parent.serveur.insertionSQL("Textes",chaine)
        
    def confirmer(self):
        self.insererExpression()
        
    def insererExpression(self):  
        chaine = "'" + str(self.parent.idProjet) + "','" +str(self.uneExpression.contenu) + "','"  + str(self.uneExpression.type)  + "','" +str(self.uneExpression.nature)  + "','" +str(self.uneExpression.emplacement) + "'"
        self.parent.serveur.insertionSQL("Mandats",chaine)  
        #la valeur dans la bd de l'emplacement est de 0 si emplacement est NULL
        self.uneExpression.reinitier() #effacer les valeurs de l'expression pour mettre des nouvelles
        
    def updateExpressions(self):  
        #self.tupleBD=self.parent.modele.selectionLesExpressions()
        self.requeteExpressions = 0
        self.requeteExpressions = self.selectionLesExpressions()
        #self.parent.vue.text.insert(END,"allo")
        #self.ajoutListe()
        #self.uneExpression=Expression()
       
     
    def enregistrer(self,texteMandat):
        #texteMandat = texteMandat.get(1.0,'end-1c')
        #supprimer le vieux texte de la BD
        self.supprimerAncienTexte()
        self.ajouterNouveauTexte(texteMandat)
   
 
            
    def explorateurFichiers(self,text):
        #ouvrir un fichier
        # filename = askopenfilename(title="Ouvrir votre document",filetypes=[('txt files','.txt'),('all files','.*')])
        fonctionne = True
        filename = askopenfilename(title="Ouvrir votre document",filetypes=[('txt files','.txt')])
        try:
            fichier = open(filename, "r")
        except FileNotFoundError:
            fonctionne = False
            print("Aucun fichier choisi!")
        if fonctionne:  
            content = fichier.read()
            fichier.close()
            text.insert("%d.%d" %(1,0),content)

    def insertionSQL(self):  
        '''sql = "INSERT INTO Mots (ROWID, TYPES, EMPLACEMENT, CONTENU, NATURE) VALUES (" + str(self.uneExpression.id)+ "," +str(self.uneExpression.type) +"," + str(self.uneExpression.emplacement) +"," + str(self.uneExpression.contenu) +"," + str(self.uneExpression.nature) + ");"
        print(sql)
        print("Envoie a la BD")
        '''
        
        '''self.curseur.execute("INSERT INTO Mots VALUES(?,?,?,?,?)", (self.uneExpression.id,self.uneExpression.type,self.uneExpression.emplacement,self.uneExpression.contenu,self.uneExpression.nature,))
        print("Envoi avec succes")'''
        
        self.parent.serveur.insertionSQL(self,"Mandats",valeurs)
        
        self.database.commit()
        
    
    def loaderTexte(self):
        requete = self.parent.serveur.selectionSQL("Textes", "id_Projet, texte")
        
        try: 
            for element in requete:
                if str(element[0]) == str(self.parent.idProjet):
                    texte = element[1]
                    break
            return texte
        except NameError:
            print("erreur, rien a loader de la BD")
            return "Bienvenue au module Mandat" #pour le texte par defaut
        
    def selectionLesExpressions(self,type,nature):
        #requete = self.parent.serveur.selectionSQL("Mandats", "contenu, type, nature")
        #expressions = []
        '''
        for element in requete:
            if str(element[1]) == str(self.parent.idProjet):
                expressions.append(element)
        '''
        #nomTable = "Mandats"
        #champs = "*"
        #where = ["id_Projet", "type", "nature"]
        #valeur = [str(self.parent.idProjet), "Explicite", "Objet"]
        nomTable = "Mandats"
        champs = "contenu"
        where = ["type","nature"]
        valeur = [type,nature]

        
        #requete = self.parent.serveur.selectionSQL3("Mandats", "contenu, type, nature", "id_Projet", str(self.parent.idProjet))
        requete = self.parent.serveur.selDonneesWHERE(nomTable,champs,where,valeur)
        return requete
    
    def supprimerAncienTexte(self):
        self.parent.serveur.delete("Textes","id_Projet", str(self.parent.idProjet))


class Controleur():
    def __init__(self):
        
        #vraie version
        self.saasIP=sys.argv[1]
        self.utilisateur=sys.argv[2]
        self.organisation=sys.argv[3]
        self.idProjet=sys.argv[4]
        self.clientIP=sys.argv[5]
        self.adresseServeur="http://"+self.saasIP+":9999"
        
        
        
        
        
        self.modele=Modele(self)
        self.serveur = self.connectionServeur()

        self.vue=Vue(self)
        self.vue.root.mainloop()
        '''
        
        self.saasIP=socket.gethostbyname(socket.gethostname())
        self.adresseServeur="http://"+self.saasIP+":9999"
        self.idProjet= 1
        self.serveur = self.connectionServeur()
        self.modele=Modele(self)
        self.vue=Vue(self)
        self.vue.root.mainloop()
        '''
    def connectionServeur(self):
        #ad="http://"+self.saasIP+":9998"
        print("Connection au serveur BD...")
        serveur=ServerProxy(self.adresseServeur)
        return serveur
        
    
                
        
        
if __name__ == '__main__':
    c=Controleur()