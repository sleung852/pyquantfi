from utils import _N
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
    def __init__(self, basket):
        """
        basket is a list of GeometricAsianOptionPricer
        """
        assert len(basket) > 0, "Basket must contain at least one GeoemetricAsianOptionPricer object"
        assert all([type(item)==GeometricAsianOptionPricer for item in basket]), "Basket contains non-GeoemetricAsianOptionPricer type"
        self.basket = basket
        self.count = len(basket)
        self.Bg = self._Bg()

    def _Bg(self):
        Bg = 1
        for asset in self.basket:
            Bg *= asset.S
        return Bg ** (1/self.count)

    def _sigma_Bg(self):
        pass
