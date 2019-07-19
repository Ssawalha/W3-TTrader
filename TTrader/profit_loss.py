import sqlite3
dbname = 'ttrader.db'
dbpath = __file__


#write a program that uses sqlite3 and hard-coded sql statement
#to calculate the P&L of ticker for a user
#do not use orm for this excersize

def get_buy_market_value(username, ticker):
    SQL = '''SELECT * FROM trades WHERE username = ? AND ticker = ?'''
    # values = #
