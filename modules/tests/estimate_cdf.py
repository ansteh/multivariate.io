import matplotlib.pyplot as plt
import pylab
import numpy as np

plt.style.use('ggplot')

import os, sys
sys.path.append('../../modules/')

from analysis.cdf import estimate_cdf

# Make up some random data
x = np.concatenate([np.random.normal(0, 1, 10000),np.random.normal(4, 1, 10000)])

ecdf = estimate_cdf(x)
plt.plot(ecdf.x, ecdf.y)

pylab.show()
