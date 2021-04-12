from utils import _N
import math

class EuropeanOptionPricer:
    def __init__(self, S, K, T, sigma, r, q=0):
        self.S = S
        self.K = K
        self.T = T
        self.sigma = sigma 
        self.r = r
        self.q = q

    def _d1(self):
        return (math.log(self.S/self.K) + (self.r - self.q)*(self.T)) / (self.sigma*math.sqrt(self.T)) + 0.5 * self.sigma * math.sqrt(self.T)

    def _d2(self):
        return (math.log(self.S/self.K) + (self.r - self.q)*(self.T)) / (self.sigma*math.sqrt(self.T)) - 0.5 * self.sigma * math.sqrt(self.T)

    def _Nd1_first_derivative(self):
        """
        For calculating N'(d1)
        """
        d1 = self._d1()
        return 1/((2 * math.pi)**0.5) * math.exp(-(d1**2)/2)

    def vega(self):
        return self.S * math.exp(-self.q * self.T) * math.sqrt(self.T) * self._Nd1_first_derivative()

    def get_call_premium(self):
        c = self.S * math.exp(-self.q * self.T) * _N(self._d1()) - self.K * math.exp(-self.r * self.T) * _N(self._d2())
        return c

    def get_put_premium(self):
        p = self.K * math.exp(-self.r * self.T) * _N(self._d2(), -1) - self.S * math.exp(-self.q * self.T) * _N(self._d1(), -1)
        return p

    def get_option_premium(self, kind ='C'):
        assert kind in ['C', 'P'], "Incorrect kind. Can only be 'C' or 'P'\na type {} of value {} is obtained instead".format(type(kind), kind)
        if kind == 'C':
            return self.get_call_premium()
        return self.get_put_premium()




    