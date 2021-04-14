from basketoptionpricer import GeometricBasketOptionPricer, ArithmeticBasketOptionBasketPricer

case_no = 1

def test_basket_option_pricer(S1, S2, K, sigma1, sigma2, rho, kind):
    global case_no
    print(f'Test Case {case_no}')
    case_no += 1
    print('*Parameters*')
    print('S1: {}, S2: {}, K: {}, sigma1: {}, sigma2: {}, rho: {}, kind: {}'.format(S1, S2, K, sigma1, sigma2, rho, kind))
    print('\nGeometric Basket Option')
    geo = GeometricBasketOptionPricer(Ss=[S1, S2], sigmas=[sigma1, sigma2], r=0.05, T=3, K=K, rhos=rho)
    print('Value from Closed Form: {}'.format(geo.get_option_premium(kind=kind, method="closed")))
    print('Value from Monte Carlo: {}'.format(geo.get_option_premium(kind=kind, method="std_mcs", m=100000)))
    print('\nArithmetic Basket Option')
    ari = ArithmeticBasketOptionBasketPricer(Ss=[S1, S2], sigmas=[sigma1, sigma2], r=0.05, T=3, K=K, rhos=rho, m=100000)
    print('Value from Standard Monte Carlo: {}'.format(ari.get_option_premium(kind=kind, method="std_mcs")))
    print('Value from Standard Monte Carlo with CV: {}'.format(ari.get_option_premium(kind=kind, method="std_mcs_cv")))
    print()

print('**Official Test for COMP7405 Assignment 3')
print('Basket Options')
test_basket_option_pricer(100, 100, 100, 0.3, 0.3, 0.5, 'P')
test_basket_option_pricer(100, 100, 100, 0.3, 0.3, 0.9, 'P')
test_basket_option_pricer(100, 100, 100, 0.1, 0.3, 0.5, 'P')
test_basket_option_pricer(100, 100, 80, 0.3, 0.3, 0.5, 'P')
test_basket_option_pricer(100, 100, 120, 0.3, 0.3, 0.5, 'P')
test_basket_option_pricer(100, 100, 100, 0.5, 0.5, 0.5, 'P')

test_basket_option_pricer(100, 100, 100, 0.3, 0.3, 0.5, 'C')
test_basket_option_pricer(100, 100, 100, 0.3, 0.3, 0.9, 'C')
test_basket_option_pricer(100, 100, 100, 0.1, 0.3, 0.5, 'C')
test_basket_option_pricer(100, 100, 80, 0.3, 0.3, 0.5, 'C')
test_basket_option_pricer(100, 100, 120, 0.3, 0.3, 0.5, 'C')
test_basket_option_pricer(100, 100, 100, 0.5, 0.5, 0.5, 'C')
