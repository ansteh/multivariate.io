import pandas as ps
import numpy as np
import time

from analysis.correlation import corr
from analysis.covariance import cov
from analysis.symmetric import isSymmetric
from analysis.definite import isPositiveDefinite
from discrete.transformation import test
#from algorithms.morgan import morgan
import tests.morgan as morgan
import tests.generator as generator

data = ps.read_csv("resources/WIKI-FB.csv", sep = ',')
#data = ps.read_csv("apple-tree.csv", sep = ',')

matrix = data.as_matrix()
matrix = matrix[:, 1:]
matrix = matrix.T
matrix = np.array(matrix, dtype=np.float64)
#matrix = np.nan_to_num(matrix)

#dim = 5
#matrix = matrix[:dim,:dim]

#print matrix
#print cov(matrix)
#print corr(matrix)

#generator.testNormalDistributedGenerator()
#generator.testNonNormalDistributedGenerator()
#generator.testFleishmanGenerator()
#generator.testArbitrarySampling()
#generator.testUnivariateMetropolisWithComparison()
#generator.testNormalVsIterativeGeneration()
#generator.testUnivariateMetropolis()
#generator.testMultivariateFleishman()

def testMorgan():
    morgan.testbed()
#testMorgan()

# start_time = time.time()
# generator.testNonNormalDistributedGenerator()
# elapsed_time = time.time() - start_time
# print elapsed_time
#
# k = 5
# np.random.seed(1)
# true_std = np.random.randn(k)
# true_mean = np.random.randn(k)
# true_cov = np.eye(k) * np.outer(true_std, true_std)
# n = 10000
#
# np.random.seed(1)
# vals = np.random.multivariate_normal(true_mean, true_cov, n)
#
# print true_cov
# print vals.shape, vals[0]
