# -*- coding: utf-8 -*-

import os,os.path
import sys
import Pyro4
import socket
from subprocess import Popen 
import math
from projet_vue import *
from IdMaker import Id

class Controleur():
    def __init__(self):
        print("Controleur")
        self.createurId=Id
        self.modele=None
        self.vue=Vue(self)
        self.vue.root.mainloop()
        
        
    
if __name__ == '__main__':
    c=Controleur()