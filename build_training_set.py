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

example_len = 4*8
example_step = 4*2

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

        size_len = len(norm_flat)
        num_examples = int(math.floor(size_len / example_len))

        for n in range(num_examples):
            i_offset = n * example_step
            i_offset_end = i_offset + example_len

            if (i_offset_end + 4) >= size_len:
                break    

            #extract from i_offset tp i_offset_end and put into new aray
            sample = norm_flat[i_offset:i_offset_end]

            norm_min = sample.min()
            norm_max = sample.max()

            sample_norm = np.divide(sample - norm_min * np.ones(len(sample)), norm_max - norm_min)

            current_date_index = int(math.floor(i_offset / 4) + 1)
            next_close_price_index = i_offset_end + 4

            current_date = dates.loc[current_date_index]
            sample_strings = ['{:.10f}'.format(x) for x in sample_norm]
            
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