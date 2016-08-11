import json
import pandas as ps
import numpy as np
import os, sys
import schedule, time

sys.path.append('../../modules/')

import generation.nonnormal as nonnormalGenerator

def load():
    with open("../resources/sampling_numpy.json") as json_file:
        return json.load(json_file)

from sampling.libraries import Sampling

options = load()
columns = options['columns']

sampler = Sampling([
    {
        "name": "normal_example",
        "numpy": {
          "function": "normal",
          "parameters": {
            "loc": 1,
            "scale": 1
          }
        }
    },{
        "name": "normal_example_second",
        "numpy": {
          "function": "normal",
          "parameters": {
            "loc": 1,
            "scale": 1
          }
        }
    }
])

def produceBlueprint():
    sample = sampler.generate(100)
    return {
        'data': sample,
        'cov': np.cov(sample),
        'corr': np.corrcoef(sample)
    }

blueprint = produceBlueprint()
simulated = nonnormalGenerator.simulate(blueprint['data'].T)
# print blueprint['corr'] - np.corrcoef(simulated.T)
# print blueprint['cov'] - np.cov(simulated.T)

print simulated[:4]

# def sample():
#     print sampler.execute(sampler.columns[0])
#
# schedule.every(1).seconds.do(sample)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
