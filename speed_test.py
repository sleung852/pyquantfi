from timeit import default_timer as timer
import numpy as np

from montecarlo import MonteCarloSimulator

start = timer()
print('Faster')
mcs = MonteCarloSimulator(100, 0.3, 0.05, 3, 100, 50, 100000)
mcs.run_simulation()
print(f'Run Time: {timer() - start}s')
print('Mean Values:', mcs.arith_payoffs.mean(), mcs.geo_payoffs.mean())


start = timer()
print('Slow')
mcs = MonteCarloSimulator(100, 0.3, 0.05, 3, 100, 50, 100000)
mcs.run_simulation_slow()
print(f'Run Time: {timer() - start}s')
print('Mean Values:', mcs.arith_payoffs.mean(), mcs.geo_payoffs.mean())