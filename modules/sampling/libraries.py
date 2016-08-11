import numpy as np
import scipy
import math
import scipy.stats as stats
from analysis.pdf import estimate_pdf
from analysis.pdf import Pdf
from analysis.pdf import sample_from as sample_cdf_from

class Metropolis():
    def sample(self, size=1, unique=False):
        #print hasattr(self, 'mixtures'), self.all_native, (hasattr(self, 'probability') == False)
        if(hasattr(self, 'mixtures') and self.all_native and (hasattr(self, 'target_probability') == False)):
            return self.rvs(size)

        if(unique):
            return self.sampleUniques(size)
        else:
            return self.metropolis(size)

    def sampleUniques(self, size=1):
        samples = np.unique(self.metropolis(size))
        while(samples.size < size):
            samples = np.append(samples, np.unique(self.metropolis(size)))
        return samples[:size]

    def metropolis(self, size=1):
        if(hasattr(self, 'target_probability') == False):
            return self.rvs(size)

        #print 'metropolis is used', self.probabilityStr
        samples = np.zeros(size)

        last = self.rvs(1)

        for i in range(size):
            u = np.random.uniform()
            x = self.rvs(1)

            #print self.target_probability(x), self.probability(last)
            # if(u < min(1, (self.probability(x)*self.probability(last, x)) / (self.probability(last)*self.probability(x, last)) )):
            if(u < min(1, self.target_probability(x) / self.probability(last))):
                last = x

            samples[i] = last

        return samples

class Metropolis_Scipy_Random(Metropolis):
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters
        self.function = getattr(stats, self.name)
        self.rvs = lambda size: self.function.rvs(size=size, **parameters)


        #self.pdf = lambda x: self.function.pdf(x, **parameters)
        if(hasattr(self.function, 'cdf')):
            self.cdf = lambda x: self.function.cdf(x, **parameters)
        else:
            self.init_cdf(self.rvs(1000))

    def init_cdf(data):
        data_cdf = sample_cdf_from(data)
        self.p, self.x = np.histogram(data_cdf, bins=data_cdf.size, density=True)
        self.bin_width = self.x[1]-self.x[0]
        self.min = self.x[0]

    def probability(self, a, b):
        if(a == b):
            return self.cdf(a)

        if(a < b):
            return self.cdf(b)-self.cdf(a)
        else:
            return self.cdf(a)-self.cdf(b)

class Metropolis_Numpy_Random(Metropolis):
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters
        self.function = getattr(np.random, self.name)

        data = self.rvs(1000)
        self.pdf_estimator = Pdf(data)
        #self.init_cdf(data)

    def init_cdf(data):
        data_cdf = sample_cdf_from(data)
        self.p, self.x = np.histogram(data_cdf, bins=data_cdf.size, density=True)
        self.bin_width = self.x[1]-self.x[0]
        self.min = self.x[0]

    def rvs(self, size=1):
        return self.function(size=size, **self.parameters)

    def pdf(self, x):
        return self.pdf_estimator.probability(x)

    def cdf(self, x):
        index = len(np.where(self.x <= x)[0])
        return self.bin_width*self.p[:index]

    def probability(self, a, b):
        if(a == b):
            return self.cdf(a)

        if(a < b):
            return self.cdf(b)-self.cdf(a)
        else:
            return self.cdf(a)-self.cdf(b)

class Metropolis_Mixture_Representation(Metropolis):
    def __init__(self, columnOptions, probabilityStr=None):
        self.options = columnOptions
        self.p_of_mixtures = map(lambda options: options['mixture_p'], self.options)
        self.p_of_mixtures = np.array(self.p_of_mixtures)
        self.mixtures = map(lambda options: self.create_metropolis_module(options), self.options)
        self.all_native = self.mixtures_are_native()

        self.probabilityStr = probabilityStr
        if((probabilityStr is None) == False):
            self.target_probability = lambda x: eval(probabilityStr)

    def mixtures_are_native(self):
        instances = map(lambda mixture: isinstance(mixture, Metropolis_Numpy_Random) or isinstance(mixture, Metropolis_Scipy_Random), self.mixtures)
        return np.all(instances)

    def create_metropolis_module(self, representation):
        if(representation['module'] == 'numpy'):
            return Metropolis_Numpy_Random(representation['function'], representation['parameters'])
        if(representation['module'] == 'scipy'):
            return Metropolis_Scipy_Random(representation['function'], representation['parameters'])

    def rvs(self, size=1):
        values = np.array(map(lambda mixture: mixture.rvs(size), self.mixtures))
        #print values.shape, range(size), self.p_of_mixtures
        if(size == 1):
            return np.sum(self.p_of_mixtures * values)
        else:
            return np.array(map(lambda i: np.sum(self.p_of_mixtures * values[:, i]), range(size)))

    def pdf(self, x):
        pdfs = map(lambda mixture: mixture.pdf(x), self.mixtures)
        return np.sum(self.p_of_mixtures * pdfs)

    def cdf(self, x):
        cdfs = map(lambda mixture: mixture.cdf(x), self.mixtures)
        return np.sum(self.p_of_mixtures * cdfs)

    def probability(self, a, b=None):
        if(b is None):
            b = a

        if(a == b):
            return self.cdf(a)

        if(a < b):
            return self.cdf(b)-self.cdf(a)
        else:
            return self.cdf(a)-self.cdf(b)

class Monte_Carlo():

    def sample(self, size=1):
        if(hasattr(self, 'probability') == False):
            return self.rvs(size)

        candidates = self.rvs(size).tolist()
        samples = []
        count = 0

        while(count < size):
            if(len(candidates) == 0):
                candidates = self.rvs(size).tolist()

            x = candidates[0]
            candidates.remove(x)

            #print 'mv probability', self.probability(x)
            if(np.random.uniform() < self.probability(x)):
                count += 1
                samples.append(x)

        return np.array(samples)

class DatasetGenerator(Monte_Carlo):
    def __init__(self, columnsOptions, probabilityStr=None):
        self.columnsOptions = columnsOptions
        self.columns = map(lambda option: self.create_column_representation(option), self.columnsOptions)
        self.n = len(self.columns)
        self.columns_range = range(len(self.columns))

        if((probabilityStr is None) == False):
            self.probability = lambda x: eval(probabilityStr)

    def create_column_representation(self, columnOption):
        mixtureOptions = columnOption['mixture_representation']
        if('uv_probability' in columnOption.keys()):
            return Metropolis_Mixture_Representation(mixtureOptions, columnOption['uv_probability'])
        else:
            return Metropolis_Mixture_Representation(mixtureOptions)

    def rvs(self, size=1):
        if(size == 1):
            return np.array(map(lambda c: c.sample(),self.columns))
        else:
            row_of_elemnts = np.array(map(lambda c: c.sample(size), self.columns))
            return row_of_elemnts.T
        # recursion produces a lot of discrepancy in mean and std if sampled by each one
        # if(size == 1):
        #     return np.array(map(lambda c: c.sample(),self.columns))
        # else:
        #     return np.array(map(lambda i: self.rvs(), range(size)))

    # def pdf(self, x):
    #     pdfs = np.array(map(lambda i: self.columns[i].pdf(x[i]), self.columns_range))
    #     return np.sum(pdfs/np.max(pdfs))/self.n

class Native_Numpy_Sampling():
    def __init__(self, columnOptions):
        self.options = columnOptions
        self.name = columnOptions['name']
        self.parameters = self.options['parameters']

        if(self.options['module'] == 'numpy'):
            self.function = getattr(np.random, self.name)
            self.sample = lambda size: self.function(size=size, **parameters)

        if(self.options['module'] == 'scipy'):
            self.function = getattr(stats, self.name)
            self.sample = lambda size: self.function.rvs(size=size, **parameters)

class Sampling():
    def __init__(self, columnsOptions):
        self.columns = columnsOptions
        # print self.create_integral_func_by("5*x")(0,1)
        # print self.create_integral_func_by("5*x")(-np.inf,1)
        # x = -np.inf
        # print eval('math.exp(2)')
        # print eval('np.exp(-x)')

    def execute(self, column, size=1):
        if(column.has_key('numpy')):
            return self.sampleColumnByModule('numpy', column, size)
        if(column.has_key('stats')):
            return self.sampleColumnByModule('stats', column, size)
        if(column.has_key('arbitrary_pdf')):
            self.sample_arbitrary_pdf(column['arbitrary_pdf'], size)
            return np.random.uniform(-1, 0, size)

    def sampleColumnByModule(self, moduleName, column, size=1):
        function = column[moduleName]['function']
        parameters =  column[moduleName]['parameters']
        parameters['size'] = size

        if(moduleName == 'numpy'):
            module = np.random

        if(moduleName == 'stats'):
            module = scipy.stats

        return getattr(module, function)(**parameters)

    def generate(self, size=1):
        data = []
        map(lambda column: data.append(self.execute(column, size)), self.columns)
        return np.array(data)

    def sample_arbitrary_pdf(self, pdfFuncStr, size=1):
        sampler = IntegralSimulation(pdfFuncStr)

    def create_integral_func_by(self, funcStr):
        return lambda a, b: scipy.integrate.quad(lambda x: eval(funcStr), a, b)[0]

class IntegralSimulation():
    def __init__(self, pdfFuncStr):
        self.code = pdfFuncStr
        self.func = lambda a, b: scipy.integrate.quad(lambda x: eval(self.code), a, b)[0]
        self.tail = self.func(-np.inf,0)

        for index, x in np.ndenumerate(np.random.uniform(1,0,1000)):
            print x, self.intigrate_cmf(x)

    def intigrate_cmf(self, x):
        if(x>=0):
            return self.tail + self.func(0,x)
        else:
            return self.tail - self.func(x,0)
