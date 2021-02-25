# IMPORTS 
import os, csv
import yfinance as yf
import pandas as pd
import talib 
from flask import Flask, render_template, request, flash, redirect, jsonify
from patterns import candlestick_patterns

# CONSTANTS 
STOCK_PATH = 'datasets/daily/Stocks'
CRYPTO_PATH = 'datasets/daily/Crypto'

app = Flask(__name__)

# Home Page
@app.route('/')
def index():
    # Get Pattern entered by user
    pattern = request.args.get('candlestick_pattern', None)
    # Create empty dict to hold stocks data 
    stocks = {}
    # Open dataset     
    with open('datasets/companies.csv') as f:
        # Store Company Symbol as key in Stocks dict
        # Value is another dict containing the company name 
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}

    # If User selected a pattern
    if pattern:
        # Get list of CSV files for companies
        datafiles = os.listdir('datasets/daily/Stocks')
        # Loop through them and read each into a pandas Data Frame
        for filename in datafiles:
            dataframe = pd.read_csv(f'datasets/daily/Stocks/{filename}')
            # Get a reference to the pattern analysis function used by TA-LIB 
            pattern_function = getattr(talib, pattern)
           
            symbol = filename.split('.')[0]
            try:
                # Process data frame
                result = pattern_function(dataframe["Open"], dataframe["High"], dataframe["Low"], dataframe["Close"])
                # Get the value of the last data frame (most recent)
                last = result.tail(1).values[0]
            
                # If the value is nonzero, the dataframe triggered the pattern
                if last > 0:
                    stocks[symbol][pattern] = 'bullish'
                elif last < 0:
                    stocks[symbol][pattern] = 'bearish'
                else:
                    stocks[symbol][pattern] = None
            except:
                pass
            # Print all stock data to console 
            print(stocks)
    return render_template('index.html', candle_patterns=candlestick_patterns, stocks=stocks, current_pattern=pattern) 

# Route to grab stock, crypto data  
@app.route('/snapshot')
def snapshot():
    """Take a snapshot of the daily closes of s&p500, binance bitcoin exchange"""
    # Open list of companies and cryptos we're collect data for 
    with open('datasets/companies.csv') as f, open('datasets/cryptos.csv') as curr:
        companies = f.read().splitlines()
        cryptos = curr.read().splitlines() 
        # Extraneous data member
        companies.remove(companies[-1])
        
        # Create and loop counter 
        index = 0
        # Loop through companies and download price data from yahoo to CSV 
        for company in companies:
            symbol = company.split(',')[0]
            dataframe = yf.download(symbol, start="2021-01-01", end="2021-02-25")
            dataframe.to_csv(f'datasets/daily/Stocks/{symbol}.csv')
            # If within index of crypto list, download price data for cryptos also 
            if index < len(cryptos):
                symbol2 = cryptos[index].split(',')[0]
                dataframe = yf.download(symbol2, start="2021-01-01", end="2021-02-25")
                dataframe.to_csv(f'datasets/daily/Crypto/{symbol2}.csv')
                index += 1
    return {
        'code': 'success'
    }
