import matplotlib.pyplot as plt
import pylab
import numpy as np

plt.style.use('ggplot')

import os, sys
sys.path.append('../../modules/')

from analysis.pdf import estimate_pdf

# Make up some random data
#x = np.concatenate([np.random.normal(0, 1, 10000)])
x = np.random.chisquare(2,1000)

pdf = estimate_pdf(x)
print pdf

hist = pdf[0]
bins = pdf[1]
width = (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.bar(center, hist, align='center', width=width)
plt.show()

pylab.show()
