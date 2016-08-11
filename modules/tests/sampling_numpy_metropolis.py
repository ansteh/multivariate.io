import pandas as ps
import numpy as np
import scipy
import os, sys
import json
import matplotlib.pyplot as plt
import pylab

plt.style.use('ggplot')

sys.path.append('../../modules/')

from sampling.libraries import Metropolis_Numpy_Random as Metropolis_Numpy
from sampling.libraries import Metropolis_Mixture_Representation
def load():
    with open("../resources/sampling_numpy.json") as json_file:
        return json.load(json_file)

normNumpySampler = Metropolis_Numpy('uniform', { 'low': 0, 'high': 1 })
N = 10000
# print np.random.uniform(0, 1, N).shape
# sample = normNumpySampler.sample(N)
# print 'unique', np.unique(sample).size, 'of ', N, np.unique(np.random.uniform(0, 1, N)).size
# std_true = scipy.stats.uniform.std(loc=0, scale=1)
# std_sampled = np.std(sample)
# print 'std', std_true, std_sampled, abs(std_true - std_sampled)
# mean_sampled = np.mean(sample)
# mean_true = scipy.stats.uniform.mean(loc=0, scale=1)
# print 'mean', mean_true, mean_sampled, abs(mean_true - mean_sampled)
#
# plt.hist(np.random.uniform(0, 1, N), 25, histtype='step', color='red', normed=True, linewidth=1)
# plt.hist(np.random.uniform(0, 1, N), 25, histtype='step', color='blue', normed=True, linewidth=1)
# plt.hist(map(lambda x: np.random.uniform(0, 1), range(N)), 25, histtype='step', color='green', normed=True, linewidth=1)
# plt.hist(sample, 25, histtype='step', color='black', normed=True, linewidth=1)
#
# plt.show()

#Metropolis_Mixture_Representation
# print 'Metropolis_Mixture_Representation:'
# mixture = Metropolis_Mixture_Representation(load()['columns'][0]['mixture_representation'])
# samples = mixture.sample(N, unique=True)
# print 'column 0 samples:', samples.shape, 'unique', np.unique(samples).size, np.unique(samples)
# mean_true, mean_sample = scipy.stats.poisson.var(loc=0, mu=5), np.mean(samples)
# print 'mean', mean_true, mean_sample, abs(mean_true - mean_sample)
# std_sampled = np.std(samples)
# std_true = scipy.stats.poisson.var(loc=0, mu=5)
# print 'std', std_true, std_sampled, abs(std_true - std_sampled)
#
# plt.hist(scipy.stats.poisson.rvs(loc=0, mu=5, size=1000), 20, histtype='step', color='red', normed=True, linewidth=1)
# plt.hist(samples, 20, histtype='step', color='blue', normed=True, linewidth=1)
#
# plt.show()

mixture = Metropolis_Mixture_Representation(load()['columns'][1]['mixture_representation'])
samples = mixture.sample(N, unique=True)
print 'column 1 samples:', samples.shape, 'unique', np.unique(samples).size #, samples
std_true = 0.7*scipy.stats.norm.std(loc=0, scale=1)+0.3*scipy.stats.beta.std(1, 3, scale=1, loc=0)
std_sampled = np.std(samples)
print 'std:', std_true, std_sampled, abs(std_true - std_sampled)/std_true*100
mean_sampled = np.mean(samples)
mean_true = 0.7*scipy.stats.norm.mean(loc=0, scale=1)+0.3*scipy.stats.beta.mean(1, 3, scale=1, loc=0)
print 'mean:', mean_true, mean_sampled, abs(mean_true - mean_sampled)/mean_true*100

plt.hist(0.7*scipy.stats.norm.rvs(loc=0, scale=1, size=N)+0.3*scipy.stats.beta.rvs(1, 3, scale=1, loc=0, size=N), 20, histtype='step', color='red', normed=True, linewidth=1)
plt.hist(samples, 20, histtype='step', color='black', normed=True, linewidth=1)
plt.hist(0.7*scipy.stats.norm.rvs(loc=0, scale=1, size=N)+0.3*scipy.stats.beta.rvs(1, 3, scale=1, loc=0, size=N), 20, histtype='step', color='blue', normed=True, linewidth=1)
plt.hist(0.7*scipy.stats.norm.rvs(loc=0, scale=1, size=N)+0.3*scipy.stats.beta.rvs(1, 3, scale=1, loc=0, size=N), 20, histtype='step', color='green', normed=True, linewidth=1)

plt.show()

pylab.show()
