#%% 0. Imports and config
#update system path
import os
import sys
wd = os.path.dirname(__file__) 
os.chdir(wd)
if wd in sys.path:
    sys.path.insert(0, wd)

#imports. Variables have been imported R style rather than with the config parser(less verbose)
#from statsmodels.tsa.stattools import adfuller
import pandas as pd
import numpy as np
import ta
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from scipy.stats import pearsonr
from scipy.stats import ttest_ind
#%% Get Data if needed
spy_path = "C:/Users/malha/Documents/Data/SP500-EDA/spy1d.csv"
df = yf.download("^GSPC", period="max", interval = "1d", threads = 'True')
df = df.reset_index().replace([np.inf, -np.inf], np.nan)
df['Change'] = df['Close'].shift(-1)/df['Open'].shift(-1)
#df['Change'] = df['Close']/df['Close'].shift(-1)
df = df[df['Date'] >= "20/04/1982"]
df.to_csv(spy_path, index = False)

#%% #Load data
spy_path = "C:/Users/malha/Documents/Data/SP500-EDA/spy1d.csv"
data = pd.read_csv(spy_path)
#data['Change'] = df['Close'].shift(-1)/df['Close']
#split into train and test
df = data.head(round(len(df)*0.75))
df_test = data.tail(round(len(df)*0.25))
#%% testing
# df2= ta.add_all_ta_features(
#     df, open="Open", high="High", low="Low", close="Close", volume="Volume")


# bins = [-np.inf, 0.98, 0.995, 1.005, 1.02, np.inf]
# names = [5,4,3,2,1]
# df['target'] = pd.cut(df['Change'], bins, labels=names)
# df2 = df.corr()

#%% Binary case
# bins = [-np.inf, 1.01, np.inf]
# names = [0,1]
# df['target'] = pd.cut(df['Change'], bins, labels=names)

#%%
def level1_split(df):
    ind_list = []
    n_list = []
    p_list = []
    reverse_list = []
    return_a_list = []
    return_b_list = []
    
    
    for n in range(1,202):
        indicator = "SMA"
        df['indicator'] = ta.trend.SMAIndicator(df['Close'], window = n).sma_indicator()
        a = df[df['Close'] > df['indicator']]['Change']
        b = df[df['Close'] <= df['indicator']]['Change']
        p = ttest_ind(a, b, equal_var=False, nan_policy='omit')[1]
        ind_list.append(indicator)
        n_list.append(n)
        p_list.append(p)
        if a.product() < 1:
            a = (2 - a)
            reverse_list.append('a')
        else:
            reverse_list.append('b')
        if b.product() < 1:
            b = (2 - b)
        a_return = a.product()
        b_return = b.product()
        return_a_list.append(a_return)
        return_b_list.append(b_return)
        
            
        indicator = "EMA"
        df['indicator'] = ta.trend.EMAIndicator(df['Close'], window = n).ema_indicator()
        a = df[df['Close'] > df['indicator']]['Change']
        b = df[df['Close'] <= df['indicator']]['Change']
        p = ttest_ind(a, b, equal_var=False, nan_policy='omit')[1]
        ind_list.append(indicator)
        n_list.append(n)
        p_list.append(p)
        if a.product() < 1:
            a = (2 - a)
            reverse_list.append('a')
        else:
            reverse_list.append('b')
        if b.product() < 1:
            b = (2 - b)
        a_return = a.product()
        b_return = b.product()
        return_a_list.append(a_return)
        return_b_list.append(b_return)
        
        indicator = "Aroon"
        df['indicator'] = ta.trend.AroonIndicator(df['Close'], df['Low'], window = n, fillna = True).aroon_up() - ta.trend.AroonIndicator(df['Close'], df['Low'], window = n, fillna = True).aroon_down()
        a = df[df['indicator'] >= 0]['Change']
        b = df[df['indicator'] < 0]['Change']
        p = ttest_ind(a, b, equal_var=False, nan_policy='omit')[1]
        mean_diff = abs(a.mean() - b.mean())
        ind_list.append(indicator)
        n_list.append(n)
        p_list.append(p)
        if a.product() < 1:
            a = (2 - a)
            reverse_list.append('a')
        else:
            reverse_list.append('b')
        if b.product() < 1:
            b = (2 - b)
        a_return = a.product()
        b_return = b.product()
        return_a_list.append(a_return)
        return_b_list.append(b_return)
        
        indicator = "ADX"
        df['indicator'] = ta.trend.ADXIndicator(df['High'], df['Low'], df['Close'], window = n).adx_pos() - ta.trend.ADXIndicator(df['High'], df['Low'], df['Close'], window = n).adx_neg()
        a = df[df['indicator'] >= 0]['Change']
        b = df[df['indicator'] < 0]['Change']
        p = ttest_ind(a, b, equal_var=False, nan_policy='omit')[1]
        mean_diff = abs(a.mean() - b.mean())
        ind_list.append(indicator)
        n_list.append(n)
        p_list.append(p)
        if a.product() < 1:
            a = (2 - a)
            reverse_list.append('a')
        else:
            reverse_list.append('b')
        if b.product() < 1:
            b = (2 - b)
        a_return = a.product()
        b_return = b.product()
        return_a_list.append(a_return)
        return_b_list.append(b_return)
        
        indicator = "ATR"
        df['indicator'] = ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close'], window = n).average_true_range()
        a = df[(df['High'] - df['Low']) > df['indicator']]['Change']
        b = df[(df['High'] - df['Low']) <= df['indicator']]['Change']
        p = ttest_ind(a, b, equal_var=False, nan_policy='omit')[1]
        mean_diff = abs(a.mean() - b.mean())
        ind_list.append(indicator)
        n_list.append(n)
        p_list.append(p)
        if a.product() < 1:
            a = (2 - a)
            reverse_list.append('a')
        else:
            reverse_list.append('b')
        if b.product() < 1:
            b = (2 - b)
        a_return = a.product()
        b_return = b.product()
        return_a_list.append(a_return)
        return_b_list.append(b_return)
        
        indicator = "BBandU"
        for sd in [0.5,1,1.5,2,2.5,3]:
            df['indicator'] = ta.volatility.BollingerBands(df['Close'], window = n, window_dev = sd).bollinger_hband()
            a = df[df['indicator'] >= df['Close']]['Change']
            b = df[df['indicator'] < df['Close']]['Change']
            p = ttest_ind(a, b, equal_var=False, nan_policy='omit')[1]
            mean_diff = abs(a.mean() - b.mean())
            ind_list.append(f'{indicator}{sd}')
            n_list.append(n)
            p_list.append(p)
            if a.product() < 1:
                a = (2 - a)
                reverse_list.append('a')
            else:
                reverse_list.append('b')
            if b.product() < 1:
                b = (2 - b)
            a_return = a.product()
            b_return = b.product()
            return_a_list.append(a_return)
            return_b_list.append(b_return)
        
        indicator = "BBandL"
        for sd in [0.5,1,1.5,2,2.5,3]:
            df['indicator'] = ta.volatility.BollingerBands(df['Close'], window = n, window_dev = sd).bollinger_lband()
            a = df[df['indicator'] <= df['Close']]['Change']
            b = df[df['indicator'] > df['Close']]['Change']
            p = ttest_ind(a, b, equal_var=False, nan_policy='omit')[1]
            mean_diff = abs(a.mean() - b.mean())
            ind_list.append(f'{indicator}{sd}')
            n_list.append(n)
            p_list.append(p)
            if a.product() < 1:
                a = (2 - a)
                reverse_list.append('a')
            else:
                reverse_list.append('b')
            if b.product() < 1:
                b = (2 - b)
            a_return = a.product()
            b_return = b.product()
            return_a_list.append(a_return)
            return_b_list.append(b_return)
        
        indicator = "NowvsxDaysAgo"
        df['indicator'] = df['Close'] > df['Close'].shift(n)
        a = df[df['indicator'] >= 0]['Change']
        b = df[df['indicator'] < 0]['Change']
        p = ttest_ind(a, b, equal_var=False, nan_policy='omit')[1]
        mean_diff = abs(a.mean() - b.mean())
        ind_list.append(indicator)
        n_list.append(n)
        p_list.append(p)
        if a.product() < 1:
            a = (2 - a)
            reverse_list.append('a')
        else:
            reverse_list.append('b')
        if b.product() < 1:
            b = (2 - b)
        a_return = a.product()
        b_return = b.product()
        return_a_list.append(a_return)
        return_b_list.append(b_return)
    
    summary = pd.DataFrame({'indicator':ind_list, 'n': n_list, 'p': p_list, 'reverse':reverse_list,
                               'return_a': return_a_list, 'return_b': return_b_list})
    summary['total_return'] = summary['return_a'] + summary['return_b']
    return summary

#%% - Find Criterion for level 1 split
test = level1_split(df)
test = test[test['p'] <= 0.05]
#Based on this, we see that BBandUpper 1.5, n=11 can slightly improve returns.
#If the close is above this indicator, buy. Otherwise, short sell. Lets test this
#%% - Test Level 1 split
def level1_test(df):
    #1. Add sma indicator
    df['indicator'] = ta.volatility.BollingerBands(df['Close'], window = 11, window_dev = 1.5).bollinger_hband()
    #2. Drop nas
    df = df.dropna()
    #3. Turn indicator col into a binary flag, 1 = by, 0 = sell
    df['indicator'] = df['Close'] <= df['indicator']
    #4. make column for expected return
    df['return'] =  np.where(df['indicator'] == 1, df['Change'], (2 - df['Change']))
    #5. add trading cost
    #df['return'] = df['return'] - 0.001 #0.1% daily fee, FXCM has 0.001 ie 0.01%
    #6. Make cumulative
    df['Hold'] = df['Change'].cumprod()
    df['Trade'] = df['return'].cumprod()
    df = df[['Date', 'Hold', 'Trade']]
    return df
                                                                            
    
results = level1_test(df_test)


#%%
df['indicator'] = ta.volatility.BollingerBands(df['Close'], window = 14, window_dev = 3).bollinger_hband()
df['direction'] = df['indicator'] <= df['Close']
df['direction'].value_counts()
#%%
df['indicator'] = ta.trend.SMAIndicator(df['Close'], window = 2).sma_indicator()
df1 = df[df['Close'] > df['indicator']]
df2 = df[df['Close'] <= df['indicator']]

df1_summary = MA_splitter(df1)
df2_summary = MA_splitter(df2)
#%%
# Initialize Bollinger Bands Indicator
indicator_bb = BollingerBands(close=df["Close"], window=20, window_dev=2)

# Add Bollinger Bands features
df['bb_bbm'] = indicator_bb.bollinger_mavg()
df['bb_bbh'] = indicator_bb.bollinger_hband()
df['bb_bbl'] = indicator_bb.bollinger_lband()


ta.momentum.StochRSIIndicator(close: pandas.core.series.Series, window: int = 14, smooth1: int = 3, smooth2: int = 3, fillna: bool = False)
ta.momentum.PercentageVolumeOscillator(volume: pandas.core.series.Series, window_slow: int = 26, window_fast: int = 12, window_sign: int = 9, fillna: bool = False)
ta.momentum.WilliamsRIndicator(high: pandas.core.series.Series, low: pandas.core.series.Series, close: pandas.core.series.Series, lbp: int = 14, fillna: bool = False)
ta.volatility.AverageTrueRange(high: pandas.core.series.Series, low: pandas.core.series.Series, close: pandas.core.series.Series, window: int = 14, fillna: bool = False)
ta.volatility.BollingerBands(close: pandas.core.series.Series, window: int = 20, window_dev: int = 2, fillna: bool = False)
ta.volatility.DonchianChannel(high: pandas.core.series.Series, low: pandas.core.series.Series, close: pandas.core.series.Series, window: int = 20, offset: int = 0, fillna: bool = False)
ta.volatility.KeltnerChannel(high: pandas.core.series.Series, low: pandas.core.series.Series, close: pandas.core.series.Series, window: int = 20, window_atr: int = 10, fillna: bool = False, original_version: bool = True, multiplier: int = 2)
ta.volatility.UlcerIndex(close: pandas.core.series.Series, window: int = 14, fillna: bool = False)
ta.trend.AroonIndicator(close: pandas.core.series.Series, window: int = 25, fillna: bool = False)
ta.trend.EMAIndicator(close: pandas.core.series.Series, window: int = 14, fillna: bool = False)
ta.trend.IchimokuIndicator(high: pandas.core.series.Series, low: pandas.core.series.Series, window1: int = 9, window2: int = 26, window3: int = 52, visual: bool = False, fillna: bool = False)
ta.trend.MACD(close: pandas.core.series.Series, window_slow: int = 26, window_fast: int = 12, window_sign: int = 9, fillna: bool = False)
ta.trend.PSARIndicator(high: pandas.core.series.Series, low: pandas.core.series.Series, close: pandas.core.series.Series, step: float = 0.02, max_step: float = 0.2, fillna: bool = False)
ta.trend.SMAIndicator(close: pandas.core.series.Series, window: int, fillna: bool = False)
ta.trend.WMAIndicator(close: pandas.core.series.Series, window: int = 9, fillna: bool = False)
ta.trend.adx(high, low, close, window=14, fillna=False)
