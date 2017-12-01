from tkinter import *
from xmlrpc.client import ServerProxy

class Formes():
    def __init__(self, x1,y1,x2,y2, pNom, pText = "i"):
        #self.modele=pModele
        self.nom = pNom
        self.x1 = x1
        self.y1 = y1
        self.x2 =x2
        self.y2 =y2
        self.text = pText

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
        print("controleur")
    
    def connexionSaas(self):
        ad="http://"+self.saasIP+":9999"
        print("Connection au serveur Saas en cours...")
        self.serveur=ServerProxy(ad,allow_none = 1)
    
    
    def chargerFormes(self):
        '''for i in self.serveur.selectionSQL1("Formes",
                                            "'x1', 'y1', 'x2', 'y2', 'texte', 'nom'",
                                            "id_Projet",
                                            "'"+str(self.idProjet)+"'"):
            print(i.x1)
            self.modele.formesTempo.append(forme)'''
        pass
    
    def commit(self):
        for i in self.modele.formes:
            self.serveur.insertionSQL("Formes", "'"+str(self.idProjet)+"', '"+str(i.x1)+"', '"+str(i.y1)+"', '"+str(i.x2)+"', '"+str(i.y2)+"', '"+i.text+"', '"+i.nom+"'")

        
        for i in self.modele.formes:
            self.modele.formes.remove(i)
            
        for i in self.modele.formes:
            print(i)
    
class Vue():
    def __init__(self, pControleur):
        self.controleur = pControleur
        self.largeur = 800
        self.hauteur = 600
        self.root = Tk()
        self.fenetre = Frame(self.root, width = self.largeur, height = self.hauteur)
        self.fenetre.pack()
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
        self.formeTemp = 0
        self.afficherCaneva()
        
    def afficherCaneva(self):
        #self.caneva.delete(ALL)
        for i in self.controleur.modele.formesTempo:
            if (i.nom == "Rectangle"):
                print("Dessine")
                self.caneva.create_rectangle(i.x1,i.y1,i.x2,i.y2)
                #self.caneva.create_rectangle(i.x1,i.y1,i.x1+i.taille,i.y1+i.taille, fill="black")
            
            elif (i.nom  == "Cercle"):
                self.caneva.create_oval(i.x1,i.y1,i.x2,i.y2)
                #self.caneva.create_oval(i.x1,i.y1,i.x1+i.taille,i.y1+i.taille, fill="black")
            
            elif (i.nom  == "Fleche"):
                #self.caneva.create_line()()(i.x1,i.y1,i.x1+i.taille,i.y1+i.taille, fill="black")
                self.caneva.create_line(i.x1,i.y1,i.x2,i.y2, arrow="last")
        
            elif (i.nom  == "Texte"):
                print("ecriture clone")
                entry = Entry(self.caneva,bd=0,font=("Purisa",15))       
                entry.insert(0,i.text)
                entry.place(x= i.x1, y= i.y1)
                #self.caneva.create_text()()()(i.x1,i.y1,i.x1+i.taille,i.y1+i.taille, fill="black")
        #self.root.after(10, self.afficherCaneva)
        
    def menuInitial(self):
        self.caneva = Canvas(self.fenetre, width = self.largeur-200, height=self.hauteur, bg="white")
        self.caneva.pack(side=LEFT)
        self.cadreBtn = Canvas(self.fenetre, width = 200, height=self.hauteur, bg="white")
        self.cadreBtn.pack(side=LEFT)
        
        self.btnRectangle=Button(self.cadreBtn,text="Rectangle",width=30,command=self.creeRectangle)
        self.cadreBtn.create_window(100,100,window=self.btnRectangle,width=150,height=30)
    
        self.btnCercle=Button(self.cadreBtn,text="Cercle",width=30,command=self.creeCercle)
        self.cadreBtn.create_window(100,250,window=self.btnCercle,width=150,height=30)
        
        self.bntTexte=Button(self.cadreBtn,text="Texte",width=30, command=self.creeTexte)
        self.cadreBtn.create_window(100,200,window=self.bntTexte,width=150,height=30)
        
        self.bntFleche=Button(self.cadreBtn,text="Fleche",width=30, command = self.creeFleche)
        self.cadreBtn.create_window(100,300,window=self.bntFleche,width=150,height=30)

        self.btnRectangle=Button(self.cadreBtn,text="Commit",width=30, command = self.commit)
        self.cadreBtn.create_window(100,500,window=self.btnRectangle,width=150,height=30)
    
        self.btnSuppr=Button(self.cadreBtn,text="Supprimer",width=30)
        
        self.cadreBtn.create_window(100,550,window=self.btnSuppr,width=150,height=30)
        
        self.caneva.bind('<B1-Motion>', self.bouge)
        self.caneva.pack(padx =5, pady =5)
        
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
        self.x2 = event.x
        self.y2 = event.y
        #print(self.x2,self.y2)
        self.dessinerTempo()
    
    def clic(self,event):
        if (self.choix != "ModeEcriture"):
            self.x1 = event.x
            self.y1 = event.y
        if (self.choix == "Texte"):
            #entry = Entry(self.caneva,bd=0,font=("Purisa",15))
            self.entryTemp.place(x= event.x, y= event.y)
            self.entryTemp.focus_force() #forcer le focus, l'usager va ecrire quelque chose dedans
            
            print("en train d'ecrire")
            self.choix = "ModeEcriture" #l'utilisateur doit rechoisir une autre option
        #print(self.x,self.y)

    def release(self,event):
        forme = None
        if self.choix != "Texte":
            forme = Formes(self.x1,self.y1,event.x,event.y,self.choix)
            print(forme.nom)
            forme = Formes(self.x1,self.y1,event.x,event.y,self.choix)
            self.controleur.modele.formesTempo.append(forme)
            self.controleur.modele.formes.append(forme)
            self.afficherCaneva()
            
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
        print("Rectangle")
                    
    def detruitTempo(self):
       pass

        
    def dessinerTempo(self):
        if(self.choix == "Cercle"):
            #self.caneva.create_oval(self.x1,self.y1,self.x1+self.x1,self.y1+self.y1)  
            self.caneva.coords("tempoCercle",self.x1,self.y1,self.x2,self.y2)      
        #self.formeTemp = self.caneva.create_rectangle(self.x,self.y,self.x2,self.y2, tag="tempo")
        elif (self.choix == "Rectangle"):
            self.caneva.coords("tempoRectangle",self.x1,self.y1,self.x2,self.y2)
        elif (self.choix == "Fleche"):
            self.caneva.coords("tempoFleche",self.x1,self.y1,self.x2,self.y2)
    def callback(event):
        print ("clicked at", event.x, event.y)
        
        
        
class Modele():
    def __init__(self, pControleur):
        self.controleur = pControleur
        self.formesTempo = [ ]
        self.formes = [ ]    
    
'''    
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
'''                        
if __name__ == '__main__':
    c = Controleur()
