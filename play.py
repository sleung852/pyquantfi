import math
import numpy as np

S = 4
sigma = 0.25
r = 0.03
deltaT = 1
N = int(deltaT/1e-2)
M = int(1e4)

#S_path = []

print("N:",N)
drift = math.exp((r - 0.5 * sigma**2) * deltaT)
print('drift:', drift)

growth_factor = drift * math.exp(sigma * math.sqrt(deltaT)*np.random.normal())
print('growth_factor:', growth_factor)
S_hat = S * growth_factor
print('S_hat', S_hat)
S_path = [S_hat]
for _ in range(int(N-1)):
    growth_factor = drift * math.exp(sigma * math.sqrt(deltaT)*np.random.normal())
    print('growth_factor:', growth_factor)
    print('S_hat', growth_factor * S_path[-1])
    S_path.append(growth_factor * S_path[-1])
print('S_path:', S_path)
print('len:', len(S_path))
print('S_T', np.array(S_path).mean())