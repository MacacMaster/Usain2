import sqlite3
import random

# Création d'un objet connect "database" à une base de donnée "fightus"
database = sqlite3.connect('SprintMasterData.db')

# Création d'un curseur pour cette base de donnée
curseur = database.cursor()

# Creer une table si elle n'existe pas
curseur.execute('''CREATE TABLE IF NOT EXISTS Organisations
             (id integer, nom text)''')

curseur.execute('''CREATE TABLE IF NOT EXISTS Usagers
             (id integer, id_Organisation integer, nom text, motDePasse text)''')
             
curseur.execute('''CREATE TABLE IF NOT EXISTS Projets
             (id integer, id_Organisation integer, nom text)''')

curseur.execute('''CREATE TABLE IF NOT EXISTS Tables
             (id integer, id_Projet integer, nom text)''')

curseur.execute('''CREATE TABLE IF NOT EXISTS Champs
             (id integer, id_Table integer, nom text, contrainte text, type text, etat text)''')

curseur.execute('''CREATE TABLE IF NOT EXISTS CasUsages
             (id integer, id_Projet integer, description text, etat text)''')

curseur.execute('''CREATE TABLE IF NOT EXISTS Humains
             (id integer, id_CasUsage integer, etat text)''')

curseur.execute('''CREATE TABLE IF NOT EXISTS Machines
             (id integer, id_CasUsage integer, etat text)''')

curseur.execute('''CREATE TABLE IF NOT EXISTS Classes
             (id INTEGER PRIMARY KEY, id_Projet integer, proprietaire text, nom text)''')

curseur.execute('''CREATE TABLE IF NOT EXISTS Responsabilites
             (id integer, id_Classe integer, nom text)''')

curseur.execute('''CREATE TABLE IF NOT EXISTS Collaborations
             (id integer, id_Classe integer, nom text)''')

curseur.execute('''CREATE TABLE IF NOT EXISTS Mandats
             (id integer, id_Projet integer, contenu text, type text, nature text, emplacement text)''')

curseur.execute('''CREATE TABLE IF NOT EXISTS Textes
             (id integer, id_Projet integer, texte text)''')

curseur.execute('''CREATE TABLE IF NOT EXISTS PlanifGlobales
             (id integer, id_Projet integer, id_Sprint, id_Reponsable, nom_fonction text,priorite text, date_debut text, date_fin text)''')

curseur.execute('''CREATE TABLE IF NOT EXISTS Sprints
             (id integer, date_debut text, date_fin text, nom text)''')

curseur.execute('''CREATE TABLE IF NOT EXISTS Formes
             (id integer,id_Projet integer, x1 integer, y1 integer, x2 integer, y2 integer, texte text, nom text)''')

# Supprimer tout ce qui se trouve dans la bd
for comptes in curseur.execute('SELECT id FROM Organisations'):
    curseur.execute('DELETE FROM Organisations')
    curseur.execute('DELETE FROM Usagers')
    curseur.execute('DELETE FROM Projets')
    curseur.execute('DELETE FROM Tables')
    curseur.execute('DELETE FROM Champs')
    curseur.execute('DELETE FROM CasUsages')
    curseur.execute('DELETE FROM Humains')
    curseur.execute('DELETE FROM Machines')
    curseur.execute('DELETE FROM Classes') #C'est la table CRC
    curseur.execute('DELETE FROM Responsabilites')
    curseur.execute('DELETE FROM Collaborations')
    curseur.execute('DELETE FROM Mandats')
    curseur.execute('DELETE FROM PlanifGlobales')
    curseur.execute('DELETE FROM Sprints')
    curseur.execute('DELETE FROM Formes')
    
# Ajouter les nouveaux comptes
curseur.execute("INSERT INTO Organisations VALUES ('1', 't')")
curseur.execute("INSERT INTO Organisations VALUES ('2', 'a')")

curseur.execute("INSERT INTO Usagers VALUES ('1', '1', 't', 't')")
curseur.execute("INSERT INTO Usagers VALUES ('2', '1', 'a', 'a')")
curseur.execute("INSERT INTO Usagers VALUES ('3', '2', 'a', 'a')")
curseur.execute("INSERT INTO Usagers VALUES ('4','1', 'admin', 'a')")


curseur.execute("INSERT INTO Projets VALUES ('1', '1', 'ProjetTest')")
curseur.execute("INSERT INTO Projets VALUES ('2', '2', 'Projet1')")
curseur.execute("INSERT INTO Projets VALUES ('3', '1', 'Projet1')")

curseur.execute("INSERT INTO Tables VALUES ('1', '1', 'Table1')")
curseur.execute("INSERT INTO Tables VALUES ('2', '1', 'Table2')")

# Voir les objets de la bd
for comptesOrg in curseur.execute('SELECT * FROM Organisations'):
    print(comptesOrg)
    
for comptesOrg in curseur.execute('SELECT * FROM Usagers'):
    print(comptesOrg)
    
    
for comptesOrg in curseur.execute('SELECT * FROM Projets'):
    print(comptesOrg)
    
for comptesOrg in curseur.execute('SELECT * FROM Tables'):
    print(comptesOrg)

# Sauvegarder (commit) les changements
database.commit()

# Fermer la connection a la bd
database.close()