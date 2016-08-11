from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt

import pandas as ps
import numpy as np
import scipy
import os, sys
import json
import matplotlib.pyplot as plt
import pylab
import pandas as pd
import seaborn as sns
from mpl_toolkits.mplot3d import axes3d

sns.set(color_codes=True)

plt.style.use('ggplot')

sys.path.append('../../modules/')

from sampling.libraries import Metropolis_Numpy_Random as Metropolis_Numpy
from sampling.libraries import DatasetGenerator
def load():
    with open("../resources/sampling_native_numpy_3d.json") as json_file:
        return json.load(json_file)

N = 1000

generator = DatasetGenerator(load()['columns'])
samples = generator.rvs(N)

# fig = plt.figure()
# ax = fig.gca(projection='3d')
# X = np.arange(-5, 5, 0.25)
# Y = np.arange(-5, 5, 0.25)
# X, Y = np.meshgrid(X, Y)
# R = np.sqrt(X**2 + Y**2)
# Z = np.sin(R)
# print X.shape
# print Y.shape
# print Z.shape
# surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
#                        linewidth=0, antialiased=False)
# ax.set_zlim(-1.01, 1.01)
#
# ax.zaxis.set_major_locator(LinearLocator(10))
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
#
# fig.colorbar(surf, shrink=0.5, aspect=5)
#
# plt.show()

# X, Y = np.meshgrid(samples[:,1], samples[:,2])
# Z = np.meshgrid(samples[:,2], samples[:,0])[1]

def make3d(data, permutation):
    X, Y = np.meshgrid(data[:,permutation[0]], data[:,permutation[1]])
    Z = np.meshgrid(data[:,permutation[1]], data[:,permutation[2]])[1]
    return X, Y, Z

X, Y, Z = make3d(samples, [1, 2, 1])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(samples[:,0], samples[:,1], samples[:,2], c='r', marker='o')

pylab.show()
