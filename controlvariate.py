from utils import _N, cross_sum_product, product
import math

class GeometricAsianOptionPricer:
    def __init__(self, S, K, deltaT, sigma, r, n):
        self.S = S
        self.K = K
        self.deltaT = deltaT
        self.sigma = sigma
        self.r = r
        self.n = n
        self.sigma_hat = self._sigma_hat()
        self.mu_hat = self._mu_hat()

    def _sigma_hat(self):
        return self.sigma * math.sqrt((self.n+1)*(2*self.n+1)/(6*self.n*self.n))

    def _mu_hat(self):
        return (self.r - 0.5 * self.sigma**2)*(self.n+1)/(2*self.n) + 0.5*(self.sigma_hat**2)

    def _d1_hat(self):
        return (math.log(self.S/self.K) + (self.mu_hat + 0.5 * self.sigma_hat**2)*self.deltaT /
        (self.sigma*math.sqrt(self.deltaT)))

    def _d2_hat(self):
        return self._d1_hat() - self.sigma_hat*math.sqrt(self.deltaT)

    def get_call_premium(self):
        c = math.exp(-self.r * self.deltaT) * (self.S*math.exp(self.mu_hat*self.deltaT)*_N(self._d1_hat()) - self. K * _N(self._d2_hat())) 
        return c

    def get_put_premium(self):
        p = math.exp(-self.r * self.deltaT) * (-1 * self.S*math.exp(self.mu_hat*self.deltaT)*_N(self._d1_hat(), -1) + self. K * _N(self._d2_hat(), -1)) 
        return p

    def get_option_premium(self, kind ='C'):
        assert kind in ['C', 'P'], "Incorrect kind. Can only be 'call' or 'put'"
        if kind == 'C':
            return self.get_call_premium()
        return self.get_put_premium()        

class GeometricAsianOptionBasketPricer:
    def __init__(self, Ss, sigmas, r, deltaT, K, rhos):
        """
        Ss is a list of asset prices
        sigmas is a list of sigma
        """
        assert len(Ss) == len(sigmas), "Size of Ss and sigmas are different!"
        self.n = len(Ss)
        self.Ss = Ss
        self.sigmas = sigmas
        self.r = r
        self.deltaT = deltaT
        self.K = K
        if type(rhos) == int or type(rhos) == float:
            self.rhos = list(rhos)
        elif type(rhos) == list:
            self.rhos = rhos
        else:
            assert False, "Rhos should be either list or int or float"

        self.Bg = self._Bg()
        self.sigma_Bg = self._sigma_Bg()
        self.mu_Bg = self._mu_Bg()

    def _Bg(self):
        return product(Bg) ** (1/self.n)

    def _sigma_Bg(self):
        return math.sqrt(cross_sum_product(self.sigmas, self.rhos)) / self.n

    def _mu_Bg(self):
        return self.r - 0.5 * sum([sigma**2 for sigma in sigmas]) / n + 0.5 * self._sigma_Bg ** 2

    def _d1_hat(self):
        return (math.log(self.Bg/self.K) + (self.mu_Bg + 0.5 * self.sigma_Bg**2)*self.deltaT /
        (self.sigma_Bg*math.sqrt(self.deltaT)))

    def _d2_hat(self):
        return self._d1_hat() - self.sigma_Bg*math.sqrt(self.deltaT)

    def get_call_premium(self):
        c = math.exp(-self.r * self.deltaT) * (self.Bg*math.exp(self.mu_Bg*self.deltaT)*_N(self._d1_hat()) - self. K * _N(self._d2_hat())) 
        return c

    def get_put_premium(self):
        p = math.exp(-self.r * self.deltaT) * (-1 * self.S*math.exp(self.mu_Bg*self.deltaT)*_N(self._d1_hat(), -1) + self. K * _N(self._d2_hat(), -1)) 
        return p

    def get_option_premium(self, kind ='C'):
        assert kind in ['C', 'P'], "Incorrect kind. Can only be 'call' or 'put'"
        if kind == 'C':
            return self.get_call_premium()
        return self.get_put_premium()