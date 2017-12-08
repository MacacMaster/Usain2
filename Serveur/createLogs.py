#-*- coding: utf-8 -*-

import sqlite3
import random

# Création d'un objet connect "database" à une base de donnée "fightus"
database = sqlite3.connect('Logs.sqlite')

# Création d'un curseur pour cette base de donnée
curseur = database.cursor()

curseur.execute('''CREATE TABLE "logs" ( `Date` INTEGER, `Organisation` TEXT, `Utilisateur` TEXT, `IP Client` TEXT, `IP Database` TEXT, `Module` TEXT, `Action` TEXT, `ErrorID` INTEGER )''')

# Sauvegarder (commit) les changements
database.commit()

# Fermer la connection a la bd
database.close()