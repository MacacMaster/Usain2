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

L_0 = Login Sucessful
L_1 = Login Fail

M_2 = Ouverture du Module
M_3 = Fermeture du Module

S_0 = 




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
self.root.protocol("WM_DELETE_WINDOW", self.parent.fermerProgramme)
