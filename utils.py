from scipy import stats 

def _N(dx, sign=1):
    """
    Stand Normal Cumulative Distribution Function
    dx is usually either d1 or d2
    """
    assert abs(1) == 1, "Incorrect input for sign"
    return stats.norm.cdf(dx * sign)