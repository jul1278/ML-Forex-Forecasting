# train_map.py

import os
import zipfile
import tempfile
import sys
import csv
import pandas as pd
import numpy as np
import datetime
import somoclu
import math
import time
import random
import plot_ohlc
import ohlc_file_helper

from collections import defaultdict

example_len = 32
example_step = 16

# main
def main():

    if len(sys.argv) < 3:
        print('Not enough arguments, requires path to training set and path to ohlc files')
        print('Quitting...')
        quit()

    training_set_path = sys.argv[1]
    ohlc_files_path = sys.argv[2]
    codebook_dir = sys.argv[3]

    if os.path.exists(training_set_path) == False:
        print('path does not exist')
        quit()
    
    print time.strftime("%H:%M:%S") + ' loading training set...'
    training_set = pd.read_csv(training_set_path)
    training_set_ex = training_set[training_set.columns[1:(example_len+1)]]

    print time.strftime("%H:%M:%S") + ' training set shape: ' + str(training_set.shape)

    # find all the ohlc files as well
    ohlc_files = get_files_in_directory(ohlc_files_path, '.csv')
    ohlc_date_map = list(build_ohlc_date_map(ohlc_files))

    # TODO: check if codebook exists

    print time.strftime("%H:%M:%S") + ' training SOM'
    som = somoclu.Somoclu(15, 29, data=training_set_ex.as_matrix(), compactsupport=False)
    som.train(radiuscooling='exponential', epochs=100, scale0=0.2)

    print time.strftime("%H:%M:%S") + ' train finished'

    # uses default k means clustering
    som.cluster()
    som.view_umatrix(bestmatches=True)

    # save the codebook to a csv
    codebook_df = pd.DataFrame(som.clusters)

    codebook_file_path = os.path.join(codebook_dir, 'som_codebook_' + time.strftime('%Y_%m_%d_%H_%M_%S') + '.csv')
    codebook_df.to_csv(codebook_file_path)

    example_cluster_map = defaultdict(list)

    # build cluster_map
    for i in range(len(training_set_ex)):      
        cluster = som.clusters[som.bmus[i, 1], som.bmus[i, 0]]
        example_cluster_map[cluster].append(i)
        
    # visualise
    while 2 > 1:
        
        k = random.randint(0, len(som.clusters) - 1)

        cluster_size = len(example_cluster_map[k])

        fst_index = example_cluster_map[k][random.randint(0, cluster_size-1)]
        snd_index = example_cluster_map[k][random.randint(0, cluster_size-1)]

        # get the open times of the examples
        fst_open_time = training_set['time_stamp'].iloc[fst_index]
        snd_open_time = training_set['time_stamp'].iloc[snd_index]

        fst_ohlc_path = find_ohlc_path_from_date(ohlc_date_map, fst_open_time)
        snd_ohlc_path = find_ohlc_path_from_date(ohlc_date_map, snd_open_time)

        if fst_ohlc_path != None and snd_ohlc_path != None:
            
            print fst_open_time
            print snd_open_time

            # 
            fst_open_datetime = datetime.datetime.strptime(fst_open_time, '%Y-%m-%d %H:%M:%S')
            fst_close_datetime = fst_open_datetime + datetime.timedelta(minutes=example_len/4) 

            snd_open_datetime = datetime.datetime.strptime(snd_open_time, '%Y-%m-%d %H:%M:%S')
            snd_close_datetime = snd_open_datetime + datetime.timedelta(minutes=example_len/4) 

            plot_ohlc.plot_ohlc_range(fst_ohlc_path, fst_open_datetime, fst_close_datetime)
            plot_ohlc.plot_ohlc_range(snd_ohlc_path, snd_open_datetime, snd_close_datetime)

if __name__ == "__main__":
       # stuff only to run when not called via 'import' here
   main()