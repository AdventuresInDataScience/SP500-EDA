# %% 0. Imports and config
# update system path
import os
import sys

wd = os.path.dirname(__file__)
os.chdir(wd)
if wd in sys.path:
    sys.path.insert(0, wd)

# imports. Variables have been imported R style rather than with the config parser(less verbose)
# from statsmodels.tsa.stattools import adfuller
import pandas as pd
import numpy as np
import ta
import matplotlib.pyplot as plt
import seaborn as sns
# from config import *
# from functions.data_functions import *

# %% 1. Load Data
# 1. Load
stocks_path = "C:/Users/malha/Documents/Data/SP500-EDA/stocks__1w.parquet.gzip"
etf_path = "C:/Users/malha/Documents/Data/SP500-EDA/etf__1w.parquet.gzip"

etf_data = pd.read_parquet(etf_path)
stock_data = pd.read_parquet(stocks_path)
# 2. Trim to 1995 and later
df = stock_data[stock_data["Date"] >= "1995"]
etf = etf_data[etf_data["Date"] >= "1999"]

# %% A quick check shows that many stocks are not really stocks - the data is unclear :-(
# f['Ticker'] = df.groupby(['Ticker'])['High'].rolling(1).max().reset_index(0,drop=True)
"""
my_DataFrame.groupby(['AGGREGATE']).agg({'MY_COLUMN': [q50, q90, 'max']})
"""


def q50(x):
    return x.quantile(0.5)


# 90th Percentile
def q25(x):
    return x.quantile(0.25)


def cwgr(x):
    return x.prod() ** (1 / len(x))


mean_change_df = (
    df[["Ticker", "change"]]
    .groupby(["Ticker"])
    .agg(
        mean_change=("change", np.mean),
        std=("change", np.std),
        med_change=("change", q50),
        change_25=("change", q25),
        minimum=("change", np.min),
        maximum=("change", np.max),
        tot_return=("change", np.sum),
        cwr=("change", cwgr),
        ret=("change", np.sum),
    )
)


# %% - Having a look at etfs in the same way
def q50(x):
    return x.quantile(0.5)


# 90th Percentile
def q25(x):
    return x.quantile(0.25)


def cwgr(x):
    return x.prod() ** (1 / len(x))


mean_change_df = (
    etf[["Ticker", "change"]]
    .groupby(["Ticker"])
    .agg(
        mean_change=("change", np.mean),
        std=("change", np.std),
        med_change=("change", q50),
        change_25=("change", q25),
        minimum=("change", np.min),
        maximum=("change", np.max),
        tot_return=("change", np.sum),
        cwr=("change", cwgr),
        ret=("change", np.sum),
    )
    .reset_index()
)

pivot_df = etf.pivot_table(index="Date", columns="Ticker", values="change").corr()
sns.heatmap(pivot_df, cmap="PiYG")

# This shows all the ETFs are correlated, with XLY and XLK slightly less than many others
# XLU has lower correlations than any other, but also one of the lowest average changes

# %% -
