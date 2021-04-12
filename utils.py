from scipy import stats
from itertools import permutations
import math
import numpy as np
import ghalton
import sobol_seq


def _N(dx, sign=1):
    """
    Stand Normal Cumulative Distribution Function
    dx is usually either d1 or d2
    """
    assert abs(1) == 1, "Incorrect input for sign"
    return stats.norm.cdf(dx * sign)

def sum_sum_product(sigmas, rhos):
    sum_val = 0
    rho_i = 0
    for i in range(len(sigmas)):
        for j in range(len(sigmas)):
            if i == j:
                sum_val += sigmas[i] * sigmas[j] # since rho = 1
            else:
                sigmas[i] * sigmas[j] * rhos[rho_i]
                rho_i += 1
    return sum_val

def product(items):
    theproduct = 1
    for item in items:
        theproduct *= item
    return theproduct

def confidence_interval(mu, sigma, M, level=0.95):
    # extension is needed to enable different confidence level
    p = stats.norm.ppf(level)
    return [mu - p*sigma/math.sqrt(M), mu + p*sigma/math.sqrt(M)]

def psuedo_rand_num_generator(size, seed=1126):
    np.random.seed(seed)
    return np.random.normal(size=size)

def quasi_rand_num_generator(size, seed=1126):
    seqr = ghalton.GeneralizedHalton(1, seed)
    X = np.array(seqr.get(size))
    Z = [z[0] for z in stats.norm.ppf(X)]
    return Z

def quasi_rand_num_generator2(size, seed=1126):
    seqr = ghalton.GeneralizedHalton(1, seed)
    X = np.array(seqr.get(size))
    Z = [z[0] for z in stats.norm.ppf(X)]
    return Z
