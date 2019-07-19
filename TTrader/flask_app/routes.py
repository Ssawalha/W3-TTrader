#!/usr/bin/env python3

from flask import request, jsonify
from flask_app.app import app
from model.util import lookup_price

@app.route('/')
def home():
    return jsonify({'message':'TTrader api'})

@app.route('/ttrader/api/get_ticker_price/<ticker>')
def get_ticker_price(ticker):
    ticker_price = lookup_price(ticker)
    return jsonify({'ticker price is ': ticker_price})