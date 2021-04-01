from controlvariate import GeometricAsianOptionPricer
import math
from statistics import mean, stdev
import numpy as np
from utils import confidence_interval

class MonteCarloSimulator:
    def __init__(self, S, sigma, r, deltaT, K, n, m):
        """
        m is the no of paths
        """
        self.S = S
        self.sigma = sigma
        self.r = r
        self.deltaT = deltaT
        self.K = K
        self.n = n
        self.m = m

        self.geo_payoffs = None
        self.arith_payoffs = None

    def run_simulation(self, kind='C'):
        drift = math.exp((self.r - 0.5 * self.sigma**2) * self.deltaT)

        geo_payoffs_list = []
        arith_payoffs_list = []

        for i in range(paths):            
            growth_factor = drift * exp(self.sigma * math.sqrt(self.deltaT)*randn)
            S_path = [self.S * growth_factor]
            for _ in range(self.n-1):
                growth_factor = drift * exp(self.sigma * math.sqrt(self.deltaT)*randn)
                S_path.append(growth_factor * S_path[-1])
        
            arith_mean = sum(S_path)/len(S_path)
            geo_mean = math.exp(sum(math.log(S_path))/N)
            if kind == 'C':
                arith_payoff = math.exp(-self.r * self.deltaT) * max(arith_mean - self.K, 0)
                geo_payoff = math.exp(-self.r * self.deltaT) * max(geo_mean - self.K, 0)
            else:
                arith_payoff = math.exp(-self.r * self.deltaT) * max(self.K - arith_mean, 0)
                geo_payoff = math.exp(-self.r * self.deltaT) * max(self.K - geo_mean, 0)

            arith_payoffs_list.append(arith_payoff)
            geo_payoffs_list.append(geo_payoff)
            
        self.geo_payoffs = np.array(geo_payoffs_list)
        self.arith_payoffs = np.array(arith_payoffs_list)

    def standard_monte_carlo(self):
        # standard monte carlo
        P_mean = self.arith_payoffs.mean()
        P_std = self.arith_payoffs.stdev()
        return P_mean, P_std, confidence_interval(P_mean, P_std, self.m)

    def control_variate(self):
        conv_XY = (self.arith_payoffs * self.geo_payoffs).mean() - self.arith_payoffs.mean() * self.geo_payoffs.mean()
        theta = conv_XY / self.geo_payoffs.var()

        gaop = GeometricAsianOptionPricer(S=self.S, sigma=self.sigma, r=self.r, deltaT = self.deltaT, n = self.n)
        geo = gaop.get_option_premium(kind=kind)

        Z = self.arith_payoffs + theta * (geo - self.geo_payoffs)
        Z_mean = Z.mean()
        Z_std = Z.std()
        
        return Z_mean, Z_std, confidence_interval(Z_mean, Z_std, self.m)

    def get_call_premium(self, mode='mc'):
        assert mode in ['mc', 'cv'], 'mode must be either "mc" or "cv"'
        self.run_simulation()
        return self.standard_monte_carlo()

    def get_put_premium(self, mode='mc'):
        assert mode in ['mc', 'cv'], 'mode must be either "mc" or "cv"'
        self.run_simulation()
        return self.control_variate()

    def get_option_premium(self, kind ='C', mode='mc'):
        assert mode in ['mc', 'cv'], 'mode must be either "mc" or "cv"'
        if kind == 'C':
            return self.get_call_premium(mode=mode)
        return self.get_put_premium(mode=mode)     

        