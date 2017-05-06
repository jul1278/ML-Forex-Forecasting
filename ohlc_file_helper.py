# ohlc_file_helper.py
import os
import zipfile
import tempfile
import sys
import csv
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
def build_ohlc_date_map(ohlc_files):
    for ohlc_file in ohlc_files:
        file_df = pd.read_csv(ohlc_file)

        start_date = file_df['open_time'].iloc[0]
        last_date = file_df['open_time'].iloc[-1]

        # get the first date and the last date and make a tuple
        yield (start_date, last_date, ohlc_file)
        

# find_ohlc_path_from_date
def find_ohlc_path_from_date(ohlc_map, date):
    for start_date, end_date, file_path in ohlc_map:
        
        #print file_path

        curr_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        start_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

        if (curr_date >= start_datetime) and (curr_date <= end_datetime):
            return file_path

if __name__ == "__main__":
   quit()