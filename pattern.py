# pattern.py

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
import plot_ohlc
import ohlc_file_helper
import matplotlib.pyplot as plt

example_len = 4*8

# main
def main():
    
    if len(sys.argv) < 3:
        print('Not enough arguments')
        print('Quitting...')
        quit()

    training_set_path = sys.argv[1]
    ohlc_path = sys.argv[2]

    if os.path.exists(training_set_path) == False:
        print(training_set + ' does not exist.')
        quit()

    # read training set
    training_set = pd.read_csv(training_set_path)
    patterns = training_set.iloc[:, 1:(example_len + 2)].values
    
    # find all the ohlc files as well
    ohlc_files = ohlc_file_helper.get_files_in_directory(ohlc_path, '.csv')
    ohlc_date_map = list(ohlc_file_helper.build_ohlc_date_map(ohlc_files))

    smallest_dist = 1000000
    smallest_index = (0, 0)

    index = 0
    for pattern in patterns:
        
        time_str = str(training_set['time_stamp'].loc[index])
        time_dt = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        time_dt_close = time_dt + datetime.timedelta(minutes=example_len/4) 

        ohlc_path = ohlc_file_helper.find_ohlc_path_from_date(ohlc_date_map, time_str)
        plot_ohlc.plot_ohlc_range(ohlc_path, time_dt, time_dt_close)

        current_index = 0
        for curr_pattern in patterns: 
            if index == current_index:
                current_index += 1
                continue

            diff = np.subtract(curr_pattern, pattern)
            sqr_diff = np.power(diff, 2)
            sqr = math.sqrt(np.sum(sqr_diff))

            # assume something fucked up
            if sqr == 0.0:
                current_index += 1
                continue

            if (sqr < smallest_dist):
                smallest_dist = sqr
                smallest_index = (current_index, index)
                
                print(smallest_dist)
                print(str(index) + ', ' + str(current_index))
                
                if current_index >= len(training_set.index):
                    break 
                
                curr_time_str = str(training_set['time_stamp'].loc[current_index])
                curr_time_dt = datetime.datetime.strptime(curr_time_str, '%Y-%m-%d %H:%M:%S')
                curr_time_dt_close = curr_time_dt + datetime.timedelta(minutes=example_len/4) 

                print(time_str + ', ' + curr_time_str)
                
                curr_ohlc_path = ohlc_file_helper.find_ohlc_path_from_date(ohlc_date_map, curr_time_str)
                plot_ohlc.plot_ohlc_range(curr_ohlc_path, curr_time_dt, curr_time_dt_close)
                
            current_index += 1
                
        index += 1
        
        # reset these when we start a new pattern
        smallest_dist = 1000000
        smallest_index = (0, 0)

    print(smallest_dist)
    print(smallest_index)

if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
   main()