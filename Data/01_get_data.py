# %% 0. Imports and config
# update system path
import os
import sys

wd = os.path.dirname(__file__)
os.chdir(wd)
if wd in sys.path:
    sys.path.insert(0, wd)

# imports. Variables have been imported R style rather than with the config parser(less verbose)
from statsmodels.tsa.stattools import adfuller
import pandas as pd
import numpy as np
import yfinance as yf
from fredapi import Fred
import ta
from config import *
from functions.data_functions import *

# %% 1. Download all SP500 data and save

# Get object to connect to Fred API
fred = Fred(api_key=fred_key)

# make list of constituents
ticker_list, constituents = make_ticker_list()

# get weekly stock data
stocks = get_yahoo_data(ticker_list, constituents, interval="1wk")

# %% Basic Data Cleaning
stocks = clean_stocks(stocks, remove_1s=False)
# Add Basic features
# stocks = engineer_basic_features(stocks)
stocks["change"] = stocks["Close"] / stocks["Open"]
# remove OHLC columns, as these are not stationary
# stocks = stocks.drop(['Adj Close', 'Open', 'High', 'Low', 'Close', 'Volume'], axis=1)
# FINALLY THE TARGET VARIABLE ie % move for next week's stock
stocks = add_target(stocks)

# %% Indexes linked to stocks
etf_df = make_etf_data(interval="1wk")

# %% Join all data together and drop NAs
stocks["Date"] = pd.to_datetime(stocks["Date"])
etf_df["Date"] = pd.to_datetime(etf_df["Date"])

# SAVE
stocks.to_parquet(stocks_path, index=False, compression="gzip")
etf_df.to_parquet(etf_path, index=False, compression="gzip")
