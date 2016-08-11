import pandas as ps
import numpy as np
import os, sys
sys.path.append('../../modules/')

from analysis.covariance import cov
from analysis.correlation import corr
from analysis.mean import mean
from algorithms.morgan import morgan

def simulate(data, count):
    C = cov(data)
    A = morgan(C)
    Mean = mean(data)
    return np.random.multivariate_normal(Mean, C, count)
