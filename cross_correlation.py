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

file1_path = 'C:\\Julian\\Prices\\2015\\AUD_JPY\\January\\AUD_JPY_Week1.csv'
file2_path = 'C:\\Julian\\Prices\\2015\\USD_JPY\\January\\USD_JPY_Week1.csv'

start_time = datetime.datetime(2015, 1, 7, 2, 15)
end_time = datetime.datetime(2015, 1, 7, 2, 18)

plt.subplot(2, 1, 1)
plt.title(str(file1_path))
plot_ticks.plot_tick_range_normalised(file1_path, start_time, end_time)
#plt.axvline(end_time, color='r')

plt.subplot(2, 1, 2)
plt.title(str(file2_path))
plot_ticks.plot_tick_range_normalised(file2_path, start_time, end_time)
#plt.axvline(end_time, color='r')

plt.show()