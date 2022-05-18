'''
https://projecteuler.net/archives ; id=3

The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143 ?
'''
#todo: recursive? Doubtful, but haven't thought about it yet.

#returning given number of primes. 
# #If given a list of primes, it will add number_of_new_primes to it. Giving other lists undefined.
def generate_primes(number_of_new_primes, output_primes = []): 
    if number_of_new_primes < 1:
        return "Too few primes expected by user"

    output_primes_size = len(output_primes)
    if output_primes_size == 0:
        output_primes.append(2) #add first prime number manually
    
    suspected_prime = 2 #to start with 2(!)
    #do, until number_of_new_primes primes are added
    while not (output_primes_size + number_of_new_primes == len(output_primes)): 
        for prime in output_primes:
            if suspected_prime % prime == 0: #if new number is divisible by some prime
                break #leave for loop, and increment again
        else: #if no known primes divided "incremented" ; executes after the loop completes normally
            output_primes.append(suspected_prime) # add primes to list
        suspected_prime+=1
    return output_primes

'''
primes = generate_primes(5)
print (primes)
primes2 = generate_primes(3,primes)
print (primes2)
'''





#divide by every prime number starting from last element, which in 1-sized array is first. 
#keep dividing until impossible. Then find new prime number, do the same with it.
#continue until you divide by all factors. Then, the biggest prime number in prime numbers array is your result.
primes = []
input_number = 600851475143
generate_primes(1, primes)
while input_number != 1:
    if input_number % primes[-1] == 0: #if what remained is divisible by biggest so far
        input_number = input_number/primes[-1] 
    else:
        generate_primes(1,primes) 
print(primes)

