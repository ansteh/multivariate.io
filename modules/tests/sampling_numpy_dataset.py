import pandas as ps
import numpy as np
import scipy
import os, sys
import json
import matplotlib.pyplot as plt
import pylab
import pandas as pd
import seaborn as sns
sns.set(color_codes=True)

plt.style.use('ggplot')

sys.path.append('../../modules/')

from sampling.libraries import Metropolis_Numpy_Random as Metropolis_Numpy
from sampling.libraries import DatasetGenerator
def load():
    with open("../resources/sampling_native_numpy.json") as json_file:
        return json.load(json_file)

N = 1000

generator = DatasetGenerator(load()['columns'])

samples = generator.rvs(N)

std_sampled = np.std(samples[:,0])
std_true = scipy.stats.poisson.std(mu=5, loc=0)
print 'std', std_true, std_sampled, abs(std_true - std_sampled)/std_true*100
mean_true, mean_sample = scipy.stats.poisson.mean(mu=5, loc=0), np.mean(samples[:,0])
print 'mean', mean_true, mean_sample, abs(mean_true - mean_sample)/mean_true*100

std_true = 0.7*scipy.stats.norm.std(loc=0, scale=1)+0.3*scipy.stats.beta.std(1, 3, scale=1, loc=0)
std_sampled = np.std(samples[:,1])
print 'std:', std_true, std_sampled, abs(std_true - std_sampled)/std_true*100
mean_sampled = np.mean(samples[:,1])
mean_true = 0.7*scipy.stats.norm.mean(loc=0, scale=1)+0.3*scipy.stats.beta.mean(1, 3, scale=1, loc=0)
print 'mean:', mean_true, mean_sampled, abs(mean_true - mean_sampled)/mean_true*100

references = 2
containers = map(lambda i: np.array([scipy.stats.poisson.rvs(mu=5, loc=0, size=N), 0.7*scipy.stats.norm.rvs(loc=0, scale=1, size=N)+0.3*scipy.stats.beta.rvs(1, 3, scale=1, loc=0, size=N)]).T, range(references))


def plot(references, containers):
    xlim = (np.min(samples[:, 0]), np.max(samples[:, 0]))
    ylim = (np.min(samples[:, 1]), np.max(samples[:, 1]))
    for i in range(references):
        xlim = (min(xlim[0], np.min(containers[i][:, 0])), max(xlim[1], np.max(containers[i][:, 0])))
        ylim = (min(ylim[0], np.min(containers[i][:, 1])), max(ylim[1], np.max(containers[i][:, 1])))

    xlim = (xlim[0]-1, xlim[1]+1)
    ylim = (ylim[0]-1, ylim[1]+1)

    df = pd.DataFrame(samples, columns=["x", "y"])
    sns.jointplot(x="x", y="y", data=df, xlim=xlim, ylim=ylim)

    for i in range(references):
        df = pd.DataFrame(containers[i], columns=["x", "y"])
        sns.jointplot(x="x", y="y", data=df, xlim=xlim, ylim=ylim)

plot(references, containers)

pylab.show()
