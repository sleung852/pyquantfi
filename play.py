class Apple:
    def __init__(self):
        print('apple created')

class Orange:
     def __init__(self):
        print('orange created')   

a = Apple()
b = Apple()
c = Orange()

basket = [a, b, c]

for i in basket:
    print(type(i) == Apple)

print(all([type(i) == Apple for i in basket]))