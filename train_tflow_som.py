# train_tflow_som.py

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
#import plot_ohlc
import ohlc_file_helper
import som
import tensorflow as tf

from collections import defaultdict
from matplotlib import pyplot as plt

example_len = 30
example_step = 15

if len(sys.argv) < 2:
    print('Not enough arguments, requires path to training set and path to ohlc files')
    print('Quitting...')
    quit()

training_set_path = sys.argv[1]
ohlc_files_path = sys.argv[2]

if os.path.exists(training_set_path) == False:
    print('path does not exist')
    quit()

print(time.strftime("%H:%M:%S") + ' loading training set...')

training_set_df = pd.read_csv(training_set_path)

print(time.strftime("%H:%M:%S") + ' training set shape: ' + str(training_set_df.shape))

# find all the ohlc files as well
ohlc_files = ohlc_file_helper.get_files_in_directory(ohlc_files_path, '.csv')
ohlc_date_map = list(ohlc_file_helper.build_ohlc_date_map(ohlc_files))

print(time.strftime("%H:%M:%S") + ' training SOM')

training_set = training_set_df.iloc[:100, 1:(example_len + 1)].values

print(training_set)

num_training = 20#400
sm = som.SOM(20, 30, example_len, num_training)
sm.train(training_set)

# plt.imshow(np.reshape(s.get_weights(), [30, 30, 3]))
# plt.show()

#Get output grid
image_grid = sm.get_centroids()
 
#Plot
plt.imshow(image_grid)
plt.title('SOM')
plt.show()