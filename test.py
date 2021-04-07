from blackscholes import EuropeanOptionPricer
from impliedvol import ImpliedVolatilityEstimator
from controlvariate import GeometricAsianOptionPricer, GeometricAsianOptionBasketPricer, GeometricAsianOptionPricer2
from montecarlo import MonteCarloSimulator
from binominaltree import BinominalTree

def condition_test(derived_val, expected_val, test_no, max_delta = 1e-4):
    global count
    global score
    
    count += 1
    print('Expected Answer:', expected_val)
    print('Derived Answer:', derived_val)
    test_str = 'Test {}'.format(test_no)
    if abs(derived_val - expected_val) < max_delta:
        print('{} passed'.format(test_str))
        score += 1
    else:
        print('{} failed'.format(test_str))

def test():
    # maximum difference from true values
    
    print('Test 1: Vanila Option Pricing')
    TEST_1_OPTION_VALUE = 0.48413599739115154 # from lecture 4 slide 21
    SIGMA = 0.3 # from lecture 4 slide 22
    bs_test = EuropeanOptionPricer(2, 2, 3, SIGMA, 0.03, 0)
    derived_option_value = bs_test.get_call_premium()
    condition_test(derived_option_value, TEST_1_OPTION_VALUE, '1')
    
    print('\nTest 2: Newtons Method for Implied Volatility')
    iv_test = ImpliedVolatilityEstimator(2, 2, 3, 0.03, 0)
    derived_sigma = iv_test.get_implied_vol(TEST_1_OPTION_VALUE, 'C')
    condition_test(derived_sigma, SIGMA, '2')

    print('\nTest 3: Closed Form for Geometric Asian Option')
    TEST_3_EXPECTED_ANSWER = 13.259
    geo_test = GeometricAsianOptionPricer(100, 100, 0.05, 3, 0.05, 50)
    derived_option_value = geo_test.get_call_premium()
    condition_test(derived_option_value, TEST_3_EXPECTED_ANSWER, '3', 0.5)

    print('\nTest 4a: Monte Carlo Standard estimation for Arithematic Asian Call Option')
    mcs_test = MonteCarloSimulator(100, 0.3, 0.05, 3, 100, 50, 1e5)
    TEST_4A_EXPECTED_ANSWER = 14.767
    mu_hat, sigma_hat, ci = mcs_test.get_call_premium()
    condition_test(mu_hat, TEST_4A_EXPECTED_ANSWER, '4a', 0.5)

    print('\nTest 4b: Monte Carlo Standard estimation for Arithematic Asian Put Option')
    mcs_test = MonteCarloSimulator(100, 0.3, 0.05, 3, 100, 50, 1e5)
    TEST_4B_EXPECTED_ANSWER = 7.7533
    mu_hat, sigma_hat, ci = mcs_test.get_put_premium()
    condition_test(mu_hat, TEST_4B_EXPECTED_ANSWER, '4b', 0.5)

    print('\nTest 4c: Monte Carlo Control Variate estimation for Arithematic Asian Call Option')
    mcs_test = MonteCarloSimulator(100, 0.3, 0.05, 3, 100, 50, 1e5)
    TEST_4C_EXPECTED_ANSWER = 14.767
    mu_hat, sigma_hat, ci = mcs_test.get_call_premium('cv')
    condition_test(mu_hat, TEST_4C_EXPECTED_ANSWER, '4c', 0.5)

    print('\nTest 4d: Monte Carlo Control Variate estimation for Arithematic Asian Put Option')
    mcs_test = MonteCarloSimulator(100, 0.3, 0.05, 3, 100, 50, 1e5)
    TEST_4D_EXPECTED_ANSWER = 7.7533
    mu_hat, sigma_hat, ci = mcs_test.get_put_premium('cv')
    condition_test(mu_hat, TEST_4D_EXPECTED_ANSWER, '4d', 0.5)

    print('\nTest 5: Binominal Tree for European Call Option')
    bt_test1 = BinominalTree(2, 2, 3, SIGMA, 0.03, 100)
    bt_test2 = BinominalTree(2, 2, 3, SIGMA, 0.03, 99)
    bt_euro1 = bt_test1.get_call_premium(option_type='european')
    bt_euro2 = bt_test2.get_call_premium(option_type='european')
    bt_euro = (bt_euro1 + bt_euro2)/2
    condition_test(bt_euro, TEST_1_OPTION_VALUE, '5', 0.5)
    
    print('\nTest 6a: Binominal Tree for American Put Option')
    bt_test_american = BinominalTree(50, 52, 2, 0.223144, 0.05, 2)
    bt_american = bt_test_american.get_put_premium(option_type='american')
    condition_test(bt_american, 5.4872, '6a')

    print('\nTest 6b: Binominal Tree for European Put Option')
    bt_test_american = BinominalTree(50, 52, 2, 0.223144, 0.05, 2)
    bt_american = bt_test_american.get_put_premium(option_type='european')
    condition_test(bt_american, 4.4219, '6b')

    print('\n***RESULT***')
    print('Score ({}/{})'.format(score,count))

if __name__ == '__main__':
    
    global count
    global score
    count = 0
    score = 0
    test()

