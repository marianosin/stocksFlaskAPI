from aplication import app
from flask import render_template
from flask import g
from flask import request
import pandas as pd

import sqlite3


# To use SQLite it is necesary to create a connection to the database using Flask tools
@app.before_request
def before_request():
    g.conn = sqlite3.connect('stocks.db')

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'conn'):
        g.conn.close()
# Define the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        if symbol:
            data = pd.read_sql_query("SELECT * FROM stockNames WHERE symbol LIKE '%{}%'".format(symbol), g.conn)
        else:
            data = pd.read_sql_query("SELECT * FROM stockNames", g.conn)
    else:
        data = pd.read_sql_query("SELECT * FROM stockNames", g.conn)

    return render_template('index.html', title='Stocks stored in DB', table=data)

# Route for more info with each symbol
@app.route('/stock/<symbol>')
def stock(symbol):
    # read database table stockName
    data = pd.read_sql_query("SELECT * FROM stockNames WHERE symbol = '{}'".format(symbol), g.conn)

    return data.drop('stockId', axis = 1).T[0].to_json(orient='columns')
@app.route('/prices/<symbol>/<startD>/<endD>')
def prices(symbol, startD = None, endD = None):
    # read database table stockName
    data = pd.read_sql_query("SELECT * FROM stockNames WHERE symbol = '{}'".format(symbol), g.conn)
    #stockId = data.T.to_json(orient='columns')
    stockId = data.T[0].to_dict()['stockId']

    data = pd.read_sql_query("SELECT * FROM stockPrices WHERE stockId = {} ;".format(stockId), g.conn)
    data['date'] = pd.to_datetime(data['date'])
    if startD is not None and endD is not None:
        data = data[(data['date'] >= startD) & (data['date'] <= endD)]
    data = data.drop('stockId', axis = 1)
    data = data.T
    data.columns = list(range(len(data.columns)))
    return {'stockId': stockId, 'symbol': symbol, 'startD': startD, 'endD': endD, 'data': data.to_dict()}
@app.route('/prices/<symbol>')
def fullPrices(symbol):
    # read database table stockName
    data = pd.read_sql_query("SELECT * FROM stockNames WHERE symbol = '{}'".format(symbol), g.conn)
    #stockId = data.T.to_json(orient='columns')
    stockId = data.T[0].to_dict()['stockId']

    data = pd.read_sql_query("SELECT * FROM stockPrices WHERE stockId = {} ;".format(stockId), g.conn)

    data = data.drop('stockId', axis = 1)
    data = data.T
    data.columns = list(range(len(data.columns)))
    return {'stockId': stockId, 'symbol': symbol, 'startD': None, 'endD': None, 'data': data.to_dict()}

@app.route('/layout')
def layout():
    return  render_template('layout.html')

# Documentation of API
@app.route('/documentation')
def documentation():
    return  {
        '/': 'List of stocks stored in the database',
        '/stock/<symbol>': 'Information about a stock',
        '/prices/<symbol>': 'All prices of a stock',
        '/prices/<symbol>/<startD>/<endD>': 'Prices of a stock in a range of dates',
        'Created by': 'Mariano Radusky'

    }