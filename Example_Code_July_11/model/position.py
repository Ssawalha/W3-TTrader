import sqlite3
from collections import OrderedDict
from orm import ORM
import util
import account
import trade
# from app.orm import orm
# from app.util import hash_password
# from app.account import Account

class Position(ORM):
    '''Python class which inherits from the class ORM. 
    \nPositions represents a single trade record, which contains: 
    \nusername - VARCHAR | foreign key
    \nticker - VARCHAR | stock ticker
    \nshares - INTEGER | the number of shares
    '''

    tablename = "positions"
    fields = ['username','ticker', 'shares']

    createsql = '''CREATE TABLE {} (pk INTEGER PRIMARY KEY AUTOINCREMENT, 
                username VARCHAR, ticker VARCHAR, shares INTEGER);'''.format(tablename)

    def __init__(self, **kwargs):
        self.values = OrderedDict()
        self.values['pk'] = kwargs.get('pk')
        self.values['username'] = kwargs.get('username')
        self.values['ticker'] = kwargs.get('ticker')
        self.values['shares'] = kwargs.get('shares')

    def __repr__(self):
        msg = '<Positions pk:{pk}, username:{username}, ticker:{ticker}, shares:{shares}>'
        return msg.format(**self.values)

    @classmethod
    def all_with_username(cls, username):
        '''return all Position rows with account_pk (username is foreign key in this db)'''
        return cls.all_from_where_clause('WHERE username = ?', (username,))


if __name__ == "__main__":
    pass
    # table = Position()
    # table.create_table()
    # transaction = Position(username = 'test_position', ticker = 'GOOGL', shares = 10)
    # transaction.save()
    # find_position = Position.one_from_where_clause('WHERE ticker = ? AND username = ?',('GOOGL', 'test_position'))
    # positions = Position()
    # print(positions.all_with_username('test_position'))
    # print(find_position)