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
import plot_ticks
import tick_file_helper
import matplotlib.pyplot as plt

example_len = 4*8

# main
def main():
    
    if len(sys.argv) < 3:
        print('Not enough arguments')
        print('Quitting...')
        quit()

    training_set_path = sys.argv[1]
    tick_path = sys.argv[2]

    if os.path.exists(training_set_path) == False:
        print(training_set + ' does not exist.')
        quit()

    # read training set
    training_set = pd.read_csv(training_set_path)
    patterns = training_set.iloc[:, 1:(example_len + 2)].values # add + 2 so we see the result as well
    
    # find all the ohlc files as well
    tick_files = tick_file_helper.get_files_in_directory(tick_path, '.csv')
    tick_date_map = list(tick_file_helper.build_tick_date_map(tick_files))

    smallest_dist = 1000000
    smallest_index = (0, 0)

    same_result_no_matching_pattern = 0
    diff_result_no_matching_pattern = 0

    same_result_w_matching_pattern = 0
    diff_result_w_matching_pattern = 0

    index = 0
    for pattern in patterns:
        
        time_str = str(training_set['time_stamp'].loc[index])
        time_dt = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        time_dt_close = time_dt + datetime.timedelta(minutes=example_len/4) 

        tick_path = tick_file_helper.find_tick_path_from_date(tick_date_map, time_str)

        current_index = 0
        for curr_pattern in patterns: 
            if index == current_index:
                current_index += 1
                continue

            diff = np.subtract(curr_pattern[:-1], pattern[:-1])
            sqr_diff = np.power(diff, 2)
            sqr = math.sqrt(np.sum(sqr_diff))

            # assume something fucked up
            if sqr == 0.0:
                current_index += 1
                continue

            if (sqr < 0.5):
                smallest_dist = sqr
                smallest_index = (current_index, index)
                
                print(smallest_dist)
                print(str(index) + ', ' + str(current_index))
                
                if current_index >= len(training_set.index):
                    break 
                
                curr_time_str = str(training_set['time_stamp'].loc[current_index])
                curr_time_dt = datetime.datetime.strptime(curr_time_str, '%Y-%m-%d %H:%M:%S')
                curr_time_dt_close = curr_time_dt + datetime.timedelta(minutes=example_len/4) 

                if (pattern[-1] != curr_pattern[-1]):
                    diff_result_w_matching_pattern += 1
                else:
                    same_result_w_matching_pattern += 1

                print(time_str + ', ' + curr_time_str)

                curr_tick_path = tick_file_helper.find_tick_path_from_date(tick_date_map, curr_time_str)
                
                plt.subplot(2, 1, 1)
                plt.title(str(tick_path))
                plot_ticks.plot_tick_range(tick_path, time_dt, time_dt_close)
                
                plt.subplot(2, 1, 2)
                plt.title(str(curr_tick_path))
                plot_ticks.plot_tick_range(curr_tick_path, curr_time_dt, curr_time_dt_close)

                plt.show()

            else:
                if (pattern[-1] != curr_pattern[-1]):
                    diff_result_no_matching_pattern += 1
                else:
                    same_result_no_matching_pattern += 1

            current_index += 1
                
        index += 1
        
        # reset these when we start a new pattern
        smallest_dist = 1000000
        smallest_index = (0, 0)

    print('Same result, different pattern: ' + str(same_result_no_matching_pattern))
    print('Same result, matching pattern: ' + str(same_result_w_matching_pattern))
    print('Different result, different pattern: ' + str(diff_result_no_matching_pattern))
    print('Different result, matching pattern: ' + str(diff_result_w_matching_pattern))

    print(smallest_dist)
    print(smallest_index)

if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
   main()