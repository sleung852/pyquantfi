from utils import _N, sum_sum_product, product, confidence_interval
import math
import numpy as np
from montecarlo import MonteCarloBasketSimulator

class GeometricBasketOptionPricer:
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
        if self.rhos.shape[0] == 1:
            v = self.sigmas[0]**2 * 1 + 2 * self.sigmas[0] * self.sigmas[1] * self.rhos[0] + self.sigmas[1]**2 * 1
        else:
            v = 0
            for i in range(len(self.sigmas)):
                for j in range(len(self.sigmas)):
                    v += self.sigmas[i] * self.sigmas[j] * self.rhos[i][j]
        return math.sqrt(v)/self.n

    def _mu_Bg(self):
        return self.r - 0.5 * sum([sigma**2 for sigma in self.sigmas]) / self.n + 0.5 * self.sigma_Bg ** 2

    def _d1_hat(self):
        return (math.log(self.Bg/self.K) + (self.mu_Bg + 0.5 * self.sigma_Bg**2)*self.T /
        (self.sigma_Bg*math.sqrt(self.T)))

    def _d2_hat(self):
        return self._d1_hat() - self.sigma_Bg*math.sqrt(self.T)

    def get_call_premium(self, method='closed', m=None):
        assert method in ['closed', 'std_mcs', 'quasi_mcs'], "method must be either 'closed' or 'msc'"
        if method == 'closed':
            c = math.exp(-self.r * self.T) * (self.Bg*math.exp(self.mu_Bg*self.T)*_N(self._d1_hat()) - self. K * _N(self._d2_hat())) 
            return c
        else:
            if m is None:
                m = 100000
            self.mcs = MonteCarloBasketSimulatorOld(self.Ss, self.sigmas, self.r, self.T, self.K, self.n, m, self.rhos)
            if method == 'quasi_mcs':
                self.mcs.run_simulation('C', 'quasi')
            else:
                self.mcs.run_simulation('C')
            P_mean, _, _ = self.standard_monte_carlo(m)
            return P_mean

    def get_put_premium(self, method='closed', m=None):
        assert method in ['closed', 'std_mcs', 'quasi_mcs'], "method must be either 'closed', 'std_mcs' or 'quasi_mcs'"
        if method == 'closed':
            p = math.exp(-self.r * self.T) * (-1 * self.Bg*math.exp(self.mu_Bg*self.T)*_N(self._d1_hat(), -1) + self. K * _N(self._d2_hat(), -1)) 
            return p
        else:
            if m is None:
                m = 100000
            self.mcs = MonteCarloBasketSimulatorOld(self.Ss, self.sigmas, self.r, self.T, self.K, self.n, m, self.rhos)
            if method == 'quasi_mcs':
                self.mcs.run_simulation('P', 'quasi')
            else:
                self.mcs.run_simulation('P')
            P_mean, _, _ = self.standard_monte_carlo(m)
            return P_mean

    def get_option_premium(self, kind ='C', method="closed", m=None):
        assert kind in ['C', 'P'], "Incorrect kind. Can only be 'C' for call or 'P' for put"
        assert method in ['closed', 'std_mcs', 'quasi_mcs'], "method must be either 'closed', 'std_mcs' or 'quasi_mcs'"
        if kind == 'C':
            return self.get_call_premium(method=method, m=m)
        return self.get_put_premium(method=method, m=m)

    def standard_monte_carlo(self, m):
        # standard monte carlo
        P_mean = self.mcs.geo_payoffs.mean()
        P_std = self.mcs.geo_payoffs.std()
        return P_mean, P_std, confidence_interval(P_mean, P_std, m)   

class ArithmeticBasketOptionBasketPricer:

    def __init__(self, Ss, sigmas, r, T, K, rhos, m):
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
            assert False, "Rhos should be either a np.ndarray or int or float"
        self.m = int(m)
        self.n = len(Ss)
        self.mcs = MonteCarloBasketSimulatorOld(Ss, sigmas, r, T, K, self.n, m, self.rhos)

    def standard_monte_carlo(self):
        # standard monte carlo
        P_mean = self.mcs.arith_payoffs.mean()
        P_std = self.mcs.arith_payoffs.std()
        return P_mean, P_std, confidence_interval(P_mean, P_std, self.m)
        # return P_mean

    def control_variate(self, kind='C'):
        conv_XY = (self.mcs.arith_payoffs * self.mcs.geo_payoffs).mean() - self.mcs.arith_payoffs.mean() * self.mcs.geo_payoffs.mean()
        # XY = np.stack((self.arith_payoffs, self.geo_payoffs), axis=0)
        # conv_XY = np.cov(XY)
        theta = conv_XY / self.mcs.geo_payoffs.var()

        gaop = GeometricBasketOptionPricer(Ss=self.Ss, K=self.K, sigmas=self.sigmas, r=self.r, T = self.T, rhos = self.rhos)
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
        