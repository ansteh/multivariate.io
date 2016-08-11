import numpy as np
from scipy.interpolate import interp1d
from statsmodels.distributions.empirical_distribution import ECDF

def estimate_pdf(data):
    return np.histogram(data, density=True)

def sample_from(data, size=1):
    """From StackOverflow https://people.duke.edu/~ccc14/sta-663/MonteCarlo.html"""
    ecdf = ECDF(data)
    inv_cdf = extrap1d(interp1d(ecdf.y, ecdf.x, bounds_error=False, assume_sorted=True))
    return inv_cdf(np.random.uniform(0, 1, size))

def extrap1d(interpolator):
    """From StackOverflow http://bit.ly/1BjyRfk"""
    xs = interpolator.x
    ys = interpolator.y

    def pointwise(x):
        if x < xs[0]:
            return ys[0]+(x-xs[0])*(ys[1]-ys[0])/(xs[1]-xs[0])
        elif x > xs[-1]:
            return ys[-1]+(x-xs[-1])*(ys[-1]-ys[-2])/(xs[-1]-xs[-2])
        else:
            return interpolator(x)

    def ufunclike(xs):
        return np.array(map(pointwise, np.array(xs)))

    return ufunclike

class Pdf():
    def __init__(self, column):
        self.column = column
        self.n = np.unique(self.column).size
        self.p, self.x = np.histogram(self.column, bins=self.n, density=True)
        self.bin_width = self.x[1]-self.x[0]
        self.first = self.x[0]
        self.last = self.x[self.x.size-1]

        #print self.p, self.x

    def probability(self, a, b=None):
        if(b is None):
            return self.single(a)
        else:
            return self.intigrate(a, b)

    def single(self, value):
        if((value < self.x[0]) or (value > self.x[self.n])):
            return 0
        else:
            return self.intigrate(value)

    def intigrate(self, a, b=None):
        if(b is None):
            index = self.getIntegralEndIndex(a)
            return self.p[index]*self.bin_width
        else:
            if(a < self.first):
                a = self.first

            if(b > self.last):
                b = self.last

            a = self.x[len(np.where(self.x <= a)[0])-1]
            start = self.x[np.where(self.x < a)].size
            end = self.x[np.where(self.x <= b)].size
            return self.bin_width * np.sum(self.p[start:end])


    def getIntegralEndIndex(self, value):
        sliced = self.x[np.where(self.x >= value)]
        index = self.x.size - sliced.size
        if(index > 0):
            index -= 1
        return index
