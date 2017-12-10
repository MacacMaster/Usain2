#-*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import *
import sqlite3
from datetime import datetime
from _overlapped import NULL

class Vue():
    def __init__(self, parent):
        print("in vue")
        self.parent=parent
        self.root=Tk() #Fenetre
        self.root.title("Sprint")
        self.hauteurTotale=600
        self.largeurTotale=800
        self.hauteurSub=500
        self.largeurSub=800
        self.fenetre = Frame(master=self.root, width=self.largeurTotale, height=self.hauteurTotale)
        self.fenetre.pack()
                   
