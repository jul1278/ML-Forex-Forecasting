# plot_ticks_test.py
import matplotlib.pyplot as plt

import datetime
import plot_ticks

strt_a = datetime.datetime(2014, 4, 6, 17, 5)
mid_a = datetime.datetime(2014, 4, 6, 17, 7)
end_a = datetime.datetime(2014, 4, 6, 17, 10)

strt_b = datetime.datetime(2014, 4, 7, 17)
mid_b = datetime.datetime(2014, 4, 7, 17, 8)
end_b = datetime.datetime(2014, 4, 7, 17, 10)

plt.subplot(2, 1, 1)
plt.title(str(strt_a))
plot_ticks.plot_tick_range('C:\\Julian\\Prices\\2014\\USD_JPY\\April\\USD_JPY_Week2.csv', strt_a, end_a)
plt.axvline(mid_a, color='r')

plt.subplot(2, 1, 2)
plt.title(str(strt_b))
plot_ticks.plot_tick_range('C:\\Julian\\Prices\\2014\\USD_JPY\\April\\USD_JPY_Week2.csv', strt_b, end_b)
plt.axvline(mid_b, color='r')



plt.show()