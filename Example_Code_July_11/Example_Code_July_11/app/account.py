# MOVE THE ORM TO A DIFFERENT FOLDER, ADJUST DB PATH
#########################################################

import sqlite3
from collections import OrderedDict
# from app.orm import orm
# from app.util import hash_password
# from app.position import Position
# from app.trade import Trade
from .orm import ORM
from . import util
from .position import Position as p #<-- same as
import trade as t                   #<-- same as

class Account(ORM):

    tablename = "accounts"
    fields = ["username", "password_hash", "balance"]

    createsql = '''CREATE TABLE {} (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR,
        password_hash TEXT,
        balance FLOAT);'''.format(tablename)

    def __init__(self, **kwargs):
        self.values = OrderedDict()
        self.values['pk'] = kwargs.get('pk')
        self.values['username'] = kwargs.get('username')
        self.values['password_hash'] = kwargs.get('password_hash')
        self.values['balance'] = kwargs.get('balance')

    def __repr__(self):
        msg = '<Account pk:{pk}, username:{username}, password_hash:{password_hash}, balance:{balance}>'
        return msg.format(**self.values)

    @classmethod
    def login(cls, username, password):
        """ login: is a class method of Account class,
             \nit checks the username and password_hash
             \nin ttrader.db accounts table
             \nand returns an instance of that account"""
        
        return cls.one_from_where_clause("WHERE username = ? and password_hash = ?",
                                    (username, password))

    def get_positions(self):
        return p.Position.all_with_username(self.values['username'])

    def get_position_for(self, ticker):
        """ return a Position object for the user. if the position does not 
        exist, return a new Position with zero shares."""
        position = p.Position.one_from_where_clause(
            "WHERE ticker =? AND username =?", (ticker, self.values['username']))
        if position is None:
            return p.Position(username=self.values['username'], ticker=ticker, shares=0)
        return position

    def get_trades(self):
        """ return all of the user's trades ordered by time. returns a list of
        Trade objects """
        trades_lst = t.Trade.all_with_username(self.values['username'])
        return trades_lst

    def trades_for(self, ticker):
        """ return all of the user's trades for a given ticker. """
        trades_lst = t.Trade.all_from_where(
            "WHERE ticker =? AND username =?", (ticker, self.values['username']))
        return trades_lst
    
    def buy(self, ticker, amount):
        """ make a purchase! raise KeyError for a nonexistent stock and
        ValueError for insufficient funds. will create a new Trade and modify
        a Position and alters the user's balance. returns nothing """
        try:
            print('Looking up ticker price')
            ticker_price = util.lookup_price(ticker)

            print("ticker price is:", ticker_price)

            print('checking ticker*amount is less than self.values[balance]')
            if (ticker_price * amount) > self.values['balance']:
                raise ValueError
            else:
                self.values['balance'] = (self.values['balance'] - ticker_price * amount)
                self.update_row() #can change to save, saving new balance after purchase
                print('remaining balance is:', self.values['balance'])

                transaction = t.Trade(buy_sell = 'Buy', username = self.values['username'], 
                 ticker = ticker, price = ticker_price, 
                 shares = amount, time = 10.0) #fix time !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                transaction.save() #created a new instance: transaction, and saved it to trades table

                position = self.get_position_for(ticker) #
                position.values['shares'] += amount
                position.save()
        except:
            raise KeyError

    def sell(self, ticker, amount):
        """ make a sale! raise KeyError for a non-existent Position and
        ValueError for insufficient shares. will create a new Trade object,
        modify a Position, and alter the self.balance. returns nothing."""
        try:
            ticker_price = util.lookup_price(ticker)
            position = self.get_position_for(ticker)
            if position.values['shares'] < amount:
                raise ValueError
            else:
                position.values['shares'] -= amount
                position.save()
                transaction = t.Trade(buy_sell = 'Sell', username = self.values['username'],
                 ticker = ticker, price = ticker_price,
                 shares = amount, time = 10.0)
                transaction.save()
                self.values['balance'] += (ticker_price * amount)
                self.update_row()
        except:
            raise KeyError

if __name__ == "__main__":

    # table1 = Account()
    # table1.create_table()
    # table2 = p.Position()
    # table2.create_table()
    # table3 = t.Trade()
    # table3.create_table()

    # account1 = Account(username = 'Sami', password_hash = '1234', balance = 1000)
    # account1.save()
    # account1.buy('tsla',2)
    # account1.buy('aapl',1)
    # account1.sell('tsla',1)
    user = 'sami'
    password = '1234'
    passwordhash = util.hash_password(password)
    account = Account()
    logged_in = account.login(username = user, password = passwordhash)
    logged_in.buy('aapl',1)

    print(logged_in.values['username'])