import sys
import os
import numpy as np
import pandas as pd
import time
import datetime as datetime
import matplotlib.pyplot as plt
import matplotlib.finance as fin

bid_header = 'RateBid'
ask_header = 'RateAsk'
time_header = 'RateDateTime'

# assumes usec could be present
def parse_time(time_str):

    if '.' in time_str:
        time_str_split, us_str = time_str.split('.')
        t = datetime.datetime.strptime(time_str_split, '%Y-%m-%d %H:%M:%S')
        return t
    else:
        return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

# to_candle
def to_candle(ticks, period):

    bid = ticks[bid_header][0]
    offer = ticks[ask_header][0]
    time = ticks[time_header][0]

    open_time = parse_time(time)
    last_open_time = open_time
    current_time = open_time
    open_price = (bid + offer) / 2
    low_price = open_price
    high_price = open_price
    close_price = open_price

    print(time, open_time)

    it = ticks.iterrows()
    
    # skip the first row
    next(it) 
    
    for i, row in it:
        full_time_str = row[time_header]

        current_time = parse_time(full_time_str)
        current_offer = row[ask_header]
        current_bid = row[bid_header]
        current_mid = (current_bid + current_offer) / 2
        close_price = current_mid

        delta = (current_time - open_time) 

        if current_mid > high_price:
            high_price = current_mid

        if current_mid < low_price:
            low_price = current_mid

        if delta > period:
            yield [last_open_time, current_time, open_price, close_price, high_price, low_price]

            last_open_time = current_time
            open_time = current_time
            open_price = current_mid
            low_price = open_price
            high_price = open_price
            close_price = open_price


# ticks_to_candle
def ticks_to_candle(filepath, output_folder, output_filename):
    # todo: check file exists
    if os.path.isfile(filepath) is False:
        quit()

    headers = ['lTid','cDealable','CurrencyPair','RateDateTime','RateBid','RateAsk'] 
    prices = pd.read_csv(filepath, names=headers, skiprows=1)

    # TODO: check the csv has data and correct columns
    candles = pd.DataFrame(columns=['open_time', 'close_time', 'open_price', 'close_price', 'high_price', 'low_price'])

    for c in to_candle(prices, datetime.timedelta(seconds=60)):
        candles = candles.append(pd.DataFrame(data=[c], columns=['open_time', 'close_time', 'open_price', 'close_price', 'high_price', 'low_price']))

    filefolder = os.path.dirname(filepath)
    filename = os.path.basename(filepath)

    output_file_path = os.path.join(output_folder, output_filename)

    if not os.path.exists(os.path.dirname(output_file_path)):
        os.makedirs(os.path.dirname(output_file_path))

    candles.to_csv(output_file_path, index=False)    


# get_files_in_directory
def get_files_in_directory(directory, filter):
    for dir_name, _, files in os.walk(directory):
        for file in files:
            if filter in file:
                yield os.path.join(dir_name, file)

# main
def main():
    
    if (len(sys.argv) < 2):
        print('Quitting...')
        quit()

    csv_path = sys.argv[1]
    output_path = sys.argv[2]

    # go through all the csv's and sort them based on the time of the first and last prices
    csv_files = get_files_in_directory(csv_path, '.csv')

    file_startdates = []

    for csv_file in csv_files:
        print(csv_file)
        df = pd.read_csv(csv_file, nrows=2)
        start_time_str = df.iloc[1]['RateDateTime']
        currency_pair_str = df['CurrencyPair'].iloc[1]
        print(start_time_str)
        start_time = parse_time(start_time_str)

        file_startdates.append((csv_file, start_time, currency_pair_str))

    sorted_files = sorted(file_startdates, key = lambda tup: tup[1])

    ohlc_files = []

    counter = 0
    avg_duration = 0.0

    for file_startdate in sorted_files:
        
        # get relative path
        print(file_startdate[0])
        
        #diff = [i for i in xrange(min(len(file_startdate[0]),len(csv_path))) if file_startdate[0][i] != csv_path[i]]

        #if diff == []:
        #    diff = [min(len(file_startdate[0]),len(csv_path))]
        
        #rel = file_startdate[0][diff[0]:]
        #rel = rel.replace('.csv', '')

        # remove the top folder which is 'extract' or something
        #rel_split = rel.split(os.sep)[1:]

        # folder should be ohlc/USD_JPY/USD_JPY_YY_MM_DD_HH_mm_ss.csv ??

        #output_file_name = '_'.join(rel_split) + ' ohlc.csv'
        
        output_file_name = file_startdate[2].replace('/', '_') + file_startdate[1].strftime('_%Y_%m_%d_%H_%M_%S') + '.csv'

        print('name: ' + output_file_name)
        
        start = time.time()
        ticks_to_candle(file_startdate[0], output_path, output_file_name)
        end = time.time()

        duration = end - start

        avg_duration = (duration + counter * avg_duration) / (counter + 1)
        counter = counter + 1

        print("elapsed: " + str(duration))

        remaining = avg_duration * (len(sorted_files) - counter)

        print("remaining time: " + str(remaining / 60.0) + " mins")

        ohlc_files.extend(output_file_name)

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()


