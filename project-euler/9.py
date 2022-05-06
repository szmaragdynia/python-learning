'''
A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,

a^2 + b^2 = c^2
For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the eproduct abc.
'''

def find_triplet(amount):
    for i in range(1,100):
        for j in range(1,100):
            

a = 0
b = 0
c = 0
while (a+b+c < 1000):