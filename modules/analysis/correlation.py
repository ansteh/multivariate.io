import numpy as np

def corr(matrix):
    return np.nan_to_num(np.corrcoef(matrix))
