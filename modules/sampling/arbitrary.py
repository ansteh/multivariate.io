import numpy as np

class Sampling():
    def __init__(self, column):
        self.column = column
        self.n = column.size

    def next(self, size=None):
        q = np.random.randint(0, 101, size=size)
        if(q is np.array):
            return map(lambda weight: np.percentile(self.column, weight), q)
        else:
            return np.percentile(self.column, q)
