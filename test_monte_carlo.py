from asianoptionpricer import GeometricAsianOptionPricer, ArithmeticAsianOptionPricer

print(f'\nTest Monte Carlo standard estimation for Geometric Asian Option')
geo_test = GeometricAsianOptionPricer(100, 100, 3, 0.3, 0.05, 50)
derived_option_value = geo_test.get_call_premium(method='mcs', m=100000)
print(derived_option_value)