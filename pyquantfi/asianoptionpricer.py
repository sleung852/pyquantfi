from .utils import _N, sum_sum_product, product, confidence_interval
import math
import numpy as np
from .montecarlo import MonteCarloSimulator, MonteCarloBasketSimulator

class GeometricAsianOptionPricer:
    def __init__(self, S, K, T, sigma, r, n):

        # print('S:', S)
        # print('K:', K)
        # print('T:', T)
        # print('sigma:', sigma)
        # print('r:', r)
        # print('n:', n)
        self.S = S
        self.K = K
        self.T = T
        self.sigma = sigma
        self.r = r
        self.n = int(n)
        self.sigma_hat = self._sigma_hat()
        self.mu_hat = self._mu_hat()


    def _sigma_hat(self):
        return self.sigma * math.sqrt((self.n+1)*(2*self.n+1)/(6*self.n**2))

    def _mu_hat(self):
        return (self.r - 0.5 * self.sigma**2)*(self.n+1)/(2*self.n) + 0.5*(self.sigma_hat**2)

    def _d1_hat(self):
        return (math.log(self.S/self.K) + (self.mu_hat + 0.5 * self.sigma_hat**2)*self.T /
        (self.sigma_hat*math.sqrt(self.T)))

    def _d2_hat(self):
        return self._d1_hat() - self.sigma_hat*math.sqrt(self.T)

    def get_call_premium(self, method="closed", m=None):
        assert method in ['closed', 'std_mcs' ,'quasi_mcs'], "method must be either 'closed' or 'msc'"
        if method == 'closed':
            c = math.exp(-self.r * self.T) * (self.S*math.exp(self.mu_hat*self.T)*_N(self._d1_hat()) - self. K*_N(self._d2_hat())) 
            return c
        else:
            if m is None:
                m = 100000
            self.mcs = MonteCarloSimulator(self.S, self.sigma, self.r, self.T, self.K, self.n, int(m))
            if method == 'quasi_mcs':
                self.mcs.run_simulation('C', 'quasi')
            else:
                self.mcs.run_simulation('C')
            P_mean, _, _ = self.standard_monte_carlo(m)
            return P_mean

    def get_put_premium(self, method="closed", m=None):
        assert method in ['closed', 'std_mcs', 'quasi_mcs'], "method must be either 'closed' or 'msc'"
        if method == 'closed':
            p = math.exp(-self.r * self.T) * (-1 * self.S*math.exp(self.mu_hat*self.T)*_N(self._d1_hat(), -1) + self. K * _N(self._d2_hat(), -1)) 
            return p
        else:
            if m is None:
                m = 100000
            self.mcs = MonteCarloSimulator(self.S, self.sigma, self.r, self.T, self.K, self.n, m)
            if method == 'quasi_mcs':
                self.mcs.run_simulation('P', 'quasi')
            else:
                self.mcs.run_simulation('P')
            P_mean, _, _ = self.standard_monte_carlo(m)
            return P_mean

    def get_option_premium(self, kind ='C', method="closed", m=None):
        assert kind in ['C', 'P'], "Incorrect kind. Can only be 'C' for call or 'P' for put"
        assert method in ['closed', 'std_mcs', 'quasi_mcs'], "method must be either 'closed' or 'msc'"
        if kind == 'C':
            return self.get_call_premium(method=method, m=m)
        return self.get_put_premium(method=method, m=m)

    def standard_monte_carlo(self, m):
        # standard monte carlo
        P_mean = self.mcs.geo_payoffs.mean()
        P_std = self.mcs.geo_payoffs.std()
        return P_mean, P_std, confidence_interval(P_mean, P_std, m)      

class ArithmeticAsianOptionPricer:

    def __init__(self, S, sigma, r, T, K, n, m, seed=1126):
        self.S = S
        self.sigma = sigma
        self.r = r
        self.T = T
        self.K = K
        self.n = int(n)
        self.m = int(m)
        self.deltaT = self.T/self.n

        self.mcs = MonteCarloSimulator(S, sigma, r, T, K, n, m, seed)

    def standard_monte_carlo(self):
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

    def get_call_premium(self, method='std_mcs'):
        assert method in ['std_mcs', 'std_mcs_cv', 'quasi_mcs', 'quasi_mcs_cv'], 'method must be either "std_mcs", "std_mcs_cv", "quasi_mcs" or "quasi_mcs_cv"'
        if method == 'std_mcs':
            self.mcs.run_simulation()
            return self.standard_monte_carlo()[0]
        elif method == 'std_mcs_cv':
            self.mcs.run_simulation()
            return self.control_variate('C')[0]
        elif method == 'quasi_mcs':
            self.mcs.run_simulation('C', 'quasi')
            return self.standard_monte_carlo()[0]
        elif method == 'quasi_mcs_cv':
            self.mcs.run_simulation('C', 'quasi')
            return self.control_variate('C')[0]

    def get_put_premium(self, method='std_mcs'):
        assert method in ['std_mcs', 'std_mcs_cv', 'quasi_mcs', 'quasi_mcs_cv'], 'method must be either "std_mcs", "std_mcs_cv", "quasi_mcs" or "quasi_mcs_cv"'
        if method == 'std_mcs':
            self.mcs.run_simulation('P')
            return self.standard_monte_carlo()[0]
        elif method == 'std_mcs_cv':
            self.mcs.run_simulation('P')
            return self.control_variate('P')[0]
        elif method == 'quasi_mcs':
            self.mcs.run_simulation('P', 'quasi')
            return self.standard_monte_carlo()[0]
        elif method == 'quasi_mcs_cv':
            self.mcs.run_simulation('P', 'quasi')
            return self.control_variate('P')[0]

    def get_option_premium(self, kind ='C', method='std_mcs'):
        assert method in ['std_mcs', 'std_mcs_cv', 'quasi_mcs', 'quasi_mcs_cv'], 'method must be either "std_mcs", "std_mcs_cv", "quasi_mcs" or "quasi_mcs_cv"'
        if kind == 'C':
            return self.get_call_premium(method=method)
        return self.get_put_premium(method=method) 