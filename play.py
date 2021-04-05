from binominaltree import BinominalTree

bt = BinominalTree(50, 50, 0.25, 0.3, 0.05, 3)

print(bt.get_option_premium())

bt2 = BinominalTree(50,52,2,0.223144,0.05,2)

print(bt2.get_option_premium('P', 'american'))

bt2 = BinominalTree(50,52,2,0.223144,0.05,500)

print(bt2.get_option_premium('P', 'american'))