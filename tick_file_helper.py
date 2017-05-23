# tick_file_helper.py
import os
import zipfile
import tempfile
import sys
import csv
import plot_ticks
import pandas as pd
import numpy as np
import datetime
import math
import time
import random

# get_files_in_directory
def get_files_in_directory(directory, filter):
    for dir_name, _, files in os.walk(directory):
        for file in files:
            if filter in file:
                yield os.path.join(dir_name, file)

# build_ohlc_date_map
def build_tick_date_map(tick_files):
    for tick_file in tick_files:
        file_df = pd.read_csv(tick_file)

        start_date = file_df['RateDateTime'].iloc[0]
        last_date = file_df['RateDateTime'].iloc[-1]

        # get the first date and the last date and make a tuple
        yield (start_date, last_date, tick_file)
    

# find_index_closest_date
def find_index_closest_date(find_date_time, tick_file_path):
    
    # TODO: check file exists
    file_df = pd.read_csv(tick_file_path)

    start_date = plot_ticks.parse_time(file_df['RateDateTime'].iloc[0])
    end_date = plot_ticks.parse_time(file_df['RateDateTime'].iloc[-1])

    # check given date is within the bounds of the file
    if (find_date_time < start_date or find_date_time > end_date):
        print("find date outside file date bounds.")
        return

    index = 0
    index = int(len(file_df.index)/2)

    index_min = 0
    index_max = len(file_df.index) - 1

    # do a binary search to find
    while (index < len(file_df.index) and index > 0):
        
        current_date = plot_ticks.parse_time(file_df['RateDateTime'].iloc[index])
        prev_date_time = plot_ticks.parse_time(file_df['RateDateTime'].iloc[index-1])
        next_date_time = plot_ticks.parse_time(file_df['RateDateTime'].iloc[index+1])

        if (find_date_time <= current_date and find_date_time >= prev_date_time):
            if (find_date_time - prev_date_time) > (current_date - find_date_time):
                return (index - 1)    
            else:
                return index

        if (find_date_time >= current_date and find_date_time <= next_date_time):
            if (find_date_time - current_date) > (next_date_time - find_date_time):
                return index
            else:
                return (index + 1)

        if (current_date > find_date_time):
            # halve index
            old_index = index
            index = index_min + int((index - index_min) / 2)
            index_max = old_index
            
        elif (current_date < find_date_time):
            #add half to index
            old_index = index
            index = int(math.ceil( index + ((index_max - index) / 2))) 
            index_min = old_index
            
# find_ohlc_path_from_date
def find_tick_path_from_date(tick_map, date):
    for start_date, end_date, file_path in tick_map:
        
        #print file_path

        curr_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        start_datetime = plot_ticks.parse_time(start_date) #datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S.%f')
        end_datetime = plot_ticks.parse_time(end_date) #datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

        if (curr_date >= start_datetime) and (curr_date <= end_datetime):
            return file_path

if __name__ == "__main__":
   quit()