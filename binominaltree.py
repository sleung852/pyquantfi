import math
import numpy as np

class BinominalTree:
    def __init__(self, S, K, T, sigma, r, n):
        assert n > 0, "n must be greater than 0"
        self.S = S
        self.K = K
        self.T = T
        self.sigma = sigma
        self.r = r
        self.n = int(n)

        self.deltaT = self.T/self.n

        self.u = self._get_u()
        self.d = self._get_d()
        self.p = self._get_p()

    def _get_u(self):
        # using the CRR (Cox, Ross and Rubinstein) model
        return math.exp(self.sigma * self.deltaT**0.5)

    def _get_d(self):
        return 1/self._get_u()

    def _get_p(self):
        return (math.exp(self.r * self.deltaT) - self.d) / (self.u - self.d)

    def _get_call_value(self, S, K):
        return max(S-K, 0)

    def _get_put_value(self, S, K):
        return max(K-S, 0)

    def _get_leaves_values(self, kind='C'):
        leaves_values = []
        # for each leave node
        for i in range(self.n + 1):
            # calculate S at time period T
            ST = self.u**(self.n - i) * self.d**(i) * self.S
            if kind == 'C':
                leaves_values.append(self._get_call_value(ST, self.K))
            else:
                leaves_values.append(self._get_put_value(ST, self.K))
        return leaves_values
        
    def _get_all_S_values(self):
        """
        This obtains all the S values in the trees from t=0 until t=T-1
        """
        S_values = [[self.S]]
        # if it is a one-step model
        if self.n == 1:
            return S_values
        # if it is a 2+ steps model
        for i in range(1, self.n):
            S_values_at_t = []
            for j in range(i+1): # until t = T-1
                S_values_at_t.append(self.u**(i - j) * self.d**(j) * self.S)
            S_values.append(S_values_at_t)
        return S_values

    def _get_values_at_t(self, leaves, S_values, kind = 'C', option_type = 'american'):
        option_values = []
        for i in range(len(leaves) - 1):
            discounted_option_value = math.exp(-self.r * self.deltaT) *(leaves[i]*self.p + leaves[i+1]*(1-self.p))
            if (option_type == 'american') and (kind == 'P'):
                option_values.append(max(discounted_option_value, self._get_put_value(S_values[-1][i], self.K)))
            else:
                option_values.append(discounted_option_value)
        S_values = S_values[:-1]
        return option_values, S_values

    def get_call_premium(self, option_type = 'american'):
        assert option_type in ['american', 'european']
        return self.get_option_premium(kind='C', option_type=option_type)

    def get_put_premium(self, option_type = 'american'):
        assert option_type in ['american', 'european']
        return self.get_option_premium(kind='P', option_type=option_type)

    def get_option_premium(self, kind='C', option_type = 'american'):
        assert option_type in ['american', 'european']
        assert kind in ['P', 'C']
        leaves = self._get_leaves_values(kind=kind)
        S_values = self._get_all_S_values()
        option_values = leaves
        while len(option_values) != 1:
            option_values, S_values = self._get_values_at_t(option_values, S_values, kind=kind, option_type=option_type)
        return option_values[0]

    def visualise(self, kind='C', option_type='american'):
        pass