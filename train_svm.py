# train_svm.py
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
import train_map
import plot_ohlc

from sklearn import svm

from collections import defaultdict

example_len = 60
training_len = 18000

# main
def main():

    print 'starting...'

    if len(sys.argv) < 3:
        print('Not enough arguments, requires path to training set and path to ohlc files')
        print('Quitting...')
        quit()

    training_set_path = sys.argv[1]
    ohlc_files_path = sys.argv[2]
    #codebook_dir = sys.argv[3]

    if os.path.exists(training_set_path) == False:
        print('path does not exist')
        quit()
    
    print time.strftime("%H:%M:%S") + ' loading training set...'

    training_set_extended = pd.read_csv(training_set_path)

    training_len = int(0.8 * len(training_set_extended.index))

    training_set = training_set_extended[training_set_extended.columns[1:(example_len+1)]][:training_len]
    training_set_pred = training_set_extended['next_price'][:training_len]

    test_set = training_set_extended[training_set_extended.columns[1:(example_len+1)]][(training_len+1):]
    test_set_result = training_set_extended['next_price'][(training_len+1):]

    print time.strftime("%H:%M:%S") + ' training set shape: ' + str(training_set.shape)

    X = training_set
    y = training_set_pred

    clf = svm.SVC()
    clf.fit(X, y) 

    correct = 0
    incorrect = 0

    print str(len(test_set.index))
    print str(len(training_set.index))

    ohlc_files = train_map.get_files_in_directory(ohlc_files_path, '.csv')
    ohlc_date_map = list(train_map.build_ohlc_date_map(ohlc_files))

    for index, row in test_set.iterrows():

        pred = int(clf.predict([row])[0])
        result = int(row['next_price'])
        print 'prediction: ', pred #row['next_price']
        print 'actual: ', result #index

        curr_date = training_set_extended['time_stamp'].iloc[index]
        curr_ohlc_path = train_map.find_ohlc_path_from_date(ohlc_date_map, curr_date)

        print curr_date

        curr_datetime = datetime.datetime.strptime(curr_date, '%Y-%m-%d %H:%M:%S')
        close_datetime = curr_datetime + datetime.timedelta(minutes=example_len + 1) 

        plot_ohlc.plot_ohlc_range(curr_ohlc_path, curr_datetime, close_datetime)

        if (pred == result):
            correct += 1
        else:
           incorrect += 1 

    print 'correct: ' + str(correct)
    print 'incorrect: ' + str(incorrect)

main()