import os
import time
from model.orm import ORM
from model.account import Account
from model.trade import Trade
from model.position import Position
from model import util

DIR = os.path.dirname(__file__)
DBFILENAME = 'ttrader.db'
DBPATH = os.path.join(DIR, DBFILENAME)

def seed(dbpath=DBPATH):
    ORM.dbpath = dbpath
    
    default = Account(username='sami', balance=10000.00)
    default.set_password('1234')
    default.save()

    # trade for a purchase of 10 shares yesterday
    # trade for a sell of 5 shares today

    # default.buy('tsla', 1) <--wouldnt make sense to use since we are going to test it

    tsla_position = Position(ticker='tsla', shares=5, username=default.values['username'])
    tsla_position.save()

    tsla_price = util.lookup_price('tsla')
    tsla_transaction = Trade(buy_sell='Buy', username=default.values['username'], ticker='tsla', price=tsla_price, shares = 5, time = 10.0) #fix time
    tsla_transaction.save()
    tsla_transaction1 = Trade(buy_sell='Sell', username=default.values['username'], ticker='tsla', price=tsla_price, shares = 1, time = 10.0)
    tsla_transaction1.save()
