from scipy import stats
from itertools import permutations
import math


def _N(dx, sign=1):
    """
    Stand Normal Cumulative Distribution Function
    dx is usually either d1 or d2
    """
    assert abs(1) == 1, "Incorrect input for sign"
    return stats.norm.cdf(dx * sign)

def cross_sum_product(sigmas, rhos):
    sum_val = 0
    sigmas_set = permutations(sigmas)
    assert len(rhos) == len(sigmas_set), "Size of sigmas do not match with size of rhos"
    for sigmas_set, rho in zip(sigmas_sets, rhos):
        sum_val *= product(sigmas_set) * rho
    return sum_val 

def product(items):
    theproduct = 1
    for item in items:
        theproduct *= item
    return theproduct

def confidence_interval(mu, sigma, M, level=0.95):
    # extension is needed to enable different confidence level
    return [mu - 1.96*sigma/math.sqrt(M), mu + 1.96*sigma/math.sqrt(M)]

def psuedo_rand_no():
    pass

def quasi_rand_no():
    pass

