import numpy as np

def disparity(A, B):
    return abs(np.subtract(A, B))

def conforms(A, B, threshold):
    return np.all(disparity(A, B) < threshold)
