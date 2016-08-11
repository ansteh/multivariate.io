import fleishman_univariate as fm
import numpy as np

def sample_from_matrix(data, N=100):
    Sample = map(lambda column: fm.generate_fleishman_from_collection(column, N), data)
    return np.array(Sample).T
