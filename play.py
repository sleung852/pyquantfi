from blackscholes import EuropeanOptionPricer

param_dict = {
    'S': 2,
    'K': 2,
    'T': 3,
    'sigma': 0.3,
    'r': 0.03,
    'q': 0
}

bs_test = EuropeanOptionPricer(**param_dict)

print(bs_test.get_call_premium())