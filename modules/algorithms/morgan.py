import numpy as np

def morgan(C):
    dim = len(C)
    A = np.zeros((dim, dim))
    A[:, 0] = C[:, 0] / np.sqrt(C[0, 0])

    for j in np.arange(1, dim):
        A[j, j] = np.sqrt(C[j, j] - np.sum(A[j, :j] * A[j, :j]))
        for i in np.arange(j+1, dim):
            A[i, j] = C[i, j] - np.sum(A[i, :j] * A[j, :j])
            A[i, j] /= A[j, j]
    return np.nan_to_num(A)
