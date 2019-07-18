""" ! [rejected]        master -> master (fetch first)
error: failed to push some refs to 'git@github.com:Ssawalha/W3-TTrader.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes
hint: (e.g., 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
"""


import os
import sqlite3

from model import orm
from model import account as a
from model import trade as t
from model import position as p
from model import util
from terminal_app import view as v

def start():
    selection = 0
    while selection != 3:
        selection = v.mainmenu()

        if selection == 1: #Create Account
            user_name, password = v.create_account() #fix with try and except
            new_account = a.Account(username = user_name, balance = 10000) #make it so that unique username | default bal of 10k
            new_account.set_password(password)
            new_account.save()
            v.create_acc_success(new_account.values['username'])

        elif selection == 2: #Log In
            user_name, pword_hash = v.login_credentials()
            account = a.Account()
            activated = account.login(username = user_name, password = pword_hash)

            if account != None:
                login_selection = 0
                while login_selection != 6:
                    login_selection = v.account_options(activated.values['username'])

                    if login_selection == 1: #Check Balance
                        v.show_balance(activated.values['balance'])

                    elif login_selection == 2:#check all stocks in portfolio
                        v.show_portfolio(activated.get_positions())

                    elif login_selection == 3:#check trade history
                        v.show_all_trades(activated.get_trades()) #<-- change

                    elif login_selection == 4:#buy stocks
                        # v.buy_stock(activated)
                        ticker = v.choose_stock()
                        try:
                            ticker_price = util.lookup_price(ticker)
                        except:
                            v.invalid_ticker()
                            raise KeyError
                        amount = v.num_of_shares(ticker, ticker_price)
                        amount = int(amount)
                        balance_before = activated.values['balance']
                        total = (amount * ticker_price)
                        if balance_before < ticker_price * amount:
                            v.insufficient_funds()
                        else:
                            confirmation = v.confirm(ticker, amount, total)
                            if confirmation == 'Y' or confirmation == 'y':
                                activated.buy(ticker, amount)
                                if (balance_before - total) == activated.values['balance']:
                                    v.purchase_success()

                    elif login_selection == 5:#sell stocks
                        ticker = v.choose_stock()
                        try:
                            ticker_price = util.lookup_price(ticker)
                        except:
                            v.invalid_ticker() 
                            raise KeyError

                        amount = v.num_of_shares(ticker, ticker_price)
                        amount = int(amount)
                        balance_before = activated.values['balance']
                        total = (amount * ticker_price)
                        if activated.get_position_for(ticker)['shares'] == 0: #look for ticker
                            v.insufficient_shares() #Ticker not found.
                        else:
                            confirmation = v.confirm(ticker, amount, total)
                            if confirmation == 'Y' or confirmation == 'y':
                                activated.sell(ticker, amount)
                                if (balance_before + total) == activated.values['balance']:
                                    v.sale_success()
            else:
                print("INVALID CREDENTIALS/LOGIN ERROR")###remove/change later


