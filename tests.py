import pandas as pd
import sqlite3
import yfinance as yf



conn = sqlite3.connect('stocks.db')

data = pd.read_sql_query('SELECT * FROM stockNames', conn)

print(data)