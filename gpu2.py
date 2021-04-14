import numpy as np
from montecarlo import MonteCarloBasketSimulator

mcs = MonteCarloBasketSimulator([100, 100], [0.3,0.3], 0.05, 3, 100, 50, 1000)
mcs.run_simulation_fast()
print('Mean Values:', mcs.arith_payoffs.mean(), mcs.geo_payoffs.mean())

mcs = MonteCarloBasketSimulator([100, 100], [0.3,0.3], 0.05, 3, 100, 50, 1000)
mcs.run_simulation()
print('Mean Values:', mcs.arith_payoffs.mean(), mcs.geo_payoffs.mean())
