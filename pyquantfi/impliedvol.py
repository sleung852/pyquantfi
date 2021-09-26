from .utils import _N
from .blackscholes import EuropeanOptionPricer
import math   
    
class ImpliedVolatilityEstimator:
    def __init__(self, S, K, T, r, q=0):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.q = q
    
    
    def get_implied_vol(self, option_mkt_price, kind = 'C', tol = 1e-8, epoch=100):
        """
        Return Implied Volatility using Newton's Method
        """
        sigma_hat = math.sqrt(2*abs((math.log(self.S / self.K) + (self.r - self.q)*self.T)/self.T))
        sigma_diff = 1
        n = 1
        sigma = sigma_hat
        while (sigma_diff >= tol and n < int(epoch)):
            option_pricer = EuropeanOptionPricer(self.S, self.K, self.T, sigma, self.r, self.q)
            option_price = option_pricer.get_option_premium(kind=kind)
            Cvega = option_pricer.vega()
            increment = (option_price-option_mkt_price)/Cvega
            sigma -= increment
            n += 1
            sigma_diff = abs(increment)
        return sigma