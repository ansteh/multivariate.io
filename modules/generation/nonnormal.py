import pandas as ps
import numpy as np
import os, sys
sys.path.append('../../modules/')

from analysis.covariance import cov
from analysis.correlation import corr
from analysis.mean import mean
from algorithms.morgan import morgan
from sklearn.decomposition import FactorAnalysis
from sklearn import preprocessing

def simulate(data, factors=0, maxtrials=5, multiplier=1, seed=0):
    n = len(data)
    dim = len(data[0])
    simulated = np.zeros((n,dim))
    distribution = np.zeros((n,dim))
    iteration = 0
    BestRMSR = 1
    trialsWithoutImprovement = 0

    #apply distribution from supplied data
    distribution = data.copy()
    TargetCorr = corr(data.T)
    IntermidiateCorr = TargetCorr.copy()
    BestCorr = IntermidiateCorr
    #print data.shape
    #print simulated.shape
    #print TargetCorr, TargetCorr.shape

    if(factors == 0):
        eigvalsObserved = np.linalg.eigvals(IntermidiateCorr)
        eigvalsRandom = np.zeros((100,dim))
        randomData = np.zeros((n,dim))

        for i in range(0, 100):
            for j in range(0, dim):
                randomData[:, j] = np.random.permutation(distribution[:, j])
            eigvalsRandom[i, :] = np.linalg.eigvals(corr(randomData.T))
        eigvalsRandom = np.mean(eigvalsRandom, axis=0)
        factors = max(1, np.sum(eigvalsObserved > eigvalsRandom))

    #steps 5,6
    SharedComp = np.random.normal(0, 1, (n, factors))
    UniqueComp = np.random.normal(0, 1, (n, dim))
    SharedLoad = np.zeros((dim, factors))
    UniqueLoad = np.zeros(dim)

    while trialsWithoutImprovement < maxtrials:
        iteration += 1

        #Calculate factor loadings and apply to reproduce desired correlations (steps 7, 8)
        fa = FactorAnalysis()
        fa.n_components = factors
        fa.fit(IntermidiateCorr)
        FactLoadings = fa.components_.T
        #print FactLoadings.shape

        if (factors == 1):
            SharedLoad[:, 0] = FactLoadings[:, 0]
        else:
            SharedLoad = FactLoadings
        #print SharedLoad

        SharedLoad = np.clip(SharedLoad, -1, 1)
        #print SharedLoad

        if (SharedLoad[0, 0] < 0):
            SharedLoad *= -1
        #print SharedLoad

        SharedLoadSq = SharedLoad * SharedLoad
        #print SharedLoadSq

        for i in range(0, dim):
            SharedLoadSum = np.sum(SharedLoadSq[i, :])
            if(SharedLoadSum < 1):
                UniqueLoad[i] = 1 - SharedLoadSum
            else:
                UniqueLoad[i] = 0
        UniqueLoad = np.sqrt(UniqueLoad)
        #print UniqueLoad

        MergedShare = np.dot(SharedComp, SharedLoad.T)
        for i in range(0, dim):
            simulated[:, i] = MergedShare[:, i] + UniqueComp[:, i]*UniqueLoad[i]
        #print simulated

        #Replace normal with nonnormal distributions (step 9)
        for i in range(0, dim):
            indices = np.argsort(simulated[:, i])
            simulated = np.array(simulated)[indices]
            simulated[:, i] = distribution[:, i]
        #print simulated
        #print distribution

        #Calculate RMSR correlation, compare to lowest value, take appropriate action (steps 10, 11, 12)
        ReproducedCorr = corr(simulated.T)
        ResidualCorr = TargetCorr - ReproducedCorr;
        #print ResidualCorr

        RMSR = np.sqrt(np.sum(np.tril(ResidualCorr) ** 2) / (0.5 * (dim*dim - dim)))
        #print RMSR

        if (RMSR < BestRMSR):
            BestRMSR = RMSR
            BestCorr = IntermidiateCorr
            BestRes = ResidualCorr
            IntermidiateCorr = IntermidiateCorr + multiplier*ResidualCorr
            trialsWithoutImprovement = 0
        else:
            trialsWithoutImprovement += 1
            CurrentMultiplier = multiplier * (0.5 ** trialsWithoutImprovement)
            try:
                IntermidiateCorr = BestCorr + CurrentMultiplier * BestRes
            except NameError:
                BestRes = ResidualCorr
                IntermidiateCorr = BestCorr + CurrentMultiplier * BestRes

    #Construct the data set with the lowest RMSR correlation (step 13)
    fa = FactorAnalysis()
    fa.n_components = factors
    fa.fit(BestCorr)
    FactLoadings = fa.components_.T

    if (factors == 1):
        SharedLoad[:, 0] = FactLoadings[:, 0]
    else:
        SharedLoad = FactLoadings

    SharedLoad = np.clip(SharedLoad, -1, 1)

    if (SharedLoad[0, 0] < 0):
        SharedLoad *= -1

    SharedLoadSq = SharedLoad * SharedLoad

    for i in range(0, dim):
        SharedLoadSum = np.sum(SharedLoadSq[i, :])
        if(SharedLoadSum < 1):
            UniqueLoad[i] = 1 - SharedLoadSum
        else:
            UniqueLoad[i] = 0
    UniqueLoad = np.sqrt(UniqueLoad)

    MergedShare = np.dot(SharedComp, SharedLoad.T)
    for i in range(0, dim):
        simulated[:, i] = MergedShare[:, i] + UniqueComp[:, i]*UniqueLoad[i]

    simulated = preprocessing.scale(simulated)

    for i in range(0, dim):
        indices = np.argsort(simulated[:, i])
        simulated = np.array(simulated)[indices]
        simulated[:, i] = distribution[:, i]

    #return the simulated data set (step 14)
    #print 'RMSR', BestRMSR

    return np.flipud(simulated)
