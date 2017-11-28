from tkinter import *

'''class Controleur():
    def __init__(self):
        self.vue = Vue(self)
        self.unReprend=False
        self.vue.root.mainloop()
        print("controleur")
    
class Vue():
    def __init__(self, pControleur):
        self.controleur = pControleur
        self.largeur = 800
        self.hauteur = 600
        self.root = Tk()
        self.fenetre = Frame(self.root, width = self.largeur, height = self.hauteur)
        self.fenetre.pack()
        self.listeCas=[]
        self.listeEtat=[]
        self.dejaOuvert=False
        self.indiceCasModifier=0
        self.menuInitial()
        self.x=0
        self.y=0
        self.x2=0
        self.y2=0
        self.cercle=False;
        self.rect=False;
      

    
    def menuInitial(self):
        self.caneva = Canvas(self.fenetre, width = self.largeur-200, height=self.hauteur, bg="white")
        self.caneva.pack(side=LEFT)
        self.cadreBtn = Canvas(self.fenetre, width = 200, height=self.hauteur, bg="white")
        self.cadreBtn.pack(side=LEFT)
        
        self.btnRectangle=Button(self.cadreBtn,text="Rectangle",width=30,command=self.creeRectangle())
        self.cadreBtn.create_window(100,100,window=self.btnRectangle,width=150,height=30)
    
        self.btnCercle=Button(self.cadreBtn,text="Cercle",width=30,command=self.creeCercle())
        self.cadreBtn.create_window(100,250,window=self.btnCercle,width=150,height=30)
        
        self.bntTexte=Button(self.cadreBtn,text="Texte",width=30)#
        self.cadreBtn.create_window(100,200,window=self.bntTexte,width=150,height=30)
        
        self.bntFleche=Button(self.cadreBtn,text="Fleche",width=30)
        self.cadreBtn.create_window(100,300,window=self.bntFleche,width=150,height=30)

        self.btnRectangle=Button(self.cadreBtn,text="Commit",width=30)
        self.cadreBtn.create_window(100,500,window=self.btnRectangle,width=150,height=30)
    
        self.btnCercle=Button(self.cadreBtn,text="Supprimer",width=30)
        
        self.cadreBtn.create_window(100,550,window=self.btnCercle,width=150,height=30)
        self.caneva.bind('<B1-Motion>', self.bouge)
        self.caneva.pack(padx =5, pady =5)
        
        self.caneva.bind('<B1-Motion>', self.bouge)
        self.caneva.pack(padx =5, pady =5)
        
        self.caneva.bind('<Button-1>', self.clic)
        self.caneva.pack(padx =5, pady =5)
       
        self.caneva.bind('ButtonRelease-1', self.release)
        self.caneva.pack(padx =5, pady =5)
    
    def bouge(self,event):
        self.x2 = event.x
        self.y2 = event.y
        print(self.x2,self.y2)
        self.dessinerTempo()
    
    def clic(self,event):
        self.x = event.x
        self.y = event.y
        print(self.x,self.y)

    def release(self):
        self.x2 = event.x
        self.y2 = event.y
        self.dessiner()
    
    def creeCercle(self):
        self.cercle=True;
   
    def creeRectangle(self):
        self.rect=True
                    
    def detruitTempo(self):
       pass

        
    def dessinerTempo(self):
        if(self.cercle):
            self.caneva.create_oval(self.x,self.y,self.x+self.x,self.y+self.x,tags="Forme")
        
        self.caneva.create_rectangle(self.x,self.y,self.x2,self.y2,tags="Forme")
        self.caneva.delete("Forme")
        
        
    def callback(event):
        print ("clicked at", event.x, event.y)'''
        
        
class Controleur():
    def __init__(self):
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.vue.root.mainloop()

class Vue():
    def __init__(self, pControleur):
        self.controleur = pControleur
        self.largeur = 800
        self.hauteur = 600
        self.root = Tk()
        self.cadreMaquette = Frame(self.root, width = self.largeur, height = self.hauteur)
        self.cadreMaquette.pack()
        self.canevas = Canvas(self.cadreMaquette, width = self.largeur, height = self.hauteur)
        self.canevas.pack(side = LEFT)
        self.cadreOutil= Frame(self.cadreMaquette, width = self.largeur - 600, height = self.hauteur, bg = "grey")
        self.cadreOutil.pack(side = LEFT)

        
    def afficherCaneva(self):
        self.canevas.delete(ALL)
        for i in self.controleur.modele.formes:
            if (self.controleur.modele.formes.nom == "Rectangle"):
                self.canevas.create_rectangle(i.x1,i.y1,i.x+i.taille,i.y+i.taille, fill="black")
            if (self.controleur.modele.formes.nom == "Cercle"):
                self.canevas.create_oval()(i.x1,i.y1,i.x+i.taille,i.y+i.taille, fill="black")
            if (self.controleur.modele.formes.nom == "Fleche"):
                self.canevas.create_line()()(i.x1,i.y1,i.x+i.taille,i.y+i.taille, fill="black")
            if (self.controleur.modele.formes.nom == "Texte"):
                self.canevas.create_text()()()(i.x1,i.y1,i.x+i.taille,i.y+i.taille, fill="black")
                
class Modele():
    def __init__(self, pControleur):
        self.controleur = pControleur
        self.formes = [ ]
        

class Formes():
    def __init__(self, pModele, pNom):
        self.modele=pModele
        self.nom = pNom
        self.x1
        self.y1
        self.x2
        self.y2
        self.text
                        
if __name__ == '__main__':
    c = Controleur()