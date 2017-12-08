from tkinter import *
from PIL import Image, ImageTk
import sqlite3
from xmlrpc.client import ServerProxy
import sys

class Controleur():
    def __init__(self):
        self.serveur = None
        self.idMaquette = None
        self.idProjet = int(sys.argv[4])
        self.saasIP = sys.argv[1]
        self.connexionSaas()
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.chargerMaquette()
        self.vue.root.mainloop()

    def chargerMaquette(self):
        for i in self.serveur.selectionSQL3("Maquettes","nom","id_Projet", self.idProjet):
            self.vue.listeMaquettes.insert(END,i[0])
        
    def connexionSaas(self):
        ad="http://"+self.saasIP+":9999"
        self.serveur=ServerProxy(ad,allow_none = 1)
        
    def commitNouvelleMaquette(self, nomMaquette):
        self.serveur.insertionSQL("Maquettes", "'"+str(self.idProjet)+"', '"+nomMaquette+"'")
        self.vue.entreNouvMaquette.delete(0,END)
        self.vue.listeMaquettes.insert(END,nomMaquette)
        
    def chargerFormesMaquette(self, nomMaquette):
        self.modele.viderListes()
        self.vue.nettoyerCanevasDessin()
        self.idMaquette = self.serveur.selectionSQL3("Maquettes","id","nom", nomMaquette)
        self.idMaquette = str(self.idMaquette)[2:len(self.idMaquette)-3]
        for i in self.serveur.selectionSQL3("Formes","id, x1, y1, x2, y2, texte, nom","id_Maquette", self.idMaquette):
            forme = Forme(i[1], i[2], i[3], i[4], i[6], i[5])
            self.modele.formesTemporaire.append(forme)
        self.modele.miseAJourNbFormes()

    def commitNouvellesFormes(self):
        for i in self.modele.formes:
            self.serveur.insertionSQL("Formes", "'"+str(self.idMaquette)+"', '"+str(i.x1)+"', '"+str(i.y1)+"', '"+str(i.x2)+"', '"+str(i.y2)+"', '"+i.text+"', '"+i.nom+"'")
        self.modele.miseAJourNbFormes()
        
    

class Vue():
    def __init__(self, pControleur):
        self.controleur = pControleur
        self.largeur = 800
        self.hauteur = 600
        self.root = Tk()
        self.creerFenetre()
        self.bindTouche()
        self.afficherFormes()
        
    def nettoyerCanevasDessin(self):
        self.canvasDessin.destroy()
        self.canvasDessin = Canvas(self.zoneDessin, width = self.largeur+17, height = self.hauteur -80, borderwidth=1, relief="solid", bg="white")
        self.canvasDessin.pack()
        self.bindTouche()
        
    def creerFenetre(self):
        self.imgRectangle = PhotoImage(file="Maquette/rectangle.gif")
        self.imgRetour = PhotoImage(file="Maquette/retour.gif")
        self.imgOvale = PhotoImage(file="Maquette/cercle.gif")
        self.imgFleche = PhotoImage(file="Maquette/fleche.gif")
        self.imgSauvegarde = PhotoImage(file="Maquette/save.gif")
        self.imgNouvMaquette = PhotoImage(file="Maquette/crayon.gif")
        
        self.cadreMaquette = Frame(self.root, width = self.largeur, height = self.hauteur)
        self.menuTop = Frame(self.cadreMaquette, width = self.largeur, height = self.hauteur-520)
        self.zoneDessin = Frame(self.cadreMaquette, width = self.largeur, height = self.hauteur-80)
        
        self.optionGauche = Canvas(self.menuTop, width = self.largeur/3, height = self.hauteur -520, borderwidth=2, relief="ridge")
        self.optionMilieu = Canvas(self.menuTop, width = self.largeur/3, height = self.hauteur -520, borderwidth=2, relief="ridge")
        self.optionDroite = Canvas(self.menuTop, width = self.largeur/3, height = self.hauteur -520, borderwidth=2, relief="ridge")
        self.canvasDessin = Canvas(self.zoneDessin, width = self.largeur+17, height = self.hauteur -80, borderwidth=1, relief="solid", bg="white")
        
        self.labelMaquette = Label(self.optionGauche, text="Maquette en cours d'utilisation")
        self.listeMaquettes = Listbox(self.optionGauche)
        self.labelOutils = Label(self.optionMilieu, text="Outils")
        self.boutonChargerMaquette = Button(self.optionGauche,image=self.imgNouvMaquette,width=30, command = lambda: self.selectionOutils("ChargerMaquette"))
        self.boutonRectangle = Button(self.optionMilieu,image=self.imgRectangle,width=30, command= lambda: self.selectionOutils("Rectangle"))
        self.boutonOvale = Button(self.optionMilieu,image=self.imgOvale,width=30, command = lambda: self.selectionOutils("Ovale"))
        self.boutonFleche = Button(self.optionMilieu,image=self.imgFleche,width=30, command = lambda: self.selectionOutils("Fleche"))
        self.boutonTexte = Button(self.optionMilieu,text="A",width=30, font=('Arial', 22), command = lambda: self.selectionOutils("Texte"))
        self.boutonSauvegarde = Button(self.optionMilieu,image=self.imgSauvegarde,width=30, command = lambda: self.selectionOutils("CommitChangement"))
        self.boutonAnnuleForme = Button(self.optionMilieu,image=self.imgRetour,width=30, command = self.annulerForme)
        self.labelNouvMaquette = Label(self.optionDroite, text="Nouvelle maquette")
        self.entreNouvMaquette = Entry(self.optionDroite)
        self.boutonNouvMaquette = Button(self.optionDroite,text="OK",width=30, command = lambda: self.selectionOutils("CommitNouvMaquette"))
        
        self.optionGauche.create_window(115,60, window=self.listeMaquettes,width=190,height=50)
        self.optionGauche.create_window(135,20, window=self.labelMaquette,width=240,height=30)
        self.optionGauche.create_window(245,60, window=self.boutonChargerMaquette,width=40,height=30)
        self.optionMilieu.create_window(245,60, window=self.boutonSauvegarde,width=40,height=30)
        self.optionMilieu.create_window(120,60, window=self.boutonFleche,width=40,height=30)
        self.optionMilieu.create_window(165,60, window=self.boutonTexte,width=40,height=30)
        self.optionMilieu.create_window(205,60, window=self.boutonAnnuleForme,width=40,height=30)
        self.optionMilieu.create_window(75,60, window=self.boutonOvale,width=40,height=30)
        self.optionMilieu.create_window(30,60, window=self.boutonRectangle,width=40,height=30)
        self.optionMilieu.create_window(135,20, window=self.labelOutils,width=240,height=30)
        self.optionDroite.create_window(115,60, window=self.entreNouvMaquette,width=190,height=30)
        self.optionDroite.create_window(135,20, window=self.labelNouvMaquette,width=240,height=30)
        self.optionDroite.create_window(245,60, window=self.boutonNouvMaquette,width=40,height=30)
        
        self.menuTop.pack()
        self.zoneDessin.pack()
        self.optionGauche.pack(side=LEFT)
        self.optionMilieu.pack(side=LEFT)
        self.optionDroite.pack(side=LEFT)
        self.cadreMaquette.pack()
        self.canvasDessin.pack()

    def bindTouche(self):
        self.canvasDessin.bind('<B1-Motion>', self.deplacementSouris)
        self.canvasDessin.bind('<Button-1>', self.clicSouris)
        self.canvasDessin.bind('<ButtonRelease-1>', self.relacheSouris)
        
    def afficherFormes(self):
        self.canvasDessin.delete("ALL")
        for i in self.controleur.modele.formesTemporaire:
            if (i.nom == "Rectangle"):
                self.canvasDessin.create_rectangle(i.x1,i.y1,i.x2, i.y2)
                print("je dessine un rectangle")
            elif (i.nom == "Ovale"):
                self.canvasDessin.create_oval(i.x1,i.y1,i.x2, i.y2)
            elif (i.nom == "Fleche"):
                self.canvasDessin.create_line(i.x1,i.y1,i.x2, i.y2)
                print("je dessine une fleche")
            elif (i.nom  == "Texte"):
                self.canvasDessin.create_text(i.x1, i.y1, text=i.text,font=("Purisa",12))
        self.root.after(250, self.afficherFormes)
        
    def annulerForme(self):
        if len(self.controleur.modele.formesTemporaire) > self.controleur.modele.nbFormesCharger:
            self.controleur.modele.formesTemporaire.pop()
            self.controleur.modele.formes.pop()
            self.nettoyerCanevasDessin()
        
    def deselectionner(self, event):
        self.canvasDessin.focus_force()
        if (self.controleur.modele.choixForme == "Texte"):
            textTemporaire = Forme(self.controleur.modele.posForme[0],
                                    self.controleur.modele.posForme[1],
                                    0,
                                    0,
                                    "Texte",
                                    self.entryTemp.get())
            self.controleur.modele.formesTemporaire.append(textTemporaire)
            self.controleur.modele.formes.append(textTemporaire)
            self.entryTemp.destroy()
    
    def deplacementSouris(self,event):
        self.controleur.modele.posForme[2] = event.x
        self.controleur.modele.posForme[3] = event.y
        self.dessinerFormeTemporaire()
        
    def clicSouris(self,event):
        self.controleur.modele.posForme[0] = event.x
        self.controleur.modele.posForme[1] = event.y
        
    def relacheSouris(self, event):
        if self.controleur.modele.choixForme == "Texte":
            self.entryTemp = Entry(self.canvasDessin, bd = 0, font=("Purisa",12))
            self.entryTemp.bind('<Return>',self.deselectionner)
            self.entryTemp.place(x= event.x, y= event.y)
            self.entryTemp.focus_force()
        else:
            formeTemporaire = Forme(self.controleur.modele.posForme[0],
                                                self.controleur.modele.posForme[1],
                                                self.controleur.modele.posForme[2],
                                                self.controleur.modele.posForme[3],
                                                self.controleur.modele.choixForme,
                                                "i")
            self.controleur.modele.formesTemporaire.append(formeTemporaire)
            self.controleur.modele.formes.append(formeTemporaire)
    
    def dessinerFormeTemporaire(self):
        self.canvasDessin.delete("FormeNonFini")
        if(self.controleur.modele.choixForme == "Rectangle"):
            self.canvasDessin.create_rectangle(self.controleur.modele.posForme[0],
                                               self.controleur.modele.posForme[1],
                                               self.controleur.modele.posForme[2],
                                               self.controleur.modele.posForme[3],
                                               tags="FormeNonFini")
        elif(self.controleur.modele.choixForme == "Ovale"):
            self.canvasDessin.create_oval(self.controleur.modele.posForme[0],
                                               self.controleur.modele.posForme[1],
                                               self.controleur.modele.posForme[2],
                                               self.controleur.modele.posForme[3],
                                               tags="FormeNonFini")
        elif(self.controleur.modele.choixForme == "Fleche"):
            self.canvasDessin.create_line(self.controleur.modele.posForme[0],
                                               self.controleur.modele.posForme[1],
                                               self.controleur.modele.posForme[2],
                                               self.controleur.modele.posForme[3],
                                               tags="FormeNonFini")
        elif(self.controleur.modele.choixForme == "Texte"):
            self.text_id = self.canvasDessin.create_text(self.controleur.modele.posForme[0],self.controleur.modele.posForme[1], anchor="nw", text="")
            self.canvasDessin.itemconfig(self.text_id, text="")
        
    def selectionOutils(self, nomBouton):
        if (nomBouton == "Rectangle"):
            self.controleur.modele.choixForme = "Rectangle"
        elif (nomBouton == "Ovale"):
            self.controleur.modele.choixForme = "Ovale"
        elif (nomBouton == "Fleche"):
            self.controleur.modele.choixForme = "Fleche"
        elif (nomBouton == "Texte"):
            self.controleur.modele.choixForme = "Texte"
        elif (nomBouton == "CommitChangement"):
            self.controleur.commitNouvellesFormes()
        elif (nomBouton == "CommitNouvMaquette"):
            self.controleur.commitNouvelleMaquette(self.entreNouvMaquette.get())
        elif (nomBouton == "ChargerMaquette"):
            self.controleur.chargerFormesMaquette(self.listeMaquettes.selection_get())
                
                
class Modele():
    def __init__(self, pControleur):
        self.controleur = pControleur
        self.posForme = [ 0, 0, 0, 0 ]
        self.formes = [ ]
        self.formesTemporaire = [ ]
        self.choixForme = None
        self.choixText = None
        self.nbFormesCharger = None
        
    def viderListes(self):
        self.formes[:] = [ ]
        self.formesTemporaire[:] = [ ]
        
    def miseAJourNbFormes(self):
        self.nbFormesCharger = len(self.formesTemporaire)
        
        

class Forme():
    def __init__(self, pX1, pY1, pX2, pY2, pNom, pText):
        self.x1 = pX1
        self.y1 = pY1
        self.x2 = pX2
        self.y2 = pY2
        self.nom = pNom
        self.text = pText


if __name__ == '__main__':
    c = Controleur()