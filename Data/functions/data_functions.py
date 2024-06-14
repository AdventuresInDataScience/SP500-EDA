from statsmodels.tsa.stattools import adfuller
import pandas as pd
import numpy as np
import yfinance as yf
from fredapi import Fred
import pandas_ta as ta


"""
    stocks['Date'] = pd.to_datetime(stocks['Date'])
    stocks['DayofWeek'] = stocks['Date'].dt.dayofweek
    stocks['Month'] = stocks['Date'].dt.month

"""
