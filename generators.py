import os, sys
sys.path.append('modules')

import pandas as pd
import numpy as np

from analysis.covariance import cov
from analysis.symmetric import isSymmetric
from analysis.definite import isPositiveDefinite

import generation.normal as normal
import generation.nonnormal as nonnormal
from sampling.libraries import DatasetGenerator

import pylab

import matplotlib.pyplot as plt
import seaborn as sns

#sns.set(color_codes=True)
plt.style.use('ggplot')

class Imitator():
    def __init__(self, filename):
        self.filename = filename
        self.threshold = 1e-6
        self.content = self.get_sample_data()
        # self.matrix = self.content.as_matrix()
        # self.matrix = self.matrix.T
        # self.matrix = np.array(self.matrix, dtype=np.float64)
        # self.C = cov(self.matrix)

    def get_columns(self):
        return list(self.sample.columns.values)

    def get_sample_data(self):
        return pd.read_csv(os.path.join(os.path.dirname(__file__), "resources/"+self.filename), sep = ',')

    def get_data(self, names=None):
        if(names is None):
            data = self.content
        else:
            data = self.content[names]

        data = data.as_matrix()
        data = data.T
        data = np.array(data, dtype=np.float64)
        return data

    def simulate_with_normal(self, size=1, columns=None):
        return normal.simulate(self.get_data(columns), size)

    def simulate_with_nonnormal(self, size=1, columns=None):
        return nonnormal.simulate(self.get_data(columns).T)[:size]

    def simulate(self, size=1, columns=None):
        data = self.get_data(columns)
        C = cov(data)
        if(isSymmetric(C, self.threshold) and isPositiveDefinite(C)):
            return self.simulate_with_normal(size, columns)
        else:
            #return self.simulate_with_normal(size, columns)
            return self.simulate_with_nonnormal(size, columns)

    def save_as_image(self, filename, samples, columns=None, selection=None, xlim=None, ylim=None):
        if(columns is None):
            df = pd.DataFrame(samples, columns=["x", "y"])
            sns.jointplot(x="x", y="y", data=df, kind="reg", xlim=xlim, ylim=ylim)
        else:
            df = pd.DataFrame(samples, columns=columns)
            sns.jointplot(selection[0], selection[1], data=df, kind="reg", xlim=xlim, ylim=ylim)

        pylab.savefig('static/images/'+filename+'.png')
