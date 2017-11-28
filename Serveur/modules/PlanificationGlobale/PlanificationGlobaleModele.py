# -*- coding: utf-8 -*-

import sqlite3

class Modele():
    def __init__(self, parent):
        pass
        
    def importerDonnees(self,projectName):
        pass

    def getTime(self):
        return (datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
class SQL():
    def __init__(self, adresseServeur):
        self.adresseServeur=adresseServeur
        
        pass
          