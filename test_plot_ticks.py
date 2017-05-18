# plot_ticks_test.py

import datetime
import plot_ticks

strt = datetime.datetime(2014, 4, 6, 17)
end = datetime.datetime(2014, 4, 6, 18)

plot_ticks.plot_tick_range('C:\\Julian\\Prices\\2014\\USD_JPY\\April\\USD_JPY_Week2.csv', strt, end)