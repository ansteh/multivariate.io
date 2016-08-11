import pandas as ps
import numpy as np
import os, sys
sys.path.append('../../modules/')

from scipy.stats import moment,norm
from algorithms.fleishman_univariate import generate_fleishman_from_collection
from algorithms.fleishman_univariate import generate_fleishman
from algorithms.fleishman_univariate import fit_fleishman_from_standardised_data
from algorithms.fleishman_univariate import describe

with open(os.path.join(os.path.dirname(__file__), "../resources/data.txt")) as f:
    data = np.array([float(line) for line in f])
mean = np.mean(data)
std = moment(data,2)**0.5
std_data = (data - mean)/std

coeff = fit_fleishman_from_standardised_data(std_data)
print(coeff)

print 'coeff:', coeff
print(describe(data))
sim = (generate_fleishman(-coeff[1],*coeff,N=10000))*std+mean
print(describe(sim))

result = generate_fleishman_from_collection(data, 1000)
print describe(result), len(result)
