# from asianoptionpricer import GeometricAsianOptionPricer
import math
from statistics import mean, stdev
import numpy as np
from utils import confidence_interval, psuedo_rand_no, product

class MonteCarloSimulator:
    def __init__(self, S, sigma, r, T, K, n, m, seed=123):
        """
        m is the no of paths
        """
        self.S = S
        self.sigma = sigma
        self.r = r
        self.T = T
        self.K = K
        self.n = n
        self.m = m

        # print('S:', self.S)
        # print('K:', self.K)
        # print('T:', self.T)
        # print('sigma:', self.sigma)
        # print('r:', self.r)
        # print('n:', self.n)
        # print('m:', self.m)

        self.deltaT = self.T/self.n

        self.geo_payoffs = None
        self.arith_payoffs = None

        np.random.seed(seed)

    def run_simulation(self, kind='C'):
        drift = math.exp((self.r - 0.5*(self.sigma**2))*self.deltaT)

        geo_payoffs_list = []
        arith_payoffs_list = []
        # for m in M sequences
        for _ in range(int(self.m)):     

            growth_factor = drift * math.exp(self.sigma * math.sqrt(self.deltaT)*np.random.normal())
            S_t = self.S * growth_factor
            S_path = [S_t]
            for _ in range(int(self.n-1)):
                growth_factor = drift * math.exp(self.sigma * math.sqrt(self.deltaT)*np.random.normal())
                S_path.append(growth_factor * S_t)
                S_t = growth_factor * S_t
            assert len(S_path) == self.n, "len(S_path): {}".format(len(S_path), self.m)
            S_path = np.array(S_path)

            arith_mean = S_path.mean()
            geo_mean = np.exp((np.log(S_path).sum())/self.n)
            if kind == 'C':
                arith_payoff = math.exp(-self.r * self.T) * max(arith_mean - self.K, 0)
                geo_payoff = math.exp(-self.r * self.T) * max(geo_mean - self.K, 0)
            else:
                arith_payoff = math.exp(-self.r * self.T) * max(self.K - arith_mean, 0)
                geo_payoff = math.exp(-self.r * self.T) * max(self.K - geo_mean, 0)

            arith_payoffs_list.append(arith_payoff)
            geo_payoffs_list.append(geo_payoff)
            
        self.geo_payoffs = np.array(geo_payoffs_list)
        self.arith_payoffs = np.array(arith_payoffs_list)

        assert self.geo_payoffs.shape[0] == self.m
        assert self.arith_payoffs.shape[0] == self.m

class MonteCarloBasketSimulator:
    def __init__(self, Ss, sigmas, r, T, K, n, m, seed=123):
        """
        m is the no of paths
        """
        assert len(Ss) == len(sigmas)
        self.Ss = Ss
        self.sigmas = sigmas
        self.r = r
        self.T = T
        self.K = K
        self.n = n
        self.m = m

        # print('S:', self.S)
        # print('K:', self.K)
        # print('T:', self.T)
        # print('sigma:', self.sigma)
        # print('r:', self.r)
        # print('n:', self.n)
        # print('m:', self.m)

        self.deltaT = self.T/self.n

        self.geo_payoffs = None
        self.arith_payoffs = None

        np.random.seed(seed)

    def run_simulation(self, kind='C'):

        geo_payoffs_list = []
        arith_payoffs_list = []
        drifts = []
        
        # prepare drift for each S
        for i in range(len(self.Ss)):
            drifts.append(math.exp((self.r - 0.5*(self.sigmas[i]**2))*self.deltaT))
        
        # for m in M sequences
        for _ in range(int(self.m)):
            Ss_t = [] # for keeping track of the current S_ts
            Ss_m1t = [] # for keeping track of the t-1 value of Ss
            # initialise first element of the Bg and Bs arrays
            for i in range(len(self.Ss)):    
                growth_factor = drifts[i] * math.exp(self.sigmas[i] * math.sqrt(self.deltaT)*np.random.normal())
                S_t = self.Ss[i] * growth_factor
                Ss_t.append(S_t)
            Ss_m1t = Ss_t
            # continue looping through the arrays
            for _ in range(int(self.n-1)):
                Ss_t = []
                for i in range(len(self.Ss)):
                    growth_factor = drifts[i] * math.exp(self.sigmas[i] * math.sqrt(self.deltaT)*np.random.normal())
                    Ss_t.append(growth_factor * Ss_m1t[i])
                Ss_m1t = Ss_t

            assert len(Ss_t) == len(self.Ss)
            Ss_t = np.array(Ss_t)

            Ba_T = Ss_t.mean()
            Bg_T = product(Ss_t)**(1/len(Ss_t))
            
            if kind == 'C':
                arith_payoff = math.exp(-self.r * self.T) * max(Ba_T - self.K, 0)
                geo_payoff = math.exp(-self.r * self.T) * max(Bg_T - self.K, 0)
            else:
                arith_payoff = math.exp(-self.r * self.T) * max(self.K - Ba_T, 0)
                geo_payoff = math.exp(-self.r * self.T) * max(self.K - Bg_T, 0)

            arith_payoffs_list.append(arith_payoff)
            geo_payoffs_list.append(geo_payoff)
            
        self.geo_payoffs = np.array(geo_payoffs_list)
        self.arith_payoffs = np.array(arith_payoffs_list)

        assert self.geo_payoffs.shape[0] == self.m
        assert self.arith_payoffs.shape[0] == self.m