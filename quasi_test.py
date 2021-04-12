from utils import quasi_rand_num_generator
import numpy as np 

Z = quasi_rand_num_generator(100)
Z2 = np.random.normal(size = 100)

count = 0

for i, _ in enumerate(Z):
    count += 1
    print(type(Z[i]), type(Z2[i]))

print(count)