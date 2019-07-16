import sqlite3
import os

DIR = os.path.dirname(__file__)
DBFILENAME = "test.db"
DBPATH = os.path.join(DIR, DBFILENAME)

########TODO Figure out UNIQUE()/FOREIGN KEY SQL syntax. update accounts/positions/trades to utilize UNIQUE & FOREIGN KEY 
def schema(dbpath=DBPATH):
    with sqlite3.connect(dbpath) as conn:
        cur = conn.cursor()
        DROPSQL = "DROP TABLE IF EXISTS {tablename};"

        cur.execute(DROPSQL.format(tablename="accounts"))

        SQL = """CREATE TABLE accounts(
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR NOT NULL,
                password_hash VARCHAR,
                balance FLOAT,
                UNIQUE(username)
            );"""

        cur.execute(SQL)

        cur.execute(DROPSQL.format(tablename="positions"))

        SQL = """CREATE TABLE positions(
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            accounts_pk INT,
            ticker VARCHAR(4) NOT NULL,
            shares INT,
            FOREIGN KEY(accounts_pk) REFERENCES accounts(pk),
            UNIQUE(accounts_pk, ticker)
            );"""

        cur.execute(SQL)

        cur.execute(DROPSQL.format(tablename="trades"))

        SQL = """CREATE TABLE trades(
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            accounts_pk INT,
            ticker VARCHAR(4) NOT NULL,
            volume INT,
            price FLOAT,
            time FLOAT,
            FOREIGN KEY(accounts_pk) REFERENCES accounts(pk)
            );"""

        cur.execute(SQL)
