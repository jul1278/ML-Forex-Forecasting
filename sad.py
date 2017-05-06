# sad.py
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

# sum_of_abs_diff
def sum_of_abs_diff(training_set_path):

    training_set = pd.read_csv(training_set_path)
    training_set_ex = training_set[training_set.columns[1:(example_len+1)]]

    r = len(training_set.rows)

    res = numpy.zeros(r, r)

    for index, row in training_set_ex.iterrows():
        for curr_index, curr_row in training_set_ex.iterrows():
            
            if (curr_index == index):
                continue

            result = row.subtract(curr_row).sum()
            res[index, curr_index] = result 


          

        

            






