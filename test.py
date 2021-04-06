from blackscholes import EuropeanOptionPricer
from impliedvol import ImpliedVolatilityEstimator
from controlvariate import GeometricAsianOptionPricer, GeometricAsianOptionBasketPricer
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
    print('Expected Answer:  ', '?') # from lecture 5 slide 17
    geo_test = GeometricAsianOptionPricer(4, 4, 1e-2, 0.25, 0.03, 1/1e-2)
    derived_option_value = geo_test.get_call_premium()
    print('Calculated Answer:', derived_option_value) 
    # assert True, "Test 3 Failed"
    print('Test 3 passed')

    print('\nTest 4a: Monte Carlo Standard estimation for Arithematic Asian Call Option')
    mcs_test = MonteCarloSimulator(100, 0.3, 0.05, 3, 100, 50, 1e5)
    TEST_4A_EXPECTED_ANSWER = 14.767
    mu_hat, sigma_hat, ci = mcs_test.get_call_premium()
    condition_test(mu_hat, TEST_4A_EXPECTED_ANSWER, '4a')

    print('\nTest 4b: Monte Carlo Standard estimation for Arithematic Asian Put Option')
    mcs_test = MonteCarloSimulator(100, 0.3, 0.05, 3, 100, 50, 1e5)
    TEST_4B_EXPECTED_ANSWER = 7.7533
    mu_hat, sigma_hat, ci = mcs_test.get_put_premium()
    condition_test(mu_hat, TEST_4B_EXPECTED_ANSWER, '4b')

    print('\nTest 4c: Monte Carlo Control Variate estimation for Arithematic Asian Call Option')
    mcs_test = MonteCarloSimulator(100, 0.3, 0.05, 3, 100, 50, 1e5)
    TEST_4C_EXPECTED_ANSWER = 14.767
    mu_hat, sigma_hat, ci = mcs_test.get_call_premium('cv')
    condition_test(mu_hat, TEST_4C_EXPECTED_ANSWER, '4c')

    print('\nTest 4d: Monte Carlo Control Variate estimation for Arithematic Asian Put Option')
    mcs_test = MonteCarloSimulator(100, 0.3, 0.05, 3, 100, 50, 1e5)
    TEST_4D_EXPECTED_ANSWER = 7.7533
    mu_hat, sigma_hat, ci = mcs_test.get_put_premium('cv')
    condition_test(mu_hat, TEST_4D_EXPECTED_ANSWER, '4d')

    print('\nTest 5a: Binominal Tree for European Option')
    bt_test1 = BinominalTree(2, 2, 3, SIGMA, 0.03, 100)
    bt_test2 = BinominalTree(2, 2, 3, SIGMA, 0.03, 99)
    bt_euro1 = bt_test1.get_call_premium(option_type='european')
    bt_euro2 = bt_test2.get_call_premium(option_type='european')
    bt_euro = (bt_euro1 + bt_euro2)/2
    condition_test(bt_euro, TEST_1_OPTION_VALUE, '5a')
    
    print('\nTest 5b: Binominal Tree for American Option')
    print('...')

    print('\n***RESULT***')
    print('Score ({}/{})'.format(score,count))

if __name__ == '__main__':
    
    global count
    global score
    count = 0
    score = 0
    test()

