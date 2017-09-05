# pair ratio
import numpy
import pandas as pd
import datetime as dt
import math
import random
import csv
import time
from decimal import *
import matplotlib.pyplot as plt

time_header = 'RateDateTime'
bid_header = 'RateBid'
    
datetime_index = 3
bid_index = 4
ask_index = 5 

# assumes nanoseconds could be present
def parse_time(time_str):
    if '.' in time_str:
        time_str_split, ns_str = time_str.split('.')
        t = dt.datetime.strptime(time_str_split, '%Y-%m-%d %H:%M:%S')
        ns = int(ns_str[:3])
        t = t + dt.timedelta(microseconds=(ns/1000))

        return t
    else:
        return dt.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

# price_pairs
# df1 first price assumed to occur after df2
def price_pairs(df1, df2):
    df1_index = 0
    df2_index = 0

    df1_time = df1[time_header]
    df2_time = df2[time_header]

    df1_bid = df1[bid_header]
    df2_bid = df2[bid_header]

    df1_first_time = parse_time(df1_time[0])
    df2_first_time = parse_time(df2_time[0])

    df1_next_datetime = parse_time(df1_time[df1_index + 1])
    df2_next_datetime = parse_time(df2_time[df2_index + 1])

    # if df1 first tick occurs *before* df2 then advance df2 index so that 
    # df2_index refers to the first tick chronologically before df1 first tick
    if df1_first_time > df2_first_time:

        while (df2_next_datetime < df1_first_time):
            df2_index = df2_index + 1
            df2_next_datetime = parse_time(df2_time[df2_index + 1])
            df2_first_time = parse_time(df2_time[0])

    else:

        while (df1_next_datetime < df2_first_time):
            df1_index = df1_index + 1
            df1_next_datetime = parse_time(df1_time[df1_index + 1])
            df1_first_time = parse_time(df1_time[0])

    df1_len = len(df1)
    df2_len = len(df2)

    while((df1_index + 1) < df1_len and (df2_index + 1) < df2_len):

        df1_next_datetime = parse_time(df1_time[df1_index + 1])
        df2_next_datetime = parse_time(df2_time[df2_index + 1])

        yield (df1_bid[df1_index], df2_bid[df2_index])

        if (df1_next_datetime > df2_next_datetime):
        # increment df2_index and not df1_index
            df2_index = df2_index + 1    

        else: # df1_next_datetime < df2_next_datetime
            #increment df1_index and not df2_index
            df1_index = df1_index + 1


# import_tick_csv
def import_tick_csv(filepath):
    
    csv_arr = []
    
    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        # skip header
        next(csv_reader, None)

        for row in csv_reader:
            
            dtime = parse_time(row[datetime_index])
            bid = Decimal(row[bid_index])
            ask = Decimal(row[ask_index])
            
            csv_arr.append((dtime, bid, ask))

    return csv_arr

# price_pairs
# df1 first price assumed to occur after df2
def price_pairs_csv(f1, f2):
 
    df1_index = 0
    df2_index = 0

    tick1_arr = import_tick_csv(f1)
    tick2_arr = import_tick_csv(f2)

    df1_first_time = tick1_arr[0][0]
    df2_first_time = tick2_arr[0][0]

    df1_next_datetime = tick1_arr[df1_index + 1][0]
    df2_next_datetime = tick2_arr[df2_index + 1][0]

    # if df1 first tick occurs *before* df2 then advance df2 index so that 
    # df2_index refers to the first tick chronologically before df1 first tick
    if df1_first_time > df2_first_time:

        while (df2_next_datetime < df1_first_time):
            df2_index = df2_index + 1
            df2_next_datetime = tick2_arr[df2_index + 1]

    else:

        while (df1_next_datetime < df2_first_time):
            df1_index = df1_index + 1
            df1_next_datetime = tick1_arr[df1_index + 1]


    f1_len = len(tick1_arr)
    f2_len = len(tick2_arr)

    while((df1_index + 1) < f1_len and (df2_index + 1) < f2_len):

        df1_next_datetime = tick1_arr[df1_index + 1][0]
        df2_next_datetime = tick2_arr[df2_index + 1][0]

        yield (tick1_arr[df1_index][1], tick2_arr[df2_index][2])

        if (df1_next_datetime > df2_next_datetime):
        # increment df2_index and not df1_index
            df2_index = df2_index + 1    

        else: # df1_next_datetime < df2_next_datetime
            #increment df1_index and not df2_index
            df1_index = df1_index + 1


file1 = '/Users/P/Documents/Prices/2015/USD_JPY/January/USD_JPY_Week1.csv'
file2 = '/Users/P/Documents/Prices/2015/EUR_JPY/January/EUR_JPY_Week1.csv'

# load both files

#df1 = pd.read_csv(file1, usecols=['RateDateTime','RateBid','RateAsk'])
#df2 = pd.read_csv(file2, usecols=['RateDateTime','RateBid','RateAsk'])

r = []

for c in price_pairs_csv(file1, file2):
    #print(c)
    r.append(c[0]/c[1])
    

plt.plot(r)
plt.show()


# find whichever file starts later

# 



