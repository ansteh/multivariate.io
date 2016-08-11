import numpy as np
from numpy.linalg import solve
from scipy.stats import moment,norm

def fleishman(b, c, d):
    """calculate the variance, skew and kurtois of a Fleishman distribution
    F = -c + bZ + cZ^2 + dZ^3, where Z ~ N(0,1)
    """
    b2 = b * b
    c2 = c * c
    d2 = d * d
    bd = b * d
    var = b2 + 6*bd + 2*c2 + 15*d2
    skew = 2 * c * (b2 + 24*bd + 105*d2 + 2)
    kurt = 24 * (bd + c2 * (1 + b2 + 28*bd) + d2 * (12 + 48*bd + 141*c2 + 225*d2))
    return (var, skew, kurt)

def flfunc(b, c, d, skew, kurtosis):
    """
    Given the fleishman coefficients, and a target skew and kurtois
    this function will have a root if the coefficients give the desired skew and kurtosis
    """
    x,y,z = fleishman(b,c,d)
    return (x - 1, y - skew, z - kurtosis)

def flderiv(b, c, d):
    """
    The deriviative of the flfunc above
    returns a matrix of partial derivatives
    """
    b2 = b * b
    c2 = c * c
    d2 = d * d
    bd = b * d
    df1db = 2*b + 6*d
    df1dc = 4*c
    df1dd = 6*b + 30*d
    df2db = 4*c * (b + 12*d)
    df2dc = 2 * (b2 + 24*bd + 105*d2 + 2)
    df2dd = 4 * c * (12*b + 105*d)
    df3db = 24 * (d + c2 * (2*b + 28*d) + 48 * d**3)
    df3dc = 48 * c * (1 + b2 + 28*bd + 141*d2)
    df3dd = 24 * (b + 28*b * c2 + 2 * d * (12 + 48*bd +
                  141*c2 + 225*d2) + d2 * (48*b + 450*d))
    return np.matrix([[df1db, df1dc, df1dd],
                      [df2db, df2dc, df2dd],
                      [df3db, df3dc, df3dd]])

def newton(a, b, c, skew, kurtosis, max_iter=25, converge=1e-5):
    """Implements newtons method to find a root of flfunc."""
    f = flfunc(a, b, c, skew, kurtosis)
    for i in range(max_iter):
        if max(map(abs, f)) < converge:
            break
        J = flderiv(a, b, c)
        delta = -solve(J, f)
        (a, b, c) = delta + (a,b,c)
        f = flfunc(a, b, c, skew, kurtosis)
    return (a, b, c)


def fleishmanic(skew, kurt):
    """Find an initial estimate of the fleisman coefficients, to feed to newtons method"""
    c1 = 0.95357 - 0.05679 * skew + 0.03520 * skew**2 + 0.00133 * kurt**2
    c2 = 0.10007 * skew + 0.00844 * skew**3
    c3 = 0.30978 - 0.31655 * c1
    return (c1, c2, c3)


def fit_fleishman_from_sk(skew, kurt):
    """Find the fleishman distribution with given skew and kurtosis
    mean =0 and stdev =1

    Returns None if no such distribution can be found
    """
    if kurt < -1.13168 + 1.58837 * skew**2:
        return None
    a, b, c = fleishmanic(skew, kurt)
    coef = newton(a, b, c, skew, kurt)
    return(coef)

def fit_fleishman_from_standardised_data(data):
    """Fit a fleishman distribution to standardised data."""
    skew = moment(data,3)
    kurt = moment(data,4)
    coeff = fit_fleishman_from_sk(skew,kurt)
    return coeff

def describe(data):
    """Return summary statistics of as set of data"""
    mean = np.mean(data)
    var = moment(data,2)
    skew = moment(data,3)/var**1.5
    kurt = moment(data,4)/var**2
    return (mean,var,skew,kurt)

def generate_fleishman(a,b,c,d,N=100):
    """Generate N data items from fleishman's distribution with given coefficents"""
    Z = norm.rvs(size=N)
    F = a + Z*(b +Z*(c+ Z*d))
    return F

def generate_fleishman_from_collection(data, N=10000):
    mean = np.mean(data)
    std = moment(data,2)**0.5
    std_data = (data - mean)/std

    coeff = fit_fleishman_from_standardised_data(std_data)
    return (generate_fleishman(-coeff[1],*coeff, N=N))*std+mean
