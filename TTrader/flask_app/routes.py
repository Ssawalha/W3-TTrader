#!/usr/bin/env python3

from flask import request, jsonify
from flask_app.app import app
from model.util import lookup_price
from model.util import hash_password
from model.account import Account

@app.route('/')
def home():
    return jsonify({'Welcome to':'TTrader api'})

@app.route('/api/create_account', methods=['POST'])
def create_account():
    if not request.json:
        return jsonify({'error':'bad request'}), 400
    if 'username' not in request.json or 'password' not in request.json or 'firstname' not in request.json or 'lastname' not in request.json:
        return jsonify({'error':'bad request'}), 400
    
    username = request.json['username']
    password = request.json['password']
    first = request.json['firstname']
    last = request.json['lastname']

    uniqueUsername = Account().username_preventduplicate(username)
    if uniqueUsername == None:
        new_account = Account(username=username, balance=0, first = first, last = last)
        new_account.set_password(password)
        new_account.generate_api_key()
        new_account.save()
        return jsonify({"Your account was created successfully.":"You start with a balance of $0.00"},{"Your api key is":new_account.values['api_key']})
    else:
        return jsonify({"error":"bad username"})

@app.route('/api/get_api_key', methods=['POST'])
def get_api_key():
    if not request.json:
        return jsonify({'error':'bad request'}), 400
    if 'username' not in request.json or 'password' not in request.json:
        return jsonify({'error':'bad request'}), 400
    username = request.json['username']
    password = request.json['password']
    print(username, password)
    logged_in = Account.login(username, password)
    if logged_in != None:
        return jsonify({"api_key":logged_in.values['api_key']})
    else:
        return jsonify({"error":"404"})

@app.route('/api/get_ticker_price/<ticker>', methods=['GET'])
def get_ticker_price(ticker):
    ticker_price = lookup_price(ticker)
    return jsonify({'price': ticker_price})

@app.route('/api/<api_key>', methods=['GET'])
def get_account_info(api_key):
    api_login_attempt = Account.api_authenticate(api_key)
    if api_login_attempt != None:
        return jsonify({"username": api_login_attempt.values['username'], "balance":api_login_attempt.values['balance'], "first_name": api_login_attempt.values['first'], "last_name": api_login_attempt.values['last']})
    else:
        return jsonify({"error":"404"})

@app.route('/api/<api_key>/balance', methods=['GET'])
def get_balance(api_key):
    api_login_attempt = Account.api_authenticate(api_key)
    if api_login_attempt != None:
        return jsonify(({'balance':api_login_attempt.values['balance']}))
    else:
        return jsonify({"error":"404"})

@app.route('/api/<api_key>/positions',methods=['GET'])
def get_positions(api_key):
    api_login_attempt = Account.api_authenticate(api_key)
    if api_login_attempt != None:
        positions = api_login_attempt.get_positions()
        return jsonify({"positions":[position.json() for position in positions]}) #should i remove pk from response?
    else:
        return jsonify({"error":"404"})

@app.route('/api/<api_key>/positions/<ticker>')
def get_positions_for(api_key, ticker):
    api_login_attempt = Account.api_authenticate(api_key)
    if api_login_attempt != None:
        positions = api_login_attempt.trades_for(ticker)
        return jsonify({"positions":[position.json() for position in positions]}) #should i remove pk from response? YES
    else:
        return jsonify({"error":"404"})

@app.route('/api/<api_key>/trades')
def get_trades(api_key):
    api_login_attempt = Account.api_authenticate(api_key)
    if api_login_attempt != None:
        trades = api_login_attempt.get_trades()
        return jsonify({"trades":[trade.json() for trade in trades]}) #should i remove pk from response? YES
    else:
        return jsonify({"error":"404"})

@app.route('/api/<api_key>/trades/<ticker>')
def get_trades_for(api_key, ticker):
    api_login_attempt = Account.api_authenticate(api_key)
    if api_login_attempt != None:
        trades = api_login_attempt.trades_for(ticker)
        return jsonify({"trades":[trade.json() for trade in trades]}) #should i remove pk from response? YES
    else:
        return jsonify({"error":"404"})

@app.route('/api/<api_key>/deposit', methods=['PUT'])
def put_deposit(api_key):
    api_login_attempt = Account.api_authenticate(api_key)   
    if not request.json:
        return jsonify({'error':'bad request'}), 400 
    if 'deposit' not in request.json:
    #if 'deposit' in request.json and type(request.json['deposit']) != bytes:
        return jsonify({'error':'bad request'}), 400 
    if api_login_attempt != None:
        current_bal = api_login_attempt.values['balance']
        new_bal = current_bal + float(request.json['deposit'])
        api_login_attempt.values['balance'] = new_bal
        api_login_attempt.save()
        return jsonify({'balance':api_login_attempt.values['balance']})

@app.route('/api/<api_key>/sell', methods=['POST'])
def sell_stock(api_key):
    api_login_attempt = Account.api_authenticate(api_key)   
    if not request.json:
        return jsonify({'error':'bad request'}), 400     
    if 'ticker' not in request.json or 'shares' not in request.json:
        return jsonify({'error':'bad request'}), 400
    ticker = request.json['ticker']
    shares = request.json['shares']
    
    api_login_attempt.sell(ticker, shares)

    new_position = api_login_attempt.get_position_for(ticker)
    return jsonify({"sale successful, new position is":new_position.json()})
 

@app.route('/api/<api_key>/buy', methods=['POST']) #buy and sell should return a json {"ticker":aapl, "shares":INTEGER}
def buy_stock(api_key):
    api_login_attempt = Account.api_authenticate(api_key)   
    if not request.json:
        return jsonify({'error':'bad request'}), 400     
    if 'ticker' not in request.json or 'shares' not in request.json:
        return jsonify({'error':'bad request'}), 400
    ticker = request.json['ticker']
    shares = request.json['shares']
    
    api_login_attempt.buy(ticker, shares)

    new_position = api_login_attempt.get_position_for(ticker)
    return jsonify({"purchase successful, new position is":new_position.json()})

@app.route('/api/<api_key>/checking_account_number', methods=['GET'])
def get_checking_account_number(api_key):
    api_login_attempt = Account.api_authenticate(api_key)
    if api_login_attempt != None:
        return jsonify(({'checking_account_number':api_login_attempt.values['checking_account_number']}))
    else:
        return jsonify({"error":"404"})

@app.route('/api/<api_key>/routing_number', methods=['GET'])
def get_routing_number(api_key):
    api_login_attempt = Account.api_authenticate(api_key)
    if api_login_attempt != None:
        return jsonify(({'routing_number':api_login_attempt.values['routing_number']}))
    else:
        return jsonify({"error":"404"})

@app.route('/api/<api_key>/settings/checking_account_number', methods=['PUT'])
def set_checking_account_number(api_key):
    api_login_attempt = Account.api_authenticate(api_key)
    if not request.json:
        return jsonify({'error':'bad request'}), 400
    if 'set_checking_account_number' not in request.json:
        return jsonify({'error':'bad request'}), 400
    if api_login_attempt != None:
        api_login_attempt.set_checking_account_number(request.json['set_checking_account_number'])
        return jsonify({'checking_account_number':api_login_attempt.values['checking_account_number']})

@app.route('/api/<api_key>/settings/routing_number', methods=['PUT'])
def set_routing_number(api_key):
    api_login_attempt = Account.api_authenticate(api_key)
    if not request.json:
        return jsonify({'error':'bad request'}), 400
    if 'set_routing_number' not in request.json:
        return jsonify({'error':'bad request'}), 400
    if api_login_attempt != None:
        api_login_attempt.set_routing_number(request.json['set_routing_number'])
        return jsonify({'routing_number':api_login_attempt.values['routing_number']})





#pep3333 --> wsgi | uwhiskey --> uses binary language (not py)
#using nginx instead of apache (open-source and free, apache is bad for scaling will crash after 10k users at the same time)

#swap reassign some requests from RAM to disk temporarily 

#ADD UNIT TESTS FOR ALL ROUTES

#CRON --> linux scheduler to check for updates and run codes at certain times 
#^ good to test that your flask app is running

#selenium will move the mouse and click on shit for you --> can do "headless" as well

#push to github prior to deploying