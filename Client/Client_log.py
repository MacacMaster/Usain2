# -*- coding: utf-8 -*-


from datetime import datetime
import sqlite3
from datetime import datetime
sqlite_file = 'example.db'


class Log():
    #Var globales
    logLocation = "log.txt"
    parent=None
    organisation=""
    user=""
    clientip=None
    dbip=None
    
#    def __init__(self,organisation="Organisation",user="User",action="Action",ip = "8.8.8.8",db="1.1.1.1"):
    def __init__(self,parent,ip):
        self.clientip=ip
        self.parent=parent
        #=======================================================================
        # logLocation='Logs.sqlite'
        # logdb = sqlite3.connect(logLocation)
        # curseur = logdb.cursor()
        # curseur.execute('''CREATE TABLE logs (date text, organisation text, user text, ip text, db text, module text, action text)''')
        #=======================================================================
        
        #=======================================================================
        # 
        # conn.commit()
        # conn.close()
        # 
        # #Ecrit le log localement
        # self.log  = open(self.logLocation, "w")
        # self.log.write(time.strftime("%c")+" - "+organisation+" - "+user+" - "+ip+" - "+db+" - "+module+" - "+action)
        # self.log.close()
        #=======================================================================
    
    #Assigner les valeurs qui ne changeront pas directement dans la classe
    def setLog(self,organisation="Organisation",user="User"):
        self.organisation=organisation
        self.user=user

    
    #La fonction d'écriture du log
    def writeLog(self,action="Actionman",errorid="L01",module="Client"):
        #print(self.getTime() + " "+self.organisation + " "+self.user + " "+self.clientip + " "+self.dbip + " "+module + " "+action)
        if (self.parent.serveur.writeLog(self.organisation,self.user,self.clientip,self.parent.saasIP,module,action,errorid)):
            return True
        else:
            return False

    #===========================================================================
    # def logWrite2(self,module="a.py",action="Action"):
    #     #log in txt file
    #     self.log = open(self.logLocation, "a")
    #     self.log.write("\n"+time.strftime("%c")+" - "+organisation+" - "+user+" - "+ip+" - "+db+" - "+module+" - "+action)
    #     self.log.close()
    #===========================================================================