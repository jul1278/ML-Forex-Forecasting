import os
import zipfile
import tempfile
import sys
import csv
import pandas as pd
import datetime
import tick_to_candle as tc
import somoclu
import math

#example_len = 52;
#example_step = 26; 

def extract_to_dir(zip_files, directory):
    for zip_file in zip_files:
        zip_ref = zipfile.ZipFile(zip_file, 'r')

        parent_folder = zip_file.split(os.path.sep)[-2]
        extract_dir = os.path.join(directory, parent_folder)

        zip_ref.extractall(path=extract_dir)
        
def get_files_in_directory(directory, filter):
    for dir_name, _, files in os.walk(directory):
        for file in files:
            if filter in file:
                yield os.path.join(dir_name, file)

def main():
    
    if (len(sys.argv) < 2):
        print('Quitting...')
        quit()

    temp_directory = os.path.join(tempfile.gettempdir(), 'prices')

    prices_path = sys.argv[1]
    extract_path = sys.argv[2]
    output_path = sys.argv[3]

    zip_files = get_files_in_directory(prices_path, '.zip')
    extract_to_dir(zip_files, extract_path)

    # go through all the extracted csv's and sort them based on the time of the first and last prices
    csv_files = get_files_in_directory(extract_path, '.csv')

    file_startdates = []

    for csv_file in csv_files:
        print(csv_file)
        df = pd.read_csv(csv_file, nrows=2)
        start_time_str = df.iloc[1]['RateDateTime']
        print(start_time_str)
        start_time = tc.parse_time(start_time_str)

        file_startdates.append((csv_file, start_time_str))

    sorted_files = sorted(file_startdates, key = lambda tup: tup[1])

    ohlc_files = []

    for file_startdate in sorted_files:
        
        # get relative path
        print(file_startdate[0])
        
        diff = [i for i in xrange(min(len(file_startdate[0]),len(prices_path))) if file_startdate[0][i] != prices_path[i]]
        rel = file_startdate[0][diff[0]:]
        rel = rel.replace('.csv', '')
        
        # remove the top folder which is 'extract' or something
        rel_split = rel.split(os.sep)[1:]

        output_file_name = '_'.join(rel_split) + ' ohlc.csv'
        print('name: ' + output_file_name)

        tc.ticks_to_candle(file_startdate[0], output_path, output_file_name)

        ohlc_files.extend(output_file_name)


main()
