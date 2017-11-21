# adfuller 


from statsmodels.tsa.stattools import adfuller
from matplotlib import pyplot
import numpy as np
import random as rnd
import math

Y = [rnd.uniform(0, 1) + 0.5*math.sin(x * (2.0/100.0 * 3.14)) for x in range(0, 500)]
X = [rnd.uniform(0, 1) + math.sin(x * (2.0/100.0 * 3.14)) for x in range(0, 500)]

diff = np.subtract(Y, X)

pyplot.plot(X)
pyplot.plot(Y)
pyplot.plot(diff)

pyplot.show()