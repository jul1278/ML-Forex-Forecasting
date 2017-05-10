import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.mpl_finance import candlestick_ohlc

import numpy as np
import pandas as pd
import urllib
import datetime as dt
import os

# convert
def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter

# plot_ohlc_range
def plot_ohlc_range(ohlc_path, range_start, range_end):

    if os.path.exists(ohlc_path) == False:
        print(ohlc_path + ' file doesnt exist')
        
        quit()

    ohlc = []
    df = pd.read_csv(ohlc_path, converters={0: bytespdate2num('%Y-%m-%d %H:%M:%S')})
    open_times = pd.read_csv(ohlc_path, usecols=['open_time'])
    
    for index, row in df.iterrows():
        open_time_unix = row['open_time']

        # get the open time string from the unconverted dataframe
        open_time_str = open_times['open_time'].iloc[index]
        open_time = dt.datetime.strptime(open_time_str, '%Y-%m-%d %H:%M:%S')

        if (open_time > range_start) and (open_time < range_end):
            append_row = row['open_time'], row['open_price'], row['high_price'],row['low_price'],row['close_price']
            ohlc.append(append_row)


    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))

    candlestick_ohlc(ax1, ohlc, width=0.0004, colorup='#77d879', colordown='#db3f3f')

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.grid(True)
    

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(ohlc_path)
    plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    plt.show()
