'''
https://projecteuler.net/archives ; id=4
A palindromic number reads the same both ways. 
The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.

Find the largest palindrome made from the product of two 3-digit numbers.
'''
#todo: recursive?
#todo: more elegant approach, maybe task-specific?

from math import *

def is_palindrome(tekst):
    stoppoint = ceil(len(tekst)/2.0)
    #print("stoppoint: ", stoppoint)
    for i in range(stoppoint):
        if tekst[i] != tekst[-(1 + i)]:
            #print("false, i= ",i)
            return False
        else:
            #print("continue, i= ",i)
            continue
    return True        



start = 999
stop = 900
max_palindrome = 0
for i in range(start, stop-1, -1):
    #print("for i: i =rt",i)
    for j in range(start, stop-1, -1):
        #print(f"for j: i = {i}, j = {j}, i*j = {i*j}")
        if is_palindrome(str(i*j)) and i*j > max_palindrome:
            max_palindrome = i*j

print(max_palindrome)


#first ideas, maybe more opeartion heavy. Abandoned.
    #this does this(more-or-less):
    #number1 * number2; number1 * (number2-1); ...; number1 * (number2-step)
    #(number1-1) * number2; (number1-1) * (number2-1); ...; (number1-1) * (number2-step)
    #...
    #(number1-step) * number2; (number1-step) * (number2-1); ...; (number1-step) * (number2-step)
    #---
    #(number1-step) * (number2-step); (number1-step) * (number2-step-1); ...; (number1-step) * (number2-step-step)
    #etc
    #trying to make this semi-optimal xD





