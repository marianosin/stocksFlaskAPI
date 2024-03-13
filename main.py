import pandas as pd
import yfinance as yf
import sqlite3
from datetime import datetime
import time

def create_database():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect('stocks.db')

    # Create a cursor object
    c = conn.cursor()

    # Create the stockNames table
    c.execute('''
        CREATE TABLE IF NOT EXISTS stockNames (
            stocId INTEGER PRIMARY KEY,
            symbol TEXT,
            security TEXT,
            sector TEXT,
            subSector TEXT,
            headquarters TEXT,
            dateAdded TEXT,
            cik TEXT,
            founded TEXT
        )
    ''')

    # Create the stockPrices table
    c.execute('''
        CREATE TABLE IF NOT EXISTS stockPrices (
            recordId INTEGER PRIMARY KEY,
            stockId INTEGER,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            FOREIGN KEY(stockId) REFERENCES stockNames(stockId),
            UNIQUE(stockId, date)
              
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def download_sp500_companies():
    # Get the table of S&P 500 companies from Wikipedia
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    companies = table[0]
    # Rename to match db columns
    companies = companies.rename(columns={
        'Symbol': 'symbol' ,
        'Security': 'security',
        'GICS Sector': 'sector',
        'GICS Sub-Industry': 'subSector',
        'Headquarters Location': 'headquarters',
        'Date first added': 'dateAdded', 
        'CIK': 'cik', 
        'Founded': 'founded'
    })

    return companies
    
def download_stock_price(symbol):
    try:
        
        stock = yf.Ticker(symbol)
        #print(stock)
        stock = stock.history(period='max')
        
        stock = stock.reset_index()
        stock['symbol'] = symbol
        #print(stock)
        stock = stock[['Date', 'Open', 'High', 'Low', 'Close', 'Volume' , 'symbol']]
        stock.columns = ['date', 'open', 'high', 'low', 'close', 'volume',  'symbol'] #match db columns

        return stock
    except Exception as e:
        print(f'Error downloading {symbol}')
        print('Error message: ', e)
        return None

def merge_stock_price(stock, companies):
    # Merge the stock price data with the company data
    stock = stock.reset_index()
    stock = stock.merge(companies, left_on='symbol', right_on='symbol')
    stock = stock.rename(columns={'stockId': 'stockId'}).drop(columns=['symbol'])
    stock = stock[['stockId', 'date', 'open', 'high', 'low', 'close', 'volume']]
    stock['date'] = stock['date'].dt.strftime('%Y-%m-%d') #format date because sqlite3 doesn't support datetime
    return stock

def insert_stock_price(stock):
    # Connect to the SQLite database
    conn = sqlite3.connect('stocks.db')

    # Insert the stock price data
    cur = conn.cursor()
    for row in stock.itertuples(index=False):
        # As stockId and date are unique when combined, we can use INSERT OR IGNORE
        #print(row.stockId, row.date, row.open, row.high, row.low, row.close, row.volume)
        #time.sleep(0.1)
        cur.execute('''
            INSERT OR IGNORE INTO stockPrices (stockId, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (row.stockId, row.date, row.open, row.high, row.low, row.close, row.volume))
        
        #time.sleep(0.1)
    conn.commit()
    conn.close()




if __name__ == '__main__':

    #Create database if it doesn't exist
    create_database()

    companies = download_sp500_companies().reset_index().rename(columns={'index': 'stockId'})
    # update the stockNames table
    conn = sqlite3.connect('stocks.db') 

    companies.to_sql('stockNames', conn, if_exists='replace', index=False)
    conn.close()

    
    # Download the S&P 500 companies
    symbols = companies['symbol'].tolist()
    for symbol in symbols:
        stock = download_stock_price(symbol)

        if stock is not None:
            try:
                merged = merge_stock_price(stock, companies)
                #conn = sqlite3.connect('stocks.db')
                #print(merged.head())
                insert_stock_price(merged)
                #conn.close()
                print('Ticker added to database: ', symbol)
            except Exception as e:
                print('Error adding ticker to database: ', symbol)
                print('Error message: ', e)