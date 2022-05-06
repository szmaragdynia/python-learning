'''
A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,

a^2 + b^2 = c^2
For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the eproduct abc.
'''
import math

a = 0
b = 0
c = 0

def find_triplet(amount):
    for i in range(1,100):
        for j in range(1,100):
            if math.sqrt(i**2 + j**2).is_integer():
                c = math.sqrt(i**2 + j**2)


while (a+b+c < 1000):