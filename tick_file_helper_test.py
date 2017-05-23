# tick_file_helper_test.py

import tick_file_helper
import datetime
import pandas as pd

strt = datetime.datetime(2014, 4, 8, 11, 50, 57)
idx = tick_file_helper.find_index_closest_date(strt, 'USD_JPY_Week2_test.csv')

df = pd.read_csv('USD_JPY_Week2_test.csv', usecols=['RateDateTime'])

print(idx)
print(df.iloc[(idx - 5):(idx + 5)])


