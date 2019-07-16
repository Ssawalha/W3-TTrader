#./test.sh
import sqlite3
import os
import unittest

from app.orm import ORM
from app.account import Account
from app.position import Position
from app.trade import Trade
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

    def test_save_and_pk_load(self):
        user = Account(username = 'Sami')
        user.save()
        self.assertIsInstance(user.values['pk'], int, 'save sets pk')  #assert will always return a boolean - if we get false back, something is broken

        pk = user.values['pk']
        same_user = Account.one_from_pk(pk)

        self.assertIsInstance(same_user, Account, 'one_from_pk loads an Account object')

        self.assertEqual(same_user.values['username'], 'Sami', 'save creates database row')
        same_user.username = 'Gregory'
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
        self.assertIsInstance(trades, Position, 'trades_for returns Trade objects' )
    

