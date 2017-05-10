# build_feature_set.py

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

example_len = 30
example_step = 15

# get_files_in_directory
def get_files_in_directory(directory, filter):
    for dir_name, _, files in os.walk(directory):
        for file in files:
            if filter in file:
                yield os.path.join(dir_name, file)

def main():

    if (len(sys.argv) < 2):
        print('ohlc files path / training set csv path missing')
        print('Quitting...')
        quit()

    ohlc_path = sys.argv[1]

    if (os.path.exists(ohlc_path) == False):
        print('path does not exist')
        quit()

    print(ohlc_path)

    ohlc_files = get_files_in_directory(ohlc_path, '.csv')
    output_file = sys.argv[2]

    training_set = []

    for ohlc_file in ohlc_files:
        #normalise
        #get training examples
        #train map

        print(ohlc_file)

        #read csv
        df = pd.read_csv(ohlc_file)
        dates = df[['open_time']]

        #normalise
        diff = df[['open_price', 'close_price', 'high_price', 'low_price']].diff(axis=0)
        norm = diff.divide(df[['open_price', 'close_price', 'high_price', 'low_price']])
        
        # flatten and drop the first four because they're NAN
        norm_flat = norm.values.flatten()[4:]

        norm_max = norm_flat.max()
        norm_min = norm_flat.min()

        norm_flat_scaled = np.divide(norm_flat - norm_min * np.ones(len(norm_flat)), norm_max - norm_min)
        norm_flat_scaled = [x - norm_flat_scaled.mean() for x in norm_flat_scaled]

        size_len = len(norm_flat_scaled)
        num_examples = int(math.floor(size_len / example_len))

        for n in range(num_examples):
            i_offset = n * example_len; 
            i_offset_end = i_offset + example_len;

            if (i_offset_end + 4) >= size_len:
                break    

            #extract from i_offset tp i_offset_end and put into new aray
            sample = norm_flat_scaled[i_offset:i_offset_end]

            current_date_index = int(math.floor(i_offset / 4) + 1)
            next_close_price_index = i_offset_end + 4

            current_date = dates.loc[current_date_index]
            sample_strings = ['{:.10f}'.format(x) for x in sample]
            
            # we want the normalised price but not scaled
            next_price = norm_flat[next_close_price_index]
            
            next_price_class = 0
            
            # classify the price change
            if next_price >= 0.0001:
                next_price_class = 1
            elif next_price <= -0.0001:
                next_price_class = 2

            write = [current_date.to_string(index=False)] + sample_strings + [next_price_class]    
            training_set.append(write)

        # write the training_set in random order to a csv
        with open(output_file, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

            # TODO write headers
            headers = ['time_stamp'] + [str(x) for x in range(1, example_len + 1)] + ['next_price']
            writer.writerow(headers)  

            for index in random.sample(range(0, len(training_set)), len(training_set)):
                writer.writerow(training_set[index])
                
if __name__ == "__main__":
       # stuff only to run when not called via 'import' here
   main()