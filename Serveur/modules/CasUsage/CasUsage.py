from tkinter import *
from logging.config import listen
from xmlrpc.client import ServerProxy

class Controleur():
    def __init__(self):
        self.saasIP=sys.argv[1]
        self.adresseServeur="http://"+self.saasIP+":9999"
        self.serveur = self.connectionServeur()
        self.vue = Vue(self)
        self.idScena=0
       
        self.unReprend=False
        self.id=1
       
        self.utilisateur=sys.argv[2]
        self.idProjet=sys.argv[4]
        self.clientIP=sys.argv[5]
        self.remplirListeCas()
        self.vue.root.mainloop()
        print("controleur")
   
    def connectionServeur(self):
        print("Connection au serveur BD...")
        serveur=ServerProxy(self.adresseServeur)
        return serveur
    
    def remplirListeCas(self):
        return self.serveur.selectionSQL("CasUsages","description")
    
    def remplirListeEtat(self):
        return self.serveur.selectionSQL("CasUsages","etat")
           
    def envoyerCas(self,cas,usager,machine):
        self.serveur.insertionSQL("CasUsages","'"+str(self.idProjet)+"','"+cas+"','Termine'")
        indiceCas=self.serveur.selectionSQL3("CasUsages","id","description",str(cas))
        self.serveur.insertionSQL("Humains","'"+str(indiceCas)+"','"+usager+"'")
        self.serveur.insertionSQL("Machines","'"+str(indiceCas)+"','"+machine+"'")
        self.vue.mettreAJourListes()
   
    def chercherBdcas(self,indice):
        return self.serveur.selectionSQL3("CasUsages","description","id",indice)
       
    def chercherUtilisateur(self,indice):
        print("Indice humain cas"            ,self.vue.indiceCasModifier)
        utilisateur=self.serveur.selectionSQL3("Humains","etat","id_CasUsage",self.vue.indiceCasModifier)
        print("humains                  ",utilisateur)
        return utilisateur
    
    def chercherMachine(self,indice):
       machine=self.serveur.selectionSQL2("Machines","etat","id","id_CasUsage",self.idScena,indice)
       return machine
    
    def modifierCas(self,cas,usager,machine):
        self.serveur.updateSQL("CasUsages",cas,"description","id","id_projet",self.vue.indiceCasModifier+1,self.idProjet)
        self.serveur.updateSQL("Humains",usager,"etat","id","id_CasUsage",self.idScena,self.vue.indiceCasModifier+1)
        self.serveur.updateSQL("Machines",machine,"etat","id","id_CasUsage",self.idMach,self.vue.indiceCasModifier+1)
   

    def indiceCasModifier(self, nomCas):
        indice=self.serveur.selectionSQL3("CasUsages","id", "description", nomCas)
        self.indice=str(indice)[2:int(len(indice)-3)]
        indiceGood=self.indice
        print("indice du cas a modifier  : ", indiceGood)
        return indiceGood
    
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

    def mettreAJourListes(self):
        self.remplirListeEtat()
        self.remplirListeCas()
        self.remplirListBoxEtat()
        self.remplirListBoxCas()    
    
    def menuInitial(self):
        self.caneva = Canvas(self.fenetre, width = self.largeur, height=self.hauteur, bg="steelblue")
        self.caneva.pack()
        self.labnbe=Label(text="Cas d'usage       ",bg="lightblue")
        self.caneva.create_window(150,50,window=self.labnbe)
        self.labelCasUsage=Entry(bg="white")
        self.caneva.create_window(150,120,window=self.labelCasUsage,width=150,height=100)
        
        self.labnbe=Label(text="Action usager    ",bg="lightblue")
        self.caneva.create_window(400,50,window=self.labnbe)
        self.labelActionUsager=Entry(bg="white")
        self.caneva.create_window(400,120,window=self.labelActionUsager,width=150,height=100)
        self.labnbe=Label(text="Action machine",bg="lightblue")
        self.caneva.create_window(650,50,window=self.labnbe)
        self.labelActionMachine=Entry(bg="white")
        self.caneva.create_window(650,120,window=self.labelActionMachine,width=150,height=100)

        self.btnEnvoyerUsager=Button(self.caneva,text="Envoyer",width=20,command=self.envoyerTexte)
        self.caneva.create_window(400,200,window=self.btnEnvoyerUsager,width=150,height=20)
    
        #self.btnModifier=Button(self.caneva,text="Modifier",width=20,command=self.indiceDeLaBD)
        #self.caneva.create_window(700,550,window=self.btnModifier,width=150,height=20)
        
        self.btnModifier=Button(self.caneva,text="Modifier",width=20,command=self.select)
        self.caneva.create_window(700,550,window=self.btnModifier,width=150,height=20)

        self.listeetat=Listbox(self.caneva,bg="lightblue",borderwidth=0,relief=FLAT,width=12,height=12)
        self.caneva.create_window(670,350,window=self.listeetat)
       

        self.listecas=Listbox(self.caneva,bg="lightblue",borderwidth=0,relief=FLAT,width=90,height=12)
        self.caneva.create_window(350,350,window=self.listecas)
        self.mettreAJourListes()

    def select(self):
        print(self.controleur.serveur.selectionSQL("Humains","id"))
        
    def indiceCasModifier(self, nomCas):
        print(nomCas,"indicecas2")
        self.controleur.indiceCasModifier(nomCas)
        #self.menuModifier()
         
    def indiceDeLaBD(self):
        #self.indiceCasModifier=self.listecas.curselection()[0]
       # print("indice a modifier : ",self.indiceCasModifier)
       # self.menuModifier()
        position=self.listecas.curselection()[0] # indice du cas selectionné
        print(position)
        nomCasSelection=self.listecas.get(position, position)
        if(position!=0):
            nomCasSelectionGood=str(nomCasSelection)[4:int(len(nomCasSelection)-6)]
        else: 
            nomCasSelectionGood=str(nomCasSelection)[2:int(len(nomCasSelection)-2)]
        print("nom cas a modifier : ",nomCasSelectionGood, "    : ", nomCasSelection)
        self.indiceCasModifier=self.controleur.indiceCasModifier(nomCasSelectionGood)
        #humain=self.controleur.humainCasModifier(indice)
        self.menuModifier()

    def remplirListeCas(self):
        self.listeCas=self.controleur.remplirListeCas()
   
    def remplirListeEtat(self):
        self.listeEtat=self.controleur.remplirListeEtat()
    
    def remplirListBoxCas(self):
        self.listecas.delete(0, END)
        laselection=self.controleur.remplirListeCas()
        
        for i in laselection:
            temp=str(i)[3:int(len(i)-5)]
            self.listeetat.insert(END,temp)
            #print("CAS",i)
            self.listecas.insert(END,i)
        self.listeCas.clear()
            
    def remplirListBoxEtat(self):
        self.listeetat.delete(0, END)
        for i in self.listeEtat:
            temp=str(i)
            self.listeetat.insert(END,temp)
        self.listeEtat.clear()
        
    def menuModifier(self):
        self.caneva.forget()
        self.canevaMod = Canvas(self.fenetre, width = self.largeur, height=self.hauteur, bg="steelblue")
        self.canevaMod.pack()
        self.labnbe=Label(text="Cas d'usage       ",bg="lightblue")
        self.canevaMod.create_window(150,50,window=self.labnbe)
        self.labelCasUsage=Entry(bg="white")
        self.canevaMod.create_window(150,200,window=self.labelCasUsage,width=150,height=250)
        
        self.labnbe=Label(text="Action usager    ",bg="lightblue")
        self.canevaMod.create_window(400,50,window=self.labnbe)
        self.labelActionUsager=Entry(bg="white")
        self.labelActionMachine=Entry(bg="white")
        self.canevaMod.create_window(650,200,window=self.labelActionMachine,width=150,height=250)
        
        cas=self.controleur.chercherBdcas(self.indiceCasModifier,);
        self.labelCasUsage.insert(END, str (cas))
        
        usager=self.controleur.chercherUtilisateur(self.indiceCasModifier,)#
        self.labelActionUsager.insert(END, str(usager))

        machine=self.controleur.chercherMachine(self.indiceCasModifier,),
        self.labelActionMachine.insert(END,str(machine))
        
        self.canevaMod.create_window(400,200,window=self.labelActionUsager,width=150,height=250)
        self.labnbe=Label(text="Action machine",bg="lightblue")
        self.canevaMod.create_window(650,50,window=self.labnbe)
        self.btnEnvoyerUsager=Button(self.canevaMod,text="Envoyer",width=20,command=self.envoyerTexte)
        self.canevaMod.create_window(400,200,window=self.btnEnvoyerUsager,width=150,height=20)
        self.btnRetour=Button(self.canevaMod,text="Retour",width=20,command=self.menuInitialMod)
        self.canevaMod.create_window(100,550,window=self.btnRetour,width=150,height=20)
        self.bntModifier=Button(self.canevaMod,text="Modifier",width=20,command=self.modifierTexte)
        self.canevaMod.create_window(150,400,window=self.bntModifier,width=150,height=20)
    
        
    def supprimer(self):
        self.indiceCasModifier=self.listeetat.curselection()[0]
        print(self.indiceCasModifier)
        self.controleur.changerEtat(self.indiceCasModifier+1)
    
    def menuInitialMod(self):
        self.canevaMod.forget()
        self.menuInitial()
       
    def modifierTexte(self):
        cas=self.labelCasUsage.get()
        usager=self.labelActionUsager.get()
        machine=self.labelActionMachine.get()
        self.controleur.modifierCas(cas,usager,machine)
        
    def envoyerTexte(self):
        cas=self.labelCasUsage.get()
        usager=self.labelActionUsager.get()
        machine=self.labelActionMachine.get()
        self.insererCas(cas,usager,machine)
        self.labelActionUsager.delete(0, 'end')
        self.labelCasUsage.delete(0, 'end')
        self.labelActionMachine.delete(0, 'end')

    def insererCas(self,cas,usager,machine):
        self.controleur.envoyerCas(cas,usager,machine)
    
if __name__ == '__main__':
    c = Controleur()