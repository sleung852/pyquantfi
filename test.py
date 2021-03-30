from blackscholes import EuropeanOptionPricer
from impliedvol import ImpliedVolatilityEstimator

def test_blackscholesextendedmodel():
    # maximum difference from true values
    max_delta = 1e-4


    print('Test 1: Vanila Option Pricing')
    OPTION_VALUE = 0.48413599739115154
    SIGMA = 0.3
    bs_test = EuropeanOptionPricer(2, 2, 3, SIGMA, 0.03, 0)
    print('Expected Answer:  ', OPTION_VALUE) # from lecture 4 slide 21
    derived_option_value = bs_test.get_call_premium()
    print('Calculated Answer:', derived_option_value)
    assert (derived_option_value - OPTION_VALUE) < max_delta, "Test 1 Failed"
    print('Test 1 passed')
    
    print('\nTest 2: Newtons Method for Implied Volatility')
    print('Expected Answer:  ', SIGMA) # from lecture 4 slide 22
    iv_test = ImpliedVolatilityEstimator(2, 2, 3, 0.03, 0)
    derived_sigma = iv_test.get_implied_vol(OPTION_VALUE, 'C')
    print('Calculated Answer:', derived_sigma) 
    assert (derived_sigma - SIGMA) < max_delta, "Test 1 Failed"
    print('Test 2 passed')
    
test_blackscholesextendedmodel()

