import os
import time
from app.orm import ORM
from app.account import Account
from app.trade import Trade
from app.position import Position

DIR = os.path.dirname(__file__)
DBFILENAME = 'ttrader.db'
DBPATH = os.path.join(DIR, DBFILENAME)

def seed(dbpath=DBPATH):
    ORM.dbpath = dbpath
    
    mike_bloom = Account(username='mike_bloom', balance=10000.00)
    mike_bloom.set_password('password')
    mike_bloom.save()

    # trade for a purchase of 10 shares yesterday
    # trade for a sell of 5 shares today

    tsla_position = Position(ticker='tsla', shares=5, accounts_pk=mike_bloom.values['pk'])
    tsla_position.save()
