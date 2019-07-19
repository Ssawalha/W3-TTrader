import sqlite3
from time import time
from collections import OrderedDict
from model.orm import ORM
from model import util
from model import position as p
from model import trade as t    

class Account(ORM):

    tablename = "accounts"
    fields = ["username", "password_hash", "balance"]

    createsql = '''CREATE TABLE {} (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR NOT NULL,
        password_hash TEXT, 
        balance FLOAT, UNIQUE(username));'''.format(tablename)

    def __init__(self, **kwargs):
        self.values = OrderedDict()
        self.values['pk'] = kwargs.get('pk')
        self.values['username'] = kwargs.get('username')
        self.values['password_hash'] = kwargs.get('password_hash')
        self.values['balance'] = kwargs.get('balance')

    def __repr__(self):
        msg = '<Account pk:{pk}, username:{username}, password_hash:{password_hash}, balance:{balance}>'
        return msg.format(**self.values)

    def set_password(self, password):
        self.values['password_hash'] = util.hash_password(password)
    
    @classmethod
    def login(cls, username, password):
        """ login: is a class method of Account class,
             \nit checks the username and password_hash
             \nin ttrader.db accounts table
             \nand returns an instance of that account"""
        check_password_bool = util.check_password(username, password)
        if check_password_bool == True:
            return cls.one_from_where_clause("WHERE username = ?",(username,))

    def get_positions(self):
        return p.Position.all_with_username(self.values['username'])

    def get_position_for(self, ticker):
        """ return a Position object for the user. if the position does not 
        exist, return a new Position with zero shares."""
        ticker = ticker.lower()
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
        ticker = ticker.lower()
        trades_lst = t.Trade.all_from_where_clause(
            "WHERE ticker =? AND username =?", (ticker, self.values['username']))
        return trades_lst
    
    def buy(self, ticker, amount):
        """ make a purchase! raise KeyError for a nonexistent stock and
        ValueError for insufficient funds. will create a new Trade and modify
        a Position and alters the user's balance. returns nothing """
        ticker = ticker.lower()
        amount = int(amount)
        try:
            ticker_price = util.lookup_price(ticker)
            if (ticker_price * amount) > self.values['balance']:
                raise ValueError
            else:
                self.values['balance'] = (self.values['balance'] - ticker_price * amount)
                self.save()
                
                transaction = t.Trade(buy_sell = 'Buy', username = self.values['username'], 
                 ticker = ticker, price = ticker_price, 
                 shares = amount, time = time())
                transaction.save()
                
                position = self.get_position_for(ticker) #
                position.values['shares'] = (position.values['shares'] + amount)
                position.save()
        except:
            raise KeyError

    def sell(self, ticker, amount):
        """ make a sale! raise KeyError for a non-existent Position and
        ValueError for insufficient shares. will create a new Trade object,
        modify a Position, and alter the self.balance. returns nothing."""
        ticker = ticker.lower()
        amount = int(amount)
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
                 shares = amount, time = time())
                transaction.save()
                self.values['balance'] += (ticker_price * amount)
                self.update_row()
        except:
            raise KeyError

    def ticker_average_buy_price(self, ticker):
        # ticker_position = self.get_position_for(ticker)
        # ticker_position_shares = ticker_position.values['shares']
        # if ticker_position_shares > 0:
        ticker_trades_lst = self.trades_for(ticker)
        buy_trades = []
        buy_mkt_value =[]
        prices_sum = 0
        num_trades = 0
        for trade in ticker_trades_lst:
            if trade.values['buy_sell'] == 'Buy':
                buy_trades.append(trade)
                num_trades += 1
        for trade in buy_trades:
            buy_mkt_value.append(trade.values['price'] * trade.values['shares']) #this is where you are
            prices_sum += trade.values['price']
        
        average_price = (prices_sum/num_trades)
        return average_price

    def ticker_average_sell_price(self, ticker):
        ticker_trades_lst = self.trades_for(ticker)
        sell_trades = []
        sell_prices =[]
        prices_sum = 0
        num_trades = 0
        for trade in ticker_trades_lst:
            if trade.values['buy_sell'] == 'Sell':
                sell_trades.append(trade)
                num_trades += 1
        for trade in sell_trades:
            sell_prices.append(trade.values['price'])
            prices_sum += trade.values['price']
        
        average_price = (prices_sum/num_trades)
        return average_price

    def ticker_profit_loss(self, ticker):
        average_buy_price  = self.ticker_average_buy_price(ticker)
        average_sell_price = self.ticker_average_sell_price(ticker)

        profit_loss = average_sell_price - average_buy_price
        
        return profit_loss
                


