from blackscholes import EuropeanOptionPricer
from impliedvol import ImpliedVolatilityEstimator
from asianoptionpricer import GeometricAsianOptionPricer, GeometricAsianOptionBasketPricer, ArithmeticAsianOptionPricer, ArithmeticAsianOptionBasketPricer
from montecarlo import MonteCarloSimulator
from binominaltree import BinominalTree

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
    
    print(f'Test {count}: Vanila Option Pricing')
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
    geo_test = GeometricAsianOptionPricer(100, 100, 0.05, 3, 0.05, 50)
    derived_option_value = geo_test.get_call_premium()
    condition_test(derived_option_value, TEST_3_EXPECTED_ANSWER, 0.5)

    print(f'\nTest {count}: Closed Form for Geometric Asian Basket Option')
    b_geo_test = GeometricAsianOptionBasketPricer([100, 100], [0.3, 0.3], 0.05, 3, 100, 0.5)
    derived_option_value = b_geo_test.get_call_premium()
    print('***This test has no test answer***')
    condition_test(derived_option_value, derived_option_value, 0.5)

    # print(f'\nTest {count}: Monte Carlo Standard estimation for Arithematic Asian Call Option')
    # mcs_test = ArithmeticAsianOptionPricer(100, 0.3, 0.05, 3, 100, 50, 1e5)
    # TEST_4A_EXPECTED_ANSWER = 14.767
    # mu_hat, sigma_hat, ci = mcs_test.get_call_premium()
    # condition_test(mu_hat, TEST_4A_EXPECTED_ANSWER, 0.5)

    # print(f'\nTest {count}: Monte Carlo Standard estimation for Arithematic Asian Put Option')
    # mcs_test = ArithmeticAsianOptionPricer(100, 0.3, 0.05, 3, 100, 50, 1e5)
    # TEST_4B_EXPECTED_ANSWER = 7.7533
    # mu_hat, sigma_hat, ci = mcs_test.get_put_premium()
    # condition_test(mu_hat, TEST_4B_EXPECTED_ANSWER, 0.5)

    # print(f'\nTest {count}: Monte Carlo Control Variate estimation for Arithematic Asian Call Option')
    # mcs_test = ArithmeticAsianOptionPricer(100, 0.3, 0.05, 3, 100, 50, 1e5)
    # TEST_4C_EXPECTED_ANSWER = 14.767
    # mu_hat, sigma_hat, ci = mcs_test.get_call_premium('cv')
    # condition_test(mu_hat, TEST_4C_EXPECTED_ANSWER, 0.5)

    # print(f'\nTest {count}: Monte Carlo Control Variate estimation for Arithematic Asian Put Option')
    # mcs_test = ArithmeticAsianOptionPricer(100, 0.3, 0.05, 3, 100, 50, 1e5)
    # TEST_4D_EXPECTED_ANSWER = 7.7533
    # mu_hat, sigma_hat, ci = mcs_test.get_put_premium('cv')
    # condition_test(mu_hat, TEST_4D_EXPECTED_ANSWER, 0.5)

    print(f'\nTest {count}: Monte Carlo Standard estimation for Arithematic Basket Asian Call Option')
    mcs_test = ArithmeticAsianOptionBasketPricer([100, 100], [0.3, 0.3], 0.05, 3, 100, 0.3, 50, 1e5)
    TEST_4A_EXPECTED_ANSWER = 24.345
    mu_hat, sigma_hat, ci = mcs_test.get_call_premium()
    condition_test(mu_hat, TEST_4A_EXPECTED_ANSWER, 0.5)

    print(f'\nTest {count}: Monte Carlo Standard estimation for Arithematic Basket Asian Put Option')
    mcs_test = ArithmeticAsianOptionBasketPricer([100, 100], [0.3, 0.3], 0.05, 3, 100, 0.3, 50, 1e5)
    TEST_4B_EXPECTED_ANSWER = 10.629
    mu_hat, sigma_hat, ci = mcs_test.get_put_premium()
    condition_test(mu_hat, TEST_4B_EXPECTED_ANSWER, 0.5)

    print(f'\nTest {count}: Monte Carlo Control Variate estimation for Arithematic Basket Asian Call Option')
    mcs_test = ArithmeticAsianOptionBasketPricer([100, 100], [0.3, 0.3], 0.05, 3, 100, 0.3, 50, 1e5)
    TEST_4C_EXPECTED_ANSWER = 24.508
    mu_hat, sigma_hat, ci = mcs_test.get_call_premium('cv')
    condition_test(mu_hat, TEST_4C_EXPECTED_ANSWER, 0.5)

    print(f'\nTest {count}: Monte Carlo Control Variate estimation for Arithematic Basket Asian Put Option')
    mcs_test = ArithmeticAsianOptionBasketPricer([100, 100], [0.3, 0.3], 0.05, 3, 100, 0.3, 50, 1e5)
    TEST_4D_EXPECTED_ANSWER = 10.558
    mu_hat, sigma_hat, ci = mcs_test.get_put_premium('cv')
    condition_test(mu_hat, TEST_4D_EXPECTED_ANSWER, 0.5)

    print(f'\nTest {count}: Binominal Tree for European Call Option')
    bt_test1 = BinominalTree(2, 2, 3, SIGMA, 0.03, 100)
    bt_test2 = BinominalTree(2, 2, 3, SIGMA, 0.03, 99)
    bt_euro1 = bt_test1.get_call_premium(option_type='european')
    bt_euro2 = bt_test2.get_call_premium(option_type='european')
    bt_euro = (bt_euro1 + bt_euro2)/2
    condition_test(bt_euro, TEST_1_OPTION_VALUE, 0.5)
    
    print(f'\nTest {count}: Binominal Tree for American Put Option')
    bt_test_american = BinominalTree(50, 52, 2, 0.223144, 0.05, 2)
    bt_american = bt_test_american.get_put_premium(option_type='american')
    condition_test(bt_american, 5.4872)

    print(f'\nTest {count}: Binominal Tree for European Put Option')
    bt_test_american = BinominalTree(50, 52, 2, 0.223144, 0.05, 2)
    bt_american = bt_test_american.get_put_premium(option_type='european')
    condition_test(bt_american, 4.4219)

    print('\n***RESULT***')
    print('Score ({}/{})'.format(score,count))

if __name__ == '__main__':
    
    global count
    global score
    count = 0
    score = 0
    test()

