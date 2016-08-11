import pandas as ps
import numpy as np
import os, sys
sys.path.append('../../modules/')

from analysis.covariance import cov
from analysis.symmetric import isSymmetric
from analysis.definite import isPositiveDefinite
from analysis.correlation import corr
from algorithms.morgan import morgan

data = ps.read_csv(os.path.join(os.path.dirname(__file__), "../resources/apple-tree.csv"), sep = ',')
matrix = data.as_matrix()
matrix = matrix.T
matrix = np.array(matrix, dtype=np.float64)

def testbed():
    C = cov(matrix)
    print np.all(np.diagonal(C) > 0)

    threshold = 1e-6
    print 'symmetric:', isSymmetric(C, threshold)
    print 'positive definite:', isPositiveDefinite(C)
    A = morgan(C)
    #print A
    print C
    print np.dot(A, A.T)
    #print np.subtract(C, np.dot(A, A.T))
    #print C == np.dot(A, A.T)
    #print np.all(C - np.dot(A, A.T) < 1e-6)
    return A
