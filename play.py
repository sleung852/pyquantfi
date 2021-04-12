import math
from scipy.stats import norm
import ghalton
import numpy as np

from blackscholes import EuropeanOptionPricer

params = {
    'S': 10,
    'K': 9,
    'T': 1,
    'sigma': 0.10,
    'r': 0.06
}

# get benchmark
bs = EuropeanOptionPricer(**params)
Ctrue = bs.get_call_premium()

# using Quasi Monte Carlo
factor = params['S'] * np.exp((params['r']-0.5*params['sigma']**2)*params['T'])
std = params['sigma'] * math.sqrt(params['T'])


seed = 2000
seqr = ghalton.GeneralizedHalton(1, seed)
# print(seqr)
# print(seqr.get(int(1e2)))

aMList = []
aMError = []

for M in [1e2, 1e3, 1e4, 1e5, 1e5, 1e6]:
    M = int(M)
    X = np.array(seqr.get(M))
    Z = norm.ppf(X)
    factorArray = std * Z
    sArray = factor * np.exp(factorArray)
    payoffArray = sArray - params['K']
    payoffArray[payoffArray<0] = 0

    aM = np.mean(payoffArray) * np.exp(-params['r'] * params['T'])
    print('the qmc price is ', aM)
    aMList.append(aM)
    aMError.append(Ctrue - aM)

