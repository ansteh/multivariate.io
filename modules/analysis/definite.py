import numpy as np

def isPositiveDefinite(X):
    return np.all(np.linalg.eigvals(X) > 0)
