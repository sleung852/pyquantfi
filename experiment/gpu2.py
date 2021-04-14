import numpy as np
from montecarlo import MonteCarloSimulator
from utils import psuedo_rand_num_generator

mcs = MonteCarloSimulator(100,0.3,0.05,3,100,50,100000)
Zs = psuedo_rand_num_generator(50, 100000, 2000)
mcs.run_simulation_fast(Zs=Zs)