# lead lag

import os
import zipfile
import tempfile
import sys
import csv
import pandas as pd
import numpy as np
import datetime
import math
import random
import time
import plot_ticks
import tick_file_helper
import matplotlib.pyplot as plt

dir = '/Users/P/Documents/Prices/2015'

file1 = '/Users/P/Documents/Prices/2015/EUR_USD/January/EUR_USD_Week1.csv'
file2 = '/Users/P/Documents/Prices/2015/USD_JPY/January/USD_JPY_Week1.csv'
file3 = '/Users/P/Documents/Prices/2015/EUR_JPY/January/EUR_JPY_Week1.csv'

# find the middle of the first file
file1_set = pd.read_csv(file1)
file2_set = pd.read_csv(file2)

l = 6050#len(file1_set) / 2

middle_date_str = file1_set['RateDateTime'][l]
middle_dt = datetime.datetime.strptime(middle_date_str.split(".")[0], '%Y-%m-%d %H:%M:%S')

middle_dt_end = middle_dt + datetime.timedelta(minutes=2)




# plt.subplot(3, 1, 1)
# plt.title(str(file1))
# plot_ticks.plot_tick_range(file1, middle_dt, middle_dt_end)


# plt.subplot(3, 1, 2)
# plt.title(str(file2))
# plot_ticks.plot_tick_range(file2, middle_dt, middle_dt_end)


# plt.subplot(3, 1, 3)
# plt.title(str(file3))
# plot_ticks.plot_tick_range(file3, middle_dt, middle_dt_end)

# plt.show()



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






