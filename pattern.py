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

# build_pattern_set
def build_pattern_set(tick_path, pattern_output_path):
    tick_files = list(ohlc_file_helper.get_files_in_directory(tick_path, '.csv'))
    patterns = []

    for tick_file in tick_files[:1]:
        print(tick_file)

        df = pd.read_csv(tick_file)

        mid = (df['RateBid'] + df['RateAsk']) / 2.0
        mid_diff = mid.diff()
        mid_pct = np.divide(mid_diff[1:], mid[:len(mid)-1])

        for n in range(0, len(mid_pct.index), example_len / 2):
            if (n + example_len) < len(mid_pct.index):           
                patterns.append(mid_pct.iloc[n:(n+example_len)].values)
            else:
                break

    
    return patterns

# main
def main():
    
    if len(sys.argv) < 3:
        print('Not enough arguments')
        print('Quitting...')
        quit()

    training_set = sys.argv[1]
    ohlc_path = sys.argv[2]

    if os.path.exists(ticks_path) == False:
        print ticks_path + ' does not exist.'
        quit()

    index = 0
    current_index = 0

    

    for pattern in patterns:
        for curr_pattern in patterns: 
            
            diff = np.subtract(curr_pattern, pattern)
            pct_diff = np.absolute(np.divide(diff, pattern))

            average = pct_diff.average()

            current_index += 1
        
        index += 1

if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
   main()