import numpy as numpy
import pandas as pd 
import math
from scipy import stats 

class OptionCalculator:


    """
    Shared Functions
    """
    
    def store_values(self, S, K, deltaT, sigma, r, q, n):
        self.S = S
        self.K = K
        self.deltaT = deltaT
        self.sigma = sigma
        self.r = r
        self.q = q
        self.n = n

    def _Nd1(self, sign=1):
        assert abs(1) == 1, "Incorrect input for sign"
        d1 = self._d1()
        return stats.norm.cdf(d1 * sign)
    
    def _d1(self):
        return (math.log(self.S/self.K) + (self.r - self.q)*(self.deltaT)) / (self.sigma*math.sqrt(self.deltaT)) + 0.5 * self.sigma * math.sqrt(self.deltaT)

    def _Nd2(self, sign=1):
        assert abs(1) == 1, "Incorrect input for sign"
        d2 = self._d2()
        return stats.norm.cdf(d2 * sign)
    
    def _d2(self):
        return (math.log(self.S/self.K) + (self.r - self.q)*(self.deltaT)) / (self.sigma*math.sqrt(self.deltaT)) - 0.5 * self.sigma * math.sqrt(self.deltaT)

    def vega(self):
        return self.S * math.exp(-self.q * self.deltaT) * math.sqrt(self.deltaT) * self.Nd1_first_derivative()


    """
    For calculating European Call/Put Option Prices
    """

    def european_option_price(self, S, K, deltaT, sigma, r, q=0, kind='C'):
        # should try to remove this function. Doesnt make sense at this stage
        self.store_values(S, K, deltaT, sigma, r, q, n=0)
        assert kind in ['C', 'P'], "Incorrect kind. Can only be 'call' or 'put'"
        if kind == 'C':
            return self.call_price()
        return self.put_price()
        
    def call_price(self):
        c = self.S * math.exp(-self.q * self.deltaT) * self._Nd1() - self.K * math.exp(-self.r * self.deltaT) * self._Nd2()
        return c

    def put_price(self):
        p = self.K * math.exp(-self.r * self.deltaT) * self._Nd2(-1) - self.S * math.exp(-self.q * self.deltaT) * self._Nd1(-1)
        return p
    
    """
    For calculating Implied Volatility
    """

    def newtons_method(self, option_mkt_price, S, K, deltaT, r, q, kind = 'C', tol = 1e-8, epoch=100):
        sigma_hat = math.sqrt(2*abs((math.log(S / K) + (r - q)*deltaT)/deltaT))
        sigma_diff = 1
        n = 1
        sigma = sigma_hat
        while (sigma_diff >= tol and n < epoch):
            option_price = self.vanila_european_price(S, K, deltaT, sigma, r, q, kind=kind)
            Cvega = self.vega()
            increment = (option_price-option_mkt_price)/Cvega
            sigma -= increment
            n += 1
            sigma_diff = abs(increment)
        return sigma

    def Nd1_first_derivative(self):
        """
        For calculating N'(d1)
        """
        d1 = self._d1()
        return 1/((2 * math.pi)**0.5) * math.exp(-(d1**2)/2)

    """
    For calculating the geometric Asian call option
    """ 

    def geo_asian_option_price(self, S, K, sigma, r, deltaT, n, kind = 'C'):
        self.store_values(S, K, deltaT, sigma, r, q=0, n=n)
        sigma_hat = self._sigma_hat()
        mu_hat = self._mu_hat(sigma_hat)
        return math.exp(-self.r * self.deltaT) * (self.S*math.exp(mu_hat*self.deltaT)*self._Nd1)

    def _sigma_hat(self):
        return self.sigma * math.sqrt((self.n+1)*(2*self.n+1)/(6*self.n*self.n))

    def _mu_hat(self, sigma_hat):
        return (self.r - 0.5 * self.sigma**2)*(self.n+1)/(2*self.n) + 0.5*(sigma_hat**2)

