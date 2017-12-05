from tkinter import *
from xmlrpc.client import ServerProxy
import sqlite3

class Controleur():
    def __init__(self):
        self.modele = Modele(self)
        self.idProjet = int(sys.argv[4])
        self.saasIP = sys.argv[1]
        self.connexionSaas()
        self.chargerFormes()
        self.vue = Vue(self)
        self.unReprend=False
        self.vue.root.mainloop()
        
    def connexionSaas(self):
        ad="http://"+self.saasIP+":9999"
        self.serveur=ServerProxy(ad,allow_none = 1)
    
    
    def chargerFormes(self):
        for i in self.serveur.selectionSQL3("Formes","id, x1, y1, x2, y2, texte, nom","id_Projet",self.idProjet):
            nom = i[6]
            forme = Formes(i[1],i[2],i[3],i[4],nom,i[0])
            self.modele.formesTempo.append(forme)
            print(i[0])
        
    
    def commit(self):
        for i in self.modele.formes:
            self.serveur.insertionSQL("Formes", "'"+str(self.idProjet)+"', '"+str(i.x1)+"', '"+str(i.y1)+"', '"+str(i.x2)+"', '"+str(i.y2)+"', '"+i.text+"', '"+i.nom+"'")

        for i in self.modele.formes:
            self.modele.formes.remove(i)
    
class Vue():
    def __init__(self, pControleur):
        self.controleur = pControleur
        self.largeur = 800
        self.hauteur = 600
        self.root = Tk()
        self.dejaOuvert=False
        self.indiceCasModifier=0
        self.menuInitial()
        self.x1=0
        self.y1=0
        self.x2=0
        self.y2=0
        self.cercle=False;
        self.rect=False;
        self.choix = ""
        self.afficherCaneva()
        self.maSelection = False
        self.formeTempo = None
        
    def afficherCaneva(self):
        for i in self.controleur.modele.formesTempo:
            if (i.nom == "Rectangle"):
                self.caneva.create_rectangle(i.x1,i.y1,i.x2,i.y2, tags = ("forme", i.text))
                #self.caneva.create_rectangle(i.x1,i.y1,i.x1+i.taille,i.y1+i.taille, fill="black")
            
            elif (i.nom  == "Cercle"):
                self.caneva.create_oval(i.x1,i.y1,i.x2,i.y2, tags = ("forme", i.text))
                #self.caneva.create_oval(i.x1,i.y1,i.x1+i.taille,i.y1+i.taille, fill="black")
            
            elif (i.nom  == "Fleche"):
                #self.caneva.create_line()()(i.x1,i.y1,i.x1+i.taille,i.y1+i.taille, fill="black")
                self.caneva.create_line(i.x1,i.y1,i.x2,i.y2, arrow="last", tags = ("forme", i.text))
        
            elif (i.nom  == "Texte"):
                entry = Entry(self.caneva,bd=0,font=("Purisa",15))       
                entry.insert(0,i.text)
                entry.place(x= i.x1, y= i.y1)
        
    def menuInitial(self):
        self.fenetre = Frame(self.root, width = 800, height = 600)
        self.fenetre.pack()
        self.menuTop = Canvas(self.fenetre, width = 800, height = 100)
        self.menuTop.pack(side=TOP)
        self.fenetreMid = Frame(self.fenetre, width = 800, height = 500)
        self.fenetreMid.pack(side=TOP)
        self.caneva = Canvas(self.fenetreMid, width = self.largeur-200, height=self.hauteur, bg="white")
        self.caneva.pack(side=LEFT)
        self.cadreBtn = Canvas(self.fenetreMid, width = 200, height=self.hauteur, bg="white")
        self.cadreBtn.pack(side=LEFT)
        
        self.btnRectangle=Button(self.cadreBtn,text="Rectangle",width=30,command=self.creeRectangle)
        self.cadreBtn.create_window(100,100,window=self.btnRectangle,width=150,height=30)
    
        self.btnCercle=Button(self.cadreBtn,text="Cercle",width=30,command=self.creeCercle)
        self.cadreBtn.create_window(100,250,window=self.btnCercle,width=150,height=30)
        
        self.bntTexte=Button(self.cadreBtn,text="Texte",width=30, command=self.creeTexte)
        self.cadreBtn.create_window(100,200,window=self.bntTexte,width=150,height=30)
        
        self.bntFleche=Button(self.cadreBtn,text="Fleche",width=30, command = self.creeFleche)
        self.cadreBtn.create_window(100,300,window=self.bntFleche,width=150,height=30)
        
        self.btnSelection=Button(self.cadreBtn,text="Selection",width=30, command = self.selection)
        self.cadreBtn.create_window(300,350,window=self.btnSelection,width=150,height=30)

        self.btnCommit=Button(self.menuTop,text="Commit",width=30, command = self.commit)
        self.menuTop.create_window(400,20,window=self.btnCommit,width=100,height=30)
    
        self.btnSuppr=Button(self.menuTop,text="Supprimer",width=30)
        self.menuTop.create_window(400,80,window=self.btnSuppr,width=100,height=30)
        
        self.e = Entry(bg="white")
        self.menuTop.create_window(100,50,window=self.e,width=50,height=30)
        
        self.caneva.bind('<B1-Motion>', self.bouge)
        self.caneva.pack(padx =5, pady =5)
        
        self.caneva.bind('<Button-1>', self.clic)
        self.caneva.pack(padx =5, pady =5)
       
        self.caneva.bind('<ButtonRelease-1>', self.release)
        self.caneva.pack(padx =5, pady =5)
        
        #formes temporaires
        self.caneva.create_rectangle(0,0,0,0,tag="tempoRectangle")
        self.caneva.create_oval(0,0,0,0,tag="tempoCercle")
        self.caneva.create_line(0,0, 0,0, tags=("tempoFleche"), arrow="last")
        self.entryTemp = Entry(self.caneva,bd=0,font=("Purisa",15))
    
        #les bindings pour faire fonctionner le entryTemp
        self.entryTemp.bind('<Return>',lambda d: self.deselectionner())
        #self.caneva.tag_bind("editable","<Return>", self.deselectionner)
    
    
    def deselectionner(self):
        self.caneva.focus_force()
        #self.caneva.delete("highlight")
        #self.caneva.select_clear()
        if (self.choix == "ModeEcriture"):
            forme = Formes(self.x1,self.y1,None,None,"Texte", self.entryTemp.get()) #la position de la forme n'a que une pair de x et de y
            self.controleur.modele.formesTempo.append(forme)
            self.afficherCaneva()   
            #effacer le contenu de l'entry temporaire
            self.entryTemp.delete(0,END)
    
    def bouge(self,event):
        if (self.caneva.gettags(CURRENT)):
            t = self.caneva.gettags(CURRENT)
            if self.maSelection == False:
                self.formeTempo = None
                for i in self.controleur.modele.formesTempo:
                    if i.text == t[1]:
                        self.formeTempo = i
            self.formeTempo.x1 = event.x
            self.formeTempo.y1 = event.y
            self.dessinerTempo()
        else:
            self.x2 = event.x
            self.y2 = event.y
            self.dessinerTempo()
            
    
    def clic(self,event):
        if (self.choix == "Texte"):
            #entry = Entry(self.caneva,bd=0,font=("Purisa",15))
            self.entryTemp.place(x= event.x, y= event.y)
            self.entryTemp.focus_force() #forcer le focus, l'usager va ecrire quelque chose dedans
            self.choix = "ModeEcriture" #l'utilisateur doit rechoisir une autre option
        elif (self.choix == "Selection" and self.caneva.gettags(CURRENT)):
            self.maSelection = True
        else :
            self.x1 = event.x
            self.y1 = event.y
        

    def release(self,event):
        if self.choix != "Texte":
            forme = Formes(self.x1,self.y1,event.x,event.y,self.choix)
            self.controleur.modele.formesTempo.append(forme)
            self.controleur.modele.formes.append(forme)
            self.afficherCaneva()
            if self.maSelection:
                self.maSelection = False
            
    def commit(self):
        self.controleur.commit()
            
    
    def creeTexte(self):
        self.choix = "Texte"
    
    def creeFleche(self):
        self.choix = "Fleche"
    
    def creeCercle(self):
        self.choix = "Cercle"
   
    def creeRectangle(self):
        self.choix = "Rectangle"
        
    def detruitTempo(self):
       pass

    def selection(self):
        self.choix = "Selection"
        
    def dessinerTempo(self):
        if(self.choix == "Cercle"):
            self.caneva.coords("tempoCercle",self.x1,self.y1,self.x2,self.y2)
        elif (self.choix == "Rectangle"):
            self.caneva.coords("tempoRectangle",self.x1,self.y1,self.x2,self.y2)
        elif (self.choix == "Fleche"):
            self.caneva.coords("tempoFleche",self.x1,self.y1,self.x2,self.y2)
        
        
        
class Modele():
    def __init__(self, pControleur):
        self.controleur = pControleur
        self.formesTempo = [ ]
        self.formes = [ ]    



class Formes():
    def __init__(self, x1,y1,x2,y2, pNom, pText = "i"):
        self.nom = pNom
        self.x1 = x1
        self.y1 = y1
        self.x2 =x2
        self.y2 =y2
        self.text = pText
          
if __name__ == '__main__':
    c = Controleur()
