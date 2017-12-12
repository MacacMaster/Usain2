Cette fonction (writeLog) écrit les actions sur une base de données situé avec le Serveur Saas. Seulement les développeurs y ont accès.
Elle va être utilisé pour le débogage et la facturation de nos clients.

L'utilisateur n'a aucune action à faire, le client écris et envoie les logs automatiquement.

Pour la facturation, les codes à utiliser sont M_2 pour l'ouverture du module, M_3 pour la fermeture du module. Il faut limiter à l'utilisateur qui à éxécuté l'action.

Les logs conservent la date, l'organisation, l'utilisateur, le module, l'action, le code de log.


LOGS CODES:
[Action][MODULE][CODE]
Action:
L = Login
M = Module
S = SQL
O = Outils
P = Projets

Modules:
0 = Client
1 = CasUsage
2 = CRC
3 = Mandat
4 = Maquette
5 = Modelisation
6 = PlanificationGlobale
7 = Sprint

E = Saas
F = ServeurBD

Codes:
0 = Success
1 = Fail
2 = Ouverture
3 = Fermeture
4 = INSERT
5 = UPDATE
6 = SELECT

L00 = Login Sucessful
L01 = Login Fail

M_2 = Ouverture du Module
M_3 = Fermeture du Module


Code

Controleur:
def __init__(self):
	self.writeLog("Ouverture du Module","M_2")

def fermerProgramme(self):
    self.writeLog("Fermeture du Module","M_3")
    self.vue.root.destroy()

def writeLog(self,action,codeid):
    self.serveur.writeLog(self.organisation,self.utilisateur,self.clientIP,self.saasIP,"Mandat",action,codeid) 

Vue
def __init__(self):
	self.root.protocol("WM_DELETE_WINDOW", self.parent.fermerProgramme)
