import matplotlib.pyplot as plt
import pylab
import numpy as np
import scipy.stats as stats
plt.style.use('ggplot')

import os, sys
sys.path.append('../../modules/')

from analysis.pdf import sample_from

# Make up some random data
#x = np.concatenate([np.random.normal(0, 1, 10000), np.random.normal(4, 1, 10000)])
x = np.random.chisquare(2, 10000)

samples = sample_from(x, 1000)

plt.hist(x, 50, histtype='step', color='red', normed=True, linewidth=1)
plt.hist(samples, 50, histtype='step', color='blue', normed=True, linewidth=1)

plt.show()

#print np.random.uniform(-4, 4, 10)

# h_true =1 - stats.norm().cdf(5)
#
# n = 10000
# y = stats.norm().rvs(n)
# h_mc = 1.0/n * np.sum(y > 5)
# # estimate and relative error
# print h_mc, np.abs(h_mc - h_true)/h_true
#
# n = 10000
# y = stats.expon(loc=5).rvs(n)
# h_is = 1.0/n * np.sum(stats.norm().pdf(y)/stats.expon(loc=5).pdf(y))
# # estimate and relative error
# print h_is, np.abs(h_is- h_true)/h_true

pylab.show()
