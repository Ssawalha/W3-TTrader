#./test.sh
import sqlite3
import os
import unittest

from model.orm import ORM
from model.account import Account
from model.position import Position
from model.trade import Trade
from model import util
from data.seed import seed
from data.schema import schema

DIR = os.path.dirname(__file__)
DBFILENAME = '_tests.db'
DBPATH = os.path.join(DIR, DBFILENAME)

ORM.dbpath = DBPATH

class TestAccount(unittest.TestCase):
    def setUp(self):
        schema(DBPATH)
        seed(DBPATH)
    
    def tearDown(self):
        os.remove(DBPATH)

    def test_hash_password(self):
        password = '1234'
        hashed_pw = util.hash_password(password)
        self.assertIsInstance(hashed_pw, bytes, 'util.hash_password takes a string input, and returns a byte string (the hashed pw and salt)')

    def test_check_password(self):
        user = Account()
        username = 'sami'
        user_info = user.one_from_where_clause('WHERE username = ?', (username,))
        self.assertIsInstance(user_info, Account, 'one_from_where_clause returns an account object where its username matches the username we gave it')
        
        hashed_pw = user_info.values['password_hash']
        self.assertIsInstance(hashed_pw, bytes, 'hashed_pw from db')

        password = '1234'
        password = password.encode()
        
        self.assertEqual = (util.bcrypt.checkpw(password, hashed_pw), True) #returns True or False
        
    def test_save_and_pk_load(self):
        user = Account(username = 'Sami')
        user.save()
        self.assertIsInstance(user.values['pk'], int, 'save sets pk')  #assert will always return a boolean - if we get false back, something is broken

        pk = user.values['pk']
        same_user = Account.one_from_pk(pk)

        self.assertIsInstance(same_user, Account, 'one_from_pk loads an Account object')

        self.assertEqual(same_user.values['username'], 'Sami', 'save creates database row')
        same_user.values['username'] = 'Gregory'
        same_user.save()
        same_again = Account.one_from_pk(pk)

        self.assertEqual(same_again.values['username'], 'Gregory', 'save updates an exisiting row')


    def test_get_positions(self):
        user = Account.one_from_pk(1)
        positions = user.get_positions()
        self.assertIsInstance(positions, list, 'get_positions returns a list')
        self.assertIsInstance(positions[0], Position, 'get_positions returns Position objects')

    def test_get_position_for(self):
        user = Account.one_from_pk(1)
        positions = user.get_position_for('TSLA')
        self.assertIsInstance(positions, Position, 'get_position_for returns one Position object' )

    def test_get_trades(self):
        user = Account.one_from_pk(1)
        trades = user.get_trades()
        self.assertIsInstance(trades, list, 'get_trades returns a list')
        self.assertIsInstance(trades[0], Trade, 'get_trades returns Position objects')

    def test_get_trades_for(self):
        user = Account.one_from_pk(1)
        trades = user.trades_for('TSLA')
        self.assertIsInstance(trades, list, 'trades_for returns a list')
        self.assertIsInstance(trades[0], Trade, 'trades_for returns Trade objects')
    
    def test_login(self):
        password = '1234'
        user = Account.login('sami', password)
        self.assertIsInstance(user, Account, 'if the username and password match what is in db, login returns an Account object')

    def test_buy(self):
        user = Account.one_from_pk(1)
        user_balance_before = user.values['balance']
        user.buy('AAPL', 1)
        user_balance_after = (user_balance_before - util.lookup_price('aapl'))
        self.assertEqual(user.values['balance'], user_balance_after, 'buy if account balance > ticker_price * shares, account balance deducted')
        
        transaction = user.trades_for('aapl')
        self.assertIsInstance(transaction[0], Trade, 'trades_for returns Trade objects')
        self.assertEqual(transaction[0].values['buy_sell'], 'Buy')
        self.assertEqual(transaction[0].values['shares'], 1)
        self.assertEqual(transaction[0].values['username'], 'sami')

        account_position = user.get_position_for('aapl') 
        self.assertIsInstance(account_position, Position, 'get_position_for returns Position object')
        self.assertEqual(account_position.values['shares'], 1)
        self.assertEqual(account_position.values['username'], 'sami')

    def test_sell(self):
        user = Account.one_from_pk(1)
        user_balance_before = user.values['balance']
        user.sell('tsla', 1)
        user_balance_after = (user_balance_before + util.lookup_price('tsla'))
        self.assertEqual(user.values['balance'], user_balance_after, 'account balance increased for ticker_price * amount ')
        
        transaction = user.trades_for('TSLA')
        self.assertIsInstance(transaction[2], Trade, 'trades_for returns Trade objects')
        self.assertEqual(transaction[2].values['buy_sell'], 'Sell')
        self.assertEqual(transaction[2].values['shares'], 1)
        self.assertEqual(transaction[2].values['username'], 'sami')

        account_position = user.get_position_for('TSLA') 
        self.assertIsInstance(account_position, Position, 'get_position_for returns Position object')
        self.assertEqual(account_position.values['shares'], 4)
        self.assertEqual(account_position.values['username'], 'sami')

##############  how do i clean the positions table if a user has 0 of that stock (useless rows)