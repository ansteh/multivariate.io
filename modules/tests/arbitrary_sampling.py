import pandas as ps
import numpy as np
import os, sys
sys.path.append('../../modules/')

from sampling.arbitrary import Sampling

def sample_from(column):
    sampler = Sampling(column)
    return sampler.next()
