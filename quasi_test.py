import ghalton
import numpy as np
from scipy.stats import norm

M = 10

N = 6

# for _ in range(M):
#     seqr = ghalton.GeneralizedHalton(1, 2000)
#     X = np.array(seqr.get(N))
#     Z = norm.ppf(X)
#     print(Z)

seqr = ghalton.GeneralizedHalton(N*2, 2000)
X = np.array(seqr.get(M))
Z = norm.ppf(X)
Z = Z.reshape((M,2,N))
for i in range(M):
    print(Z[i])
    print((Z[i].shape))

# Z = np.random.standard_normal((M,N))

# print(Z.shape)

# print(Z[0])