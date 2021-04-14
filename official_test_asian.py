from asianoptionpricer import ArithmeticAsianOptionPricer, GeometricAsianOptionPricer

case_no = 1

def test_asian_option_pricer(sigma, K, n, kind):
    global case_no
    print(f'Test Case {case_no}')
    case_no += 1
    print('*Parameters*')
    print('Sigma: {}, K: {}, n: {}, kind: {}'.format(sigma, K, n, kind))
    print('\nGeometric Asian Option')
    geo = GeometricAsianOptionPricer(S=100, r=0.05, T=3, sigma=sigma, K=K, n=n)
    print('Value from Closed Form: {}'.format(geo.get_option_premium(kind=kind, method="closed")))
    print('Value from Monte Carlo: {}'.format(geo.get_option_premium(kind=kind, method="std_mcs", m=100000)))
    print('\nArithmetic Asian Option')
    ari = ArithmeticAsianOptionPricer(S=100, r=0.05, T=3, m=100000, sigma=sigma, K=K, n=n)
    print('Value from Standard Monte Carlo: {}'.format(ari.get_option_premium(kind=kind, method="std_mcs")))
    print('Value from Standard Monte Carlo with CV: {}'.format(ari.get_option_premium(kind=kind, method="std_mcs_cv")))
    print()

print('**Official Test for COMP7405 Assignment 3')
print('Asian Options')
test_asian_option_pricer(0.3, 100, 50, 'P')
test_asian_option_pricer(0.3, 100, 100, 'P')
test_asian_option_pricer(0.4, 100, 50, 'P')
test_asian_option_pricer(0.3, 100, 50, 'C')
test_asian_option_pricer(0.3, 100, 100, 'C')
test_asian_option_pricer(0.4, 100, 50, 'C')