import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from pyquantfi.blackscholes import EuropeanOptionPricer
from pyquantfi.impliedvol import ImpliedVolatilityEstimator
from pyquantfi.asianoptionpricer import GeometricAsianOptionPricer, ArithmeticAsianOptionPricer
from pyquantfi.basketoptionpricer import ArithmeticBasketOptionBasketPricer, GeometricBasketOptionPricer
from pyquantfi.binominaltree import BinominalTree

import numpy as np

def condition_test(derived_val, expected_val, max_delta = 1e-4):
    global count
    global score

    print('Expected Answer:', expected_val)
    print('Derived Answer:', derived_val)
    test_str = 'Test {}'.format(count)
    if abs(derived_val - expected_val) < max_delta:
        print('{} passed'.format(test_str))
        score += 1
    else:
        print('{} failed'.format(test_str))
    count += 1

def test():
    global count
    # maximum difference from true values
    
    print(f'\nTest {count}: Vanila Option Pricing')
    TEST_1_OPTION_VALUE = 0.48413599739115154 # from lecture 4 slide 21
    SIGMA = 0.3 # from lecture 4 slide 22
    bs_test = EuropeanOptionPricer(2, 2, 3, SIGMA, 0.03, 0)
    derived_option_value = bs_test.get_call_premium()
    condition_test(derived_option_value, TEST_1_OPTION_VALUE)
    
    print(f'\nTest {count}: Newtons Method for Implied Volatility')
    iv_test = ImpliedVolatilityEstimator(2, 2, 3, 0.03, 0)
    derived_sigma = iv_test.get_implied_vol(TEST_1_OPTION_VALUE, 'C')
    condition_test(derived_sigma, SIGMA)

    print(f'\nTest {count}: Closed Form for Geometric Asian Option')
    TEST_3_EXPECTED_ANSWER = 13.259
    geo_test = GeometricAsianOptionPricer(100, 100, 3, 0.3, 0.05, 50)
    derived_option_value = geo_test.get_call_premium()
    condition_test(derived_option_value, TEST_3_EXPECTED_ANSWER, 0.5)

    print(f'\nTest {count}: Monte Carlo standard estimation for Geometric Asian Option')
    TEST_3_EXPECTED_ANSWER = 13.286
    geo_test = GeometricAsianOptionPricer(100, 100, 3, 0.3, 0.05, 50)
    derived_option_value = geo_test.get_call_premium(method='std_mcs', m=100000)
    condition_test(derived_option_value, TEST_3_EXPECTED_ANSWER, 0.5)

    print(f'\nTest {count}: Closed Form for Geometric Asian Basket Option')
    b_geo_test = GeometricBasketOptionPricer([100, 100], [0.3, 0.3], 0.05, 3, 100, 0.5)
    derived_option_value = b_geo_test.get_call_premium()
    condition_test(derived_option_value, 22.102, 0.5)

    print(f'\nTest {count}: Monte Carlo Standard estimation for Geometric Asian Basket Option')
    b_geo_test = GeometricBasketOptionPricer([100, 100], [0.3, 0.3], 0.05, 3, 100, 0.5)
    derived_option_value = b_geo_test.get_call_premium()
    condition_test(derived_option_value, 21.948, 0.5)

    print(f'\nTest {count}: Monte Carlo Standard estimation for Arithematic Asian Call Option')
    mcs_test = ArithmeticAsianOptionPricer(100, 0.3, 0.05, 3, 100, 50, 1e5)
    TEST_4A_EXPECTED_ANSWER = 14.767
    mu_hat = mcs_test.get_call_premium()
    condition_test(mu_hat, TEST_4A_EXPECTED_ANSWER, 0.5)

    print(f'\nTest {count}: Monte Carlo Standard estimation for Arithematic Asian Put Option')
    mcs_test = ArithmeticAsianOptionPricer(100, 0.3, 0.05, 3, 100, 50, 1e5)
    TEST_4B_EXPECTED_ANSWER = 7.7533
    mu_hat = mcs_test.get_put_premium()
    condition_test(mu_hat, TEST_4B_EXPECTED_ANSWER, 0.5)

    print(f'\nTest {count}: Monte Carlo Control Variate estimation for Arithematic Asian Call Option')
    mcs_test = ArithmeticAsianOptionPricer(100, 0.3, 0.05, 3, 100, 50, 1e5)
    TEST_4C_EXPECTED_ANSWER = 14.767
    mu_hat = mcs_test.get_call_premium('std_mcs_cv')
    condition_test(mu_hat, TEST_4C_EXPECTED_ANSWER, 0.5)

    print(f'\nTest {count}: Monte Carlo Control Variate estimation for Arithematic Asian Put Option')
    mcs_test = ArithmeticAsianOptionPricer(100, 0.3, 0.05, 3, 100, 50, 1e5)
    TEST_4D_EXPECTED_ANSWER = 7.7533
    mu_hat = mcs_test.get_put_premium('std_mcs_cv')
    condition_test(mu_hat, TEST_4D_EXPECTED_ANSWER, 0.5)

    print(f'\nTest {count}: Monte Carlo Standard estimation for Arithematic Basket Asian Call Option')
    mcs_test = ArithmeticBasketOptionBasketPricer([100, 100], [0.3, 0.3], 0.05, 3, 100, 0.5, 1e5)
    TEST_4A_EXPECTED_ANSWER = 24.345
    mu_hat = mcs_test.get_call_premium()
    condition_test(mu_hat, TEST_4A_EXPECTED_ANSWER, 1)

    print(f'\nTest {count}: Monte Carlo Standard estimation for Arithematic Basket Asian Put Option')
    mcs_test = ArithmeticBasketOptionBasketPricer([100, 100], [0.3, 0.3], 0.05, 3, 100, 0.5, 1e5)
    TEST_4B_EXPECTED_ANSWER = 10.629
    mu_hat = mcs_test.get_put_premium()
    condition_test(mu_hat, TEST_4B_EXPECTED_ANSWER, 1)

    print(f'\nTest {count}: Monte Carlo Control Variate estimation for Arithematic Basket Asian Call Option')
    mcs_test = ArithmeticBasketOptionBasketPricer([100, 100], [0.3, 0.3], 0.05, 3, 100, 0.5, 1e5)
    TEST_4C_EXPECTED_ANSWER = 24.508
    mu_hat = mcs_test.get_call_premium('std_mcs_cv')
    condition_test(mu_hat, TEST_4C_EXPECTED_ANSWER, 1)

    print(f'\nTest {count}: Binominal Tree for European Call Option')
    bt_test1 = BinominalTree(2, 2, 3, SIGMA, 0.03, 100)
    bt_test2 = BinominalTree(2, 2, 3, SIGMA, 0.03, 99)
    bt_euro1 = bt_test1.get_call_premium(option_type='european')
    bt_euro2 = bt_test2.get_call_premium(option_type='european')
    bt_euro = (bt_euro1 + bt_euro2)/2
    condition_test(bt_euro, TEST_1_OPTION_VALUE, 0.5) # from lecture
    
    print(f'\nTest {count}: Binominal Tree for American Put Option')
    bt_test_american = BinominalTree(50, 52, 2, 0.223144, 0.05, 2)
    bt_american = bt_test_american.get_put_premium(option_type='american')
    condition_test(bt_american, 5.4872) # from lecture

    print(f'\nTest {count}: Binominal Tree for European Put Option')
    bt_test_american = BinominalTree(50, 52, 2, 0.223144, 0.05, 2)
    bt_american = bt_test_american.get_put_premium(option_type='european')
    condition_test(bt_american, 4.4219) # provided in Moodle

    print(f'\nTest {count}: Binominal Tree for American Put Option')
    bt_test_american = BinominalTree(50, 40, 2, 0.4, 0.1, 200)
    bt_american = bt_test_american.get_put_premium(option_type='american')
    condition_test(bt_american, 3.418464) # provided in Moodle

    print(f'\nTest {count}: Binominal Tree for American Put Option')
    bt_test_american = BinominalTree(50, 50, 2, 0.4, 0.1, 200)
    bt_american = bt_test_american.get_put_premium(option_type='american')
    condition_test(bt_american, 7.467612) # provided in Moodle

    print(f'\nTest {count}: Binominal Tree for American Put Option')
    bt_test_american = BinominalTree(50, 70, 2, 0.4, 0.1, 200)
    bt_american = bt_test_american.get_put_premium(option_type='american')
    condition_test(bt_american, 20.83142) # provided in Moodle

    print('\n***RESULT***')
    print('Score ({}/{})'.format(score,count))

    print('\n\n**Bonus Tests**')
    print(f'\nTest {count}: Monte Carlo Control Variate estimation for Three Assets Arithematic Basket Asian Put Option')
    rhos = np.array([[1,0.5, 0.5], [0.5,1, 0.5], [0.5,0.5, 1]])
    mcs_test = ArithmeticBasketOptionBasketPricer([100, 100], [0.3, 0.3], 0.05, 3, 100, rhos, 1e5)
    mu_hat = mcs_test.get_put_premium('std_mcs_cv')
    print('Price: ', mu_hat)

    print(f'\nTest {count}: Quasi Monte Carlo estimation for Arithematic Basket Asian Call Option')
    mcs_test = ArithmeticBasketOptionBasketPricer([100, 100], [0.3, 0.3], 0.05, 3, 100, 0.5, 1e5)
    TEST_4A_EXPECTED_ANSWER = 24.345
    mu_hat = mcs_test.get_call_premium('quasi_mcs_cv')
    condition_test(mu_hat, TEST_4A_EXPECTED_ANSWER, 1)

if __name__ == '__main__':
    
    global count
    global score
    count = 0
    score = 0
    test()

