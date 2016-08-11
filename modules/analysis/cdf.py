import numpy as np
from statsmodels.distributions.empirical_distribution import ECDF

def estimate_cdf(data):
    return ECDF(data)
