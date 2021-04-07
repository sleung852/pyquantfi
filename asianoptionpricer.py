from utils import _N, sum_sum_product, product, confidence_interval
import math
import numpy as np
from montecarlo import MonteCarloSimulator, MonteCarloSimulator3, MonteCarloSimulator2

class GeometricAsianOptionPricer:
    def __init__(self, S, K, T, sigma, r, n):
        self.S = S
        self.K = K
        self.T = T
        self.sigma = sigma
        self.r = r
        self.n = n
        self.sigma_hat = self._sigma_hat()
        self.mu_hat = self._mu_hat()
        # print('S:', self.S)
        # print('K:', self.K)
        # print('T:', self.T)
        # print('sigma:', self.sigma)
        # print('r:', self.r)
        # print('n:', self.n)

    def _sigma_hat(self):
        return self.sigma * math.sqrt((self.n+1)*(2*self.n+1)/(6*self.n**2))

    def _mu_hat(self):
        return (self.r - 0.5 * self.sigma**2)*(self.n+1)/(2*self.n) + 0.5*(self.sigma_hat**2)

    def _d1_hat(self):
        return (math.log(self.S/self.K) + (self.mu_hat + 0.5 * self.sigma_hat**2)*self.T /
        (self.sigma_hat*math.sqrt(self.T)))

    def _d2_hat(self):
        return self._d1_hat() - self.sigma_hat*math.sqrt(self.T)

    def get_call_premium(self):
        c = math.exp(-self.r * self.T) * (self.S*math.exp(self.mu_hat*self.T)*_N(self._d1_hat()) - self. K*_N(self._d2_hat())) 
        return c

    def get_put_premium(self):
        p = math.exp(-self.r * self.T) * (-1 * self.S*math.exp(self.mu_hat*self.T)*_N(self._d1_hat(), -1) + self. K * _N(self._d2_hat(), -1)) 
        return p

    def get_option_premium(self, kind ='C'):
        assert kind in ['C', 'P'], "Incorrect kind. Can only be 'call' or 'put'"
        if kind == 'C':
            return self.get_call_premium()
        return self.get_put_premium()        

class GeometricAsianOptionBasketPricer:
    def __init__(self, Ss, sigmas, r, T, K, rhos):
        """
        Ss is a list of asset prices
        sigmas is a list of sigma
        """
        assert len(Ss) == len(sigmas), "Size of Ss and sigmas are different!"
        self.n = len(Ss)
        self.Ss = Ss
        self.sigmas = sigmas
        self.r = r
        self.T = T
        self.K = K
        if type(rhos) == int or type(rhos) == float:
            self.rhos = np.array([rhos])
        elif type(rhos) == np.ndarray:
            self.rhos = rhos
        else:
            assert False, "Rhos should be either list or int or float"

        self.Bg = self._Bg()
        self.sigma_Bg = self._sigma_Bg()
        self.mu_Bg = self._mu_Bg()

    def _Bg(self):
        return product(self.Ss) ** (1/self.n)

    def _sigma_Bg(self):
        # return math.sqrt(sum_sum_product(self.sigmas, self.rhos)) / self.n
        return math.sqrt(self.sigmas[0] * self.sigmas[1] * self.rhos[0])/self.n

    def _mu_Bg(self):
        return self.r - 0.5 * sum([sigma**2 for sigma in self.sigmas]) / self.n + 0.5 * self.sigma_Bg ** 2

    def _d1_hat(self):
        return (math.log(self.Bg/self.K) + (self.mu_Bg + 0.5 * self.sigma_Bg**2)*self.T /
        (self.sigma_Bg*math.sqrt(self.T)))

    def _d2_hat(self):
        return self._d1_hat() - self.sigma_Bg*math.sqrt(self.T)

    def get_call_premium(self):
        c = math.exp(-self.r * self.T) * (self.Bg*math.exp(self.mu_Bg*self.T)*_N(self._d1_hat()) - self. K * _N(self._d2_hat())) 
        return c

    def get_put_premium(self):
        p = math.exp(-self.r * self.T) * (-1 * self.Bg*math.exp(self.mu_Bg*self.T)*_N(self._d1_hat(), -1) + self. K * _N(self._d2_hat(), -1)) 
        return p

    def get_option_premium(self, kind ='C'):
        assert kind in ['C', 'P'], "Incorrect kind. Can only be 'call' or 'put'"
        if kind == 'C':
            return self.get_call_premium()
        return self.get_put_premium()

class ArithmeticAsianOptionPricer:

    def __init__(self, S, sigma, r, T, K, n, m, seed=1126):
        self.S = S
        self.sigma = sigma
        self.r = r
        self.T = T
        self.K = K
        self.n = n
        self.m = m
        self.deltaT = self.T/self.n

        self.mcs = MonteCarloSimulator(S, sigma, r, T, K, n, m, seed)


    def standard_monte_carlo(self, option_type='arithmetic'):
        # standard monte carlo
        P_mean = self.mcs.arith_payoffs.mean()
        P_std = self.mcs.arith_payoffs.std()
        return P_mean, P_std, confidence_interval(P_mean, P_std, self.m)

    def control_variate(self, kind='C'):
        conv_XY = (self.mcs.arith_payoffs * self.mcs.geo_payoffs).mean() - self.mcs.arith_payoffs.mean() * self.mcs.geo_payoffs.mean()
        # XY = np.stack((self.arith_payoffs, self.geo_payoffs), axis=0)
        # conv_XY = np.cov(XY)
        theta = conv_XY / self.mcs.geo_payoffs.var()

        gaop = GeometricAsianOptionPricer(S=self.S, K=self.K, sigma=self.sigma, r=self.r, T = self.T, n = self.n)
        geo = gaop.get_option_premium(kind=kind)

        Z = self.mcs.arith_payoffs + theta * (geo - self.mcs.geo_payoffs)
        Z_mean = Z.mean()
        Z_std = Z.std()
        
        return Z_mean, Z_std, confidence_interval(Z_mean, Z_std, self.m)

    def get_call_premium(self, mode='mc'):
        assert mode in ['mc', 'cv'], 'mode must be either "mc" or "cv"'
        self.mcs.run_simulation()
        if mode == 'mc':
            return self.standard_monte_carlo()
        return self.control_variate('C')

    def get_put_premium(self, mode='mc'):
        assert mode in ['mc', 'cv'], 'mode must be either "mc" or "cv"'
        self.mcs.run_simulation('P')
        if mode == 'mc':
            return self.standard_monte_carlo()
        return self.control_variate('P')

    def get_option_premium(self, kind ='C', mode='mc'):
        assert mode in ['mc', 'cv'], 'mode must be either "mc" or "cv"'
        if kind == 'C':
            return self.get_call_premium(mode=mode)
        return self.get_put_premium(mode=mode)   

class ArithmeticAsianOptionBasketPricer:

    def __init__(self, Ss, sigmas, r, T, K, rhos, n, m):
        assert len(Ss) == len(sigmas), "Size of Ss and sigmas are different!"
        self.n = len(Ss)
        self.Ss = Ss
        self.sigmas = sigmas
        self.r = r
        self.T = T
        self.K = K
        if type(rhos) == int or type(rhos) == float:
            self.rhos = np.array([rhos])
        elif type(rhos) == np.ndarray:
            self.rhos = rhos
        else:
            assert False, "Rhos should be either list or int or float"
        self.m = m
        self.n = n
        self.rhos = rhos
        self.mcs = MonteCarloSimulator3(Ss, sigmas, r, T, K, n, m)

    def standard_monte_carlo(self, option_type='arithmetic'):
        # standard monte carlo
        P_mean = self.mcs.arith_payoffs.mean()
        P_std = self.mcs.arith_payoffs.std()
        return P_mean, P_std, confidence_interval(P_mean, P_std, self.m)

    def control_variate(self, kind='C'):
        conv_XY = (self.mcs.arith_payoffs * self.mcs.geo_payoffs).mean() - self.mcs.arith_payoffs.mean() * self.mcs.geo_payoffs.mean()
        # XY = np.stack((self.arith_payoffs, self.geo_payoffs), axis=0)
        # conv_XY = np.cov(XY)
        theta = conv_XY / self.mcs.geo_payoffs.var()

        gaop = GeometricAsianOptionBasketPricer(Ss=self.Ss, K=self.K, sigmas=self.sigmas, r=self.r, T = self.T, rhos = self.rhos)
        geo = gaop.get_option_premium(kind=kind)

        Z = self.mcs.arith_payoffs + theta * (geo - self.mcs.geo_payoffs)
        Z_mean = Z.mean()
        Z_std = Z.std()

        return Z_mean, Z_std, confidence_interval(Z_mean, Z_std, self.m)

    def get_call_premium(self, mode='mc'):
        assert mode in ['mc', 'cv'], 'mode must be either "mc" or "cv"'
        self.mcs.run_simulation()
        if mode == 'mc':
            return self.standard_monte_carlo()
        return self.control_variate('C')

    def get_put_premium(self, mode='mc'):
        assert mode in ['mc', 'cv'], 'mode must be either "mc" or "cv"'
        self.mcs.run_simulation('P')
        if mode == 'mc':
            return self.standard_monte_carlo()
        return self.control_variate('P')

    def get_option_premium(self, kind ='C', mode='mc'):
        assert mode in ['mc', 'cv'], 'mode must be either "mc" or "cv"'
        if kind == 'C':
            return self.get_call_premium(mode=mode)
        return self.get_put_premium(mode=mode)  
        