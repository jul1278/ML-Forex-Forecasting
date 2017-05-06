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

example_len = 30

# find_similarity
def find_similarity(training_set_path, ohlc_path):
    
    training_set = pd.read_csv(training_set_path)
    training_set_ex = training_set[training_set.columns[1:(example_len+1)]]

    # find all the ohlc files as well
    ohlc_files = ohlc_file_helper.get_files_in_directory(ohlc_path, '.csv')
    ohlc_date_map = list(ohlc_file_helper.build_ohlc_date_map(ohlc_files))

    sim = []

    for index, row in training_set_ex.iterrows():
        
        fst_open_time = training_set['time_stamp'].iloc[index]
        print fst_open_time

        for curr_index, curr_row in training_set_ex.iterrows():
            
            if curr_index == index:
                continue

            result = (abs(curr_row - row) / row).sum()
            
            if result < 0.5:
                print result

    


# main
def main():
    
    if len(sys.argv) < 3:
        print('Not enough arguments, requires path to training set and path to ohlc files')
        print('Quitting...')
        quit()

    training_set_path = sys.argv[1]
    ohlc_path = sys.argv[2]
    
    if os.path.exists(training_set_path) == False:
        print 'training set path ' + training_set_path + ' does not exist'
        quit()

    if os.path.exists(ohlc_path) == False:
        print ohlc_path + ' does not exist.'
        quit()

    find_similarity(training_set_path, ohlc_path)

if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
   main()