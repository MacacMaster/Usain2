from tkinter import * 
from tkinter.filedialog import *


def explorateurFichiers(text):
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
    
    #Label(fenetre, text=content).pack(padx=10, pady=10)
    
fenetre = Tk()

label = Label(fenetre, text="Hello World")
label.pack()
value = StringVar() 
value.set("texte par defaut")
text = Text(fenetre, height=20, width=55)
text.pack()

button = Button(fenetre,text="Loader",command= lambda: explorateurFichiers(text))
button.pack()




fenetre.mainloop()