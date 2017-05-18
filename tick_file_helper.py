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