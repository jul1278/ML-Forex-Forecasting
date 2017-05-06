# plot_ohlc_test.py

import datetime
import plot_ohlc

strt = datetime.datetime(2014, 4, 8)
end = datetime.datetime(2014, 4, 9)

plot_ohlc.plot_ohlc_range('/Users/P/Documents/Prices/ohlc/apr_USD_JPY_Week2 ohlc.csv', strt, end)