import os
import sqlite3
from orm import ORM
from account import Account
from trade import Trade
from position import Position
import util
import view as v


def start():
    selection = 0
    while selection != 3:
        selection = v.mainmenu()

        if selection == 1: #Create Account
            user_name, pword_hash = v.create_account()
            new_account = Account(username = user_name, password_hash = pword_hash, balance = 10000) #make it so that unique username
            new_account.save()
            v.create_acc_success(new_account.values['username'])


        elif selection == 2: #Log In
            user_name, pword_hash = v.login_credentials()
            account = Account()
            activated = account.login(username = user_name, password = pword_hash)

            if account != None:
                login_selection = 0
                while login_selection != 6:
                    login_selection = v.account_options(activated.values['username'])

                    if login_selection == 1: #Check Balance
                        v.show_balance(activated.values['balance'])

                    elif login_selection == 2:#check all stocks in portfolio
                        v.show_portfolio(activated)

                    elif login_selection == 3:#check 1 stock in portfolio
                        v.show_position(activated)

                    elif login_selection == 4:#buy stocks
                        # v.buy_stock(activated)
                        ticker, amount = v.choose_stock()
                        confirm_purchase = v.confirm_purchase()
                        # shares = v.shares()


                    elif login_selection == 5:#sell stocks
                        pass
            else:
                print("INVALID CREDENTIALS/LOGIN ERROR")###remove/change later
        
if __name__ == "__main__":
    start()


