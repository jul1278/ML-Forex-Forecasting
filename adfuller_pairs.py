# adfuller_pairs.py

from statsmodels.tsa.stattools import adfuller
from matplotlib import pyplot
import numpy as np
import pandas as pd
import random as rnd
import math


pairs_csv = 'cpp/pairs.csv'
df = pd.read_csv(pairs_csv)

window_size = 500
window_step = 100
offset = 13900

num_windows = int(math.floor(len(df) / window_size))

end = len(df) - window_size

for i in range(offset, end, window_step):
    
    p1 = df.iloc[i:(i+window_size), 1]
    p2 = df.iloc[i:(i+window_size), 2]

    p1_norm = (p1 - p1.min()) / (p1.max() - p1.min()) 
    p2_norm = (p2 - p2.min()) / (p2.max() - p2.min()) 

    diff = p1_norm - p2_norm
    adf_result = adfuller(diff)

    if (adf_result[1] <= 0.5):
        print("t-stat: " + str(adf_result[1]) +  " p: " +  str(adf_result[1]) + " - yes")
    else:
        print("t-stat: " + str(adf_result[1]) +  " p: " +  str(adf_result[1]) + " - no")
        

    fig, [ax1, ax2] = pyplot.subplots(2, 1)

    ax1.set_xlabel('time')
    ax1.set_ylabel(df.columns[1], color='b')
    ax1.plot(p1, 'b-', linewidth=1.0)
    
    ax1_2 = ax1.twinx()
    ax1_2.plot(p2, 'r-', linewidth=1.0)
    ax1_2.set_ylabel(df.columns[2], color='r')
    

    ax2.set_title('diff')

    av = diff.rolling(window=50).std()

    ax2.plot(diff, linewidth=0.8)
    ax2.plot(range(i, i + len(av)), av, linewidth=0.8)

    # fig.tight_layout()

    pyplot.show()
    
quit()