import pandas as ps
import numpy as np
import os, sys
sys.path.append('../../modules/')

def getNormalDistrubutedData():
    data = ps.read_csv(os.path.join(os.path.dirname(__file__), "../resources/apple-tree.csv"), sep = ',')
    matrix = data.as_matrix()
    matrix = matrix.T
    matrix = np.array(matrix, dtype=np.float64)
    return matrix

data = getNormalDistrubutedData()

import numpy as np
from scipy.interpolate import UnivariateSpline
from matplotlib import pyplot as plt
from analysis.pdf import Pdf

pdf = Pdf(data[0])

print 3.3, pdf.probability(3.3)
print pdf.probability(6.8)
print pdf.probability(3.4)
print pdf.probability(4.40)
print pdf.probability(6.5)
print 3.3, 3.3, '=', pdf.probability(3.3, 3.3)
print 3.3, 3.4, '=', pdf.probability(3.3, 3.4)
print 3.4, 3.5, '=', pdf.probability(3.4, 3.5)
print 3.3, 3.65, '=', pdf.probability(3.3, 3.65)
print 3.4, 6.5, '=', pdf.probability(3.4, 6.5)
print 3.4, 6.3, '=', pdf.probability(3.4, 6.3)
print 3.3, 6.8, '=', pdf.probability(3.3, 6.8)
print 5.2, 6.8, '=', pdf.probability(5.2, 6.8)
print 0, 10, '=', pdf.probability(0, 10)
#print 6, 4, '=', pdf.probability(6, 4)
