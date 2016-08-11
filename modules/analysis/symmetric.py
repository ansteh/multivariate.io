import numpy as np
from scipy import stats

def isSymmetric(X, threshold=0):
    return np.all(abs(X - X.T) < threshold)
