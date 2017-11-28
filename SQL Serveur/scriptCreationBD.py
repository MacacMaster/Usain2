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

# Supprimer tout ce qui se trouve dans la bd
for comptes in curseur.execute('SELECT id FROM Organisations'):
    curseur.execute('DELETE FROM Organisations')
    curseur.execute('DELETE FROM Usagers')
    curseur.execute('DELETE FROM Projets')
    
# Ajouter les nouveaux comptes
curseur.execute("INSERT INTO Organisations VALUES ('1', 't')")
curseur.execute("INSERT INTO Organisations VALUES ('2', 'a')")

curseur.execute("INSERT INTO Usagers VALUES ('1', '1', 't', 't')")
curseur.execute("INSERT INTO Usagers VALUES ('2', '1', 'a', 'a')")
curseur.execute("INSERT INTO Usagers VALUES ('3', '2', 'a', 'a')")


curseur.execute("INSERT INTO Projets VALUES ('1', '1', 'ProjetTest')")
curseur.execute("INSERT INTO Projets VALUES ('2', '2', 'Projet1')")
curseur.execute("INSERT INTO Projets VALUES ('3', '1', 'Projet1')")

# Voir les objets de la bd
for comptesOrg in curseur.execute('SELECT * FROM Organisations'):
    print(comptesOrg)
    
for comptesOrg in curseur.execute('SELECT * FROM Usagers'):
    print(comptesOrg)
    
    
for comptesOrg in curseur.execute('SELECT * FROM Projets'):
    print(comptesOrg)

# Sauvegarder (commit) les changements
database.commit()

# Fermer la connection a la bd
database.close()