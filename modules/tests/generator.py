import pandas as ps
import numpy as np
import os, sys
sys.path.append('../../modules/')

import generation.normal as generator
import generation.nonnormal as nonnormalGenerator
import analysis.deviation as deviation
from analysis.covariance import cov
from analysis.correlation import corr
from analysis.mean import mean
import algorithms.fleishman_multivariate as fm
from sampling.arbitrary import Sampling
from monte_carlo.arbitrary.univariate import Metropolis as UnivariateMetropolis
from algorithms.fleishman_univariate import generate_fleishman_from_collection
from algorithms.fleishman_multivariate import sample_from_matrix as fm_mv_from_matrix

def getNormalDistrubutedData():
    data = ps.read_csv(os.path.join(os.path.dirname(__file__), "../resources/apple-tree.csv"), sep = ',')
    matrix = data.as_matrix()
    matrix = matrix.T
    matrix = np.array(matrix, dtype=np.float64)
    return matrix

def testNormalDistributedGenerator():
    matrix = getNormalDistrubutedData()
    simulated = generator.simulate(matrix, 1000000)
    #print simulated
    threshold = 1e-02
    print deviation.conforms(mean(matrix), mean(simulated.T), threshold)
    print deviation.conforms(cov(matrix), cov(simulated.T), 1e-01)
    print deviation.disparity(cov(matrix), cov(simulated.T))

def getNonNormalDistrubutedData():
    data = ps.read_csv(os.path.join(os.path.dirname(__file__), "../resources/WIKI-FB.csv"), sep = ',')
    matrix = data.as_matrix()
    matrix = matrix[:, 1:]
    matrix = np.array(matrix, dtype=np.float64)
    return matrix

def testNonNormalDistributedGenerator():
    data = getNonNormalDistrubutedData()
    simulated = nonnormalGenerator.simulate(data)
    print simulated.shape
    print corr(data) - corr(simulated)
    return simulated

def testNormalVsIterativeGeneration():
    matrix = getNormalDistrubutedData()
    N = 10
    normalSampled = generator.simulate(matrix, N)
    iterativeSampled = nonnormalGenerator.simulate(matrix.T)
    print normalSampled.shape
    print iterativeSampled.shape

    #print matrix, matrix[:, :2], cov(matrix[:, :2])
    print cov(matrix[:, :5])

    print cov(matrix)
    print cov(normalSampled.T)
    print cov(iterativeSampled.T)

    threshold = 1
    print deviation.conforms(mean(matrix), mean(normalSampled.T), threshold), deviation.conforms(mean(matrix), mean(iterativeSampled.T), threshold)
    print deviation.conforms(cov(matrix), cov(normalSampled.T), 1e-01), deviation.conforms(cov(matrix), cov(iterativeSampled.T), 1e-01)
    print deviation.conforms(corr(matrix), corr(normalSampled.T), threshold), deviation.conforms(corr(matrix), corr(iterativeSampled.T), threshold)

def testFleishmanGenerator():
    data = getNormalDistrubutedData()
    Sample = fm.sample_from_matrix(data)
    print Sample

def testArbitrarySampling():
    data = getNormalDistrubutedData()
    sampler = Sampling(data[0])
    print data[0]
    print sampler.next()
    print sampler.next(10)

def testUnivariateMetropolis():
    data = np.random.uniform(0, 1, 10000)
    metropolis = UnivariateMetropolis(data)
    sampled = metropolis.sample(100)
    print sampled
    print np.mean(data), np.mean(sampled)

def testMultivariateFleishman():
    data = getNonNormalDistrubutedData()[:, 1:].T
    sampled = fm_mv_from_matrix(data, 100)
    print data.shape
    print cov(data)
    print sampled.shape
    print cov(data).shape
    print cov(sampled.T).shape
    print deviation.disparity(cov(data), cov(sampled.T))

def testUnivariateMetropolisWithComparison():
    data = getNormalDistrubutedData()
    metropolis = UnivariateMetropolis(data[0])
    # print data[0]
    # print metropolis.sample(10)
    # data = getNonNormalDistrubutedData()
    # print data.shape
    # print data[:, 1].size

    slicedData = getNonNormalDistrubutedData()[:, 1]
    means = []
    covs = []
    stds = []

    for i in range(100):
        metropolis = UnivariateMetropolis(slicedData)
        N = 100
        sampled = metropolis.sample(N)
        sampler = Sampling(slicedData)
        simpleSampling = sampler.next(N)
        fmSample = generate_fleishman_from_collection(slicedData, N)
        # print 'N=', N
        # print '                data     metropolis    simple sampling   fleishman'
        # print 'unique samples  ', np.unique(slicedData).size, '         ', np.unique(sampled).size, '         ', np.unique(sampled).size, '          ',np.unique(fmSample).size
        # print 'covariance      ', cov(slicedData), cov(sampled), cov(simpleSampling), cov(fmSample)
        # print 'diff covariance ', cov(slicedData)-cov(slicedData), abs(cov(slicedData)-cov(sampled)), abs(cov(slicedData)-cov(simpleSampling)), abs(cov(slicedData)-cov(fmSample))
        means.append([np.mean(slicedData), np.mean(sampled), np.mean(simpleSampling), np.mean(fmSample)])
        covs.append([np.cov(slicedData), np.cov(sampled), np.cov(simpleSampling), np.cov(fmSample)])
        stds.append([np.std(slicedData), np.std(sampled), np.std(simpleSampling), np.std(fmSample)])

    means = np.array(means)
    #print means
    print 'means statistics:'
    print 'statistic data        metropolis          simple sampling          fleishman'
    print 'std      ', np.std(means[:, 0]), '       ', np.std(means[:, 1]), '       ', np.std(means[:, 2]), '       ', np.std(means[:, 3])
    print 'cov      ', np.cov(means[:, 0]), '       ', np.cov(means[:, 1]), '       ', np.cov(means[:, 2]), '       ', np.cov(means[:, 3])
    print 'mean     ', np.mean(means[:, 0]), ' ', np.mean(means[:, 1]), '       ', np.mean(means[:, 2]), '       ', np.mean(means[:, 3])

    print ''
    print ''
    covs = np.array(covs)
    #print means
    print 'covs statistics:'
    print 'statistic   data    metropolis   simple sampling     fleishman'
    print 'std', np.std(covs[:, 0]), '    ', np.std(covs[:, 1]), np.std(covs[:, 2]), '    ', np.std(covs[:, 3])
    print 'cov', np.cov(covs[:, 0]), '    ', np.cov(covs[:, 1]), np.cov(covs[:, 2]), '    ', np.cov(covs[:, 3])
    print 'mean', np.mean(covs[:, 0]), np.mean(covs[:, 1]), np.mean(covs[:, 2]), '    ', np.mean(covs[:, 3])

    stds = np.array(stds)
    #print means
    # print 'stds statistics:'
    # print 'statistic   data    metropolis   simple sampling     fleishman'
    # print 'std', np.std(stds[:, 0]), '    ', np.std(stds[:, 1]), np.std(stds[:, 2]), '    ', np.std(stds[:, 3])
    # print 'cov', np.cov(stds[:, 0]), '    ', np.cov(stds[:, 1]), np.cov(stds[:, 2]), '    ', np.cov(stds[:, 3])
    # print 'mean', np.mean(stds[:, 0]), np.mean(stds[:, 1]), np.mean(stds[:, 2]), '    ', np.mean(stds[:, 3])
    print ''
    print ''
    print 'statistic   data    metropolis   simple sampling     fleishman'
    print 'stds statistics:'
    print 'std', np.std(stds, axis=0)
    print 'mean', np.mean(stds, axis=0)
