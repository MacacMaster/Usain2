# -*- coding: utf-8 -*-

import sqlite3
from time import *
from Sprint  import *

#TODO - UPDATE

class Modele():
    def __init__(self, parent):
        self.parent=parent

    def getTime(self):
        return (datetime.now().strftime('%Y/%m/%d %H:%M:%S'))