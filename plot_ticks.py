import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc

import numpy as np
import pandas as pd
import urllib
import datetime as dt
import os
import tick_file_helper as tfh

# assumes usec could be present
def parse_time(time_str):

    if '.' in time_str:
        time_str_split, us_str = time_str.split('.')
        t = dt.datetime.strptime(time_str_split, '%Y-%m-%d %H:%M:%S')
        return t
    else:
        return dt.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

# plot_ohlc_range
def plot_tick_range(tick_path, range_start, range_end):

    if os.path.exists(tick_path) == False:
        print(tick_path + ' file doesnt exist')
        
        quit()

    date_cols = ['RateDateTime']

    df = pd.read_csv(tick_path, usecols=['RateDateTime','RateBid','RateAsk'])

    start_index = tfh.find_index_closest_date(range_start, tick_path)
    end_index = tfh.find_index_closest_date(range_end, tick_path)

    # dont proceed if we didnt find indices
    if (start_index is None or end_index is None):
        print('start_index or end_index was None')
        quit()

    ticks_s = df.iloc[start_index:end_index]

    ticks = (ticks_s['RateAsk'] + ticks_s['RateBid']) / 2.0

    dates_dt = [dt.datetime.strptime(str.split(x, '.')[0], '%Y-%m-%d %H:%M:%S') for x in ticks_s['RateDateTime'].values]

    dates = mdates.date2num(dates_dt)

    #fig = plt.figure()
    #ax1 = plt.subplot2grid((1,1), (0,0))

    plt.plot_date(dates, ticks, 'b-')

    # candlestick_ohlc(ax1, ohlc, width=0.0004, colorup='#77d879', colordown='#db3f3f')

    # for label in ax1.xaxis.get_ticklabels():
    #     label.set_rotation(45)

    # ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    # ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    # ax1.grid(True)
    

    # plt.xlabel('Date')
    # plt.ylabel('Price')
    # plt.title(ohlc_path)
    # plt.legend()
    # plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    #plt.show()

    # plot_ohlc_range
def plot_tick_range_normalised(tick_path, range_start, range_end):

    if os.path.exists(tick_path) == False:
        print(tick_path + ' file doesnt exist')
        
        quit()

    date_cols = ['RateDateTime']

    df = pd.read_csv(tick_path, usecols=['RateDateTime','RateBid','RateAsk'])

    start_index = tfh.find_index_closest_date(range_start, tick_path)
    end_index = tfh.find_index_closest_date(range_end, tick_path)

    # dont proceed if we didnt find indices
    if (start_index is None or end_index is None):
        print('start_index or end_index was None')
        quit()

    ticks_s = df.iloc[start_index:end_index]

    ticks = ((ticks_s['RateAsk'] + ticks_s['RateBid']) / 2.0)

    ticks_norm = (ticks - ticks.min()) / (ticks.max() - ticks.min())

    dates_dt = [dt.datetime.strptime(str.split(x, '.')[0], '%Y-%m-%d %H:%M:%S') for x in ticks_s['RateDateTime'].values]

    dates = mdates.date2num(dates_dt)

    plt.plot_date(dates, ticks_norm, 'b-')


