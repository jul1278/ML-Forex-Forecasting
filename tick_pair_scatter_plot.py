# tick_pair_scatter_plot.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import linear_model

# moving_average
def moving_average(nums, window_size):
    for i in range(window_size, len(nums)):
        yield np.average(nums[(i - window_size):i])
    

pair_file = 'cpp/pairs.csv'

pair1_header = 'AUD_JPY_Week1.csv'
pair2_header = 'USD_JPY_Week1.csv'

pairs_df = pd.read_csv(pair_file)

inc = 18500
window = 400
step = 50

while True:

    ser = pairs_df.iloc[inc:(inc + window)]

    pair1 = ser[pair1_header].reshape((window, 1))
    pair2 = ser[pair2_header].reshape((window, 1))

    regr_full = linear_model.LinearRegression()
    regr1 = linear_model.LinearRegression()
    regr2 = linear_model.LinearRegression()
    
    regr1.fit(pair1[:300], pair2[:300])
    regr2.fit(pair2[:300], pair1[:300])
    regr_full.fit(pair1, pair2)

    pred = regr_full.predict(pair1)

    #plt.clf()

    pred1 = regr1.predict(pair1[300:350])
    pred2 = regr2.predict(pair2[300:350])

    # plot scatter
    fig = plt.figure(figsize=(11, 10))
    plt.subplot(4, 1, 1)
    plt.scatter(pair1, pair2)
    plt.plot(pair1, pred, color='red', linewidth=1)
    plt.title(pair1_header + ' vs ' + pair2_header)

    # first pair
    plt.subplot(4, 1, 3)
    plt.plot(pair1)
    #plt.plot(range(300, 350), pred2)
    #plt.axvline(300, color='red')

    max_idx1 = np.argmax(pred2)

    ylim_min, ylim_max = plt.ylim()
    xlim_min, xlim_max = plt.xlim()

    #plt.plot([max_idx1 + 302.5, max_idx1 + 325], [pair1[max_idx1 + 300] + 500, pair1[max_idx1 + 300] + 10000], color='red', linestyle='-', linewidth=1.5)
    plt.title(pair1_header)

    # second pair
    plt.subplot(4, 1, 2)
    plt.plot(pair2)
    #plt.plot(range(300, 350), pred1)
    #plt.axvline(300, color='red')
    plt.title(pair2_header)

    plt.subplot(4, 1, 4)

    diff = pair2 - pair1
    ma = list(moving_average(diff, 50))

    plt.plot(diff)
    plt.plot(range(50, window), ma)
    plt.title(pair2_header + ' / ' + pair1_header)

    plt.show()

    inc = inc + step 

