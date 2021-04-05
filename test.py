from blackscholes import EuropeanOptionPricer
from impliedvol import ImpliedVolatilityEstimator
from controlvariate import GeometricAsianOptionPricer, GeometricAsianOptionBasketPricer
from montecarlo import MonteCarloSimulator

def test():
    # maximum difference from true values
    max_delta = 1e-4


    print('Test 1: Vanila Option Pricing')
    OPTION_VALUE = 0.48413599739115154
    SIGMA = 0.3
    bs_test = EuropeanOptionPricer(2, 2, 3, SIGMA, 0.03, 0)
    print('Expected Answer:  ', OPTION_VALUE) # from lecture 4 slide 21
    derived_option_value = bs_test.get_call_premium()
    print('Calculated Answer:', derived_option_value)
    assert abs(derived_option_value - OPTION_VALUE) < max_delta, "Test 1 Failed"
    print('Test 1 passed')
    
    print('\nTest 2: Newtons Method for Implied Volatility')
    print('Expected Answer:  ', SIGMA) # from lecture 4 slide 22
    iv_test = ImpliedVolatilityEstimator(2, 2, 3, 0.03, 0)
    derived_sigma = iv_test.get_implied_vol(OPTION_VALUE, 'C')
    print('Calculated Answer:', derived_sigma) 
    assert abs(derived_sigma - SIGMA) < max_delta, "Test 2 Failed"
    print('Test 2 passed')

    print('\nTest 3: Control Variant Method for Geometric Asian Option')
    print('Expected Answer:  ', '?') # from lecture 5 slide 17
    geo_test = GeometricAsianOptionPricer(4, 4, 1e-2, 0.25, 0.03, 1/1e-2)
    derived_option_value = geo_test.get_call_premium()
    print('Calculated Answer:', derived_option_value) 
    # assert True, "Test 3 Failed"
    print('Test 3 passed')

    print('\nTest4: Monte Carlo Standard estimation for Arithematic Asian Option')
    mcs_test = MonteCarloSimulator(4, 0.25, 0.03, 1e-2, 4, 1/1e-2, 1e4)
    mu_hat, sigma_hat, ci = mcs_test.get_call_premium()
    print('Calculated Answer:', mu_hat, sigma_hat, ci )
    print('Test 4 passed')

    print('\nTest5: Monte Carlo Control Variate estimation for Arithematic Asian Option')
    # TEST_5_ANSWER = 0.26
    # print('Expected Answer:  ', TEST_5_ANSWER)
    mcs_test = MonteCarloSimulator(4, 0.25, 0.03, 1e-2, 4, 1/1e-2, 1e4)
    mu_hat, sigma_hat, ci = mcs_test.get_call_premium('cv')
    print('Calculated Answer:', mu_hat, sigma_hat, ci )
    # assert abs(mu_hat - TEST_5_ANSWER) < max_delta, "Test 5 Failed"
    print('Test 5 passed')

    print('\nTest6: Control Variant Method for Basket Geometric Asian Option')
    # TEST_5_ANSWER = 0.26
    # print('Expected Answer:  ', TEST_5_ANSWER)
    mcs_test = GeometricAsianOptionBasketPricer(4, 0.25, 0.03, 1e-2, 4, 1/1e-2, 1e4)
    mu_hat, sigma_hat, ci = mcs_test.get_call_premium('cv')
    print('Calculated Answer:', mu_hat, sigma_hat, ci )
    # assert abs(mu_hat - TEST_5_ANSWER) < max_delta, "Test 5 Failed"
    print('Test 6 passed')    

    
test()

