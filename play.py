from binominaltree import BinominalTree
import numpy as np
import matplotlib.pyplot as plt

bt = BinominalTree(50, 50, 0.25, 0.3, 0.05, 3)

print(bt.get_option_premium())

bt2 = BinominalTree(50,52,2,0.223144,0.05,2)

print(bt2.get_option_premium('P', 'american'))

bt2 = BinominalTree(50,52,2,0.223144,0.05,500)

# alist = []

# for i in range(2,500):
#     bt2 = BinominalTree(50,52,2,0.223144,0.05, i)
#     alist.append(bt2.get_option_premium('P', 'american'))

# y_values = np.array(alist)

# plt.plot(np.arange(y_values.shape[0]), y_values)

# plt.show()