import os
from time import time
from model.orm import ORM
from model.account import Account

DIR = os.path.dirname(__file__)
DBFILENAME = 'ttrader.db'
DBPATH = os.path.join(DIR, DBFILENAME)

def seed(dbpath=DBPATH):
    ORM.dbpath = dbpath
    
    default = Account(username='sami', balance=10000.00)
    default.set_password('1234')
    default.save()

    default.buy('tsla',6)
    default.sell('tsla',1)
