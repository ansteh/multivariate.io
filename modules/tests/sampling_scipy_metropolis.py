import pandas as ps
import numpy as np
import scipy
import os, sys
sys.path.append('../../modules/')

from sampling.libraries import Metropolis_Scipy_Random as Metropolis_Scipy

normScipySampler = Metropolis_Scipy('uniform', { 'loc': 0, 'scale': 1 })
sample =  normScipySampler.sample(1000)

print scipy.stats.uniform.std(loc=0, scale=1), np.std(sample)
