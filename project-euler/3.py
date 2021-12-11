'''
The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143 ?
'''

def generate_primes(output_primes,number_of_new_primes): #tablica do ktorej ci bd zw
    if number_of_new_primes < 1:
        return -1
    output_primes.append(2)
    if number_of_new_primes == 1:
        return output_primes
    incremented = 1 #to start with 2(!)
    primes_size = len(output_primes)
    while not (primes_size + number_of_new_primes == len(output_primes)): #do until number_of_new_primes primes are added
        incremented+=1
        #print(f"in while, incremented = {incremented}")
        #print(f"primes: {output_primes}")
        for prime in output_primes:
            if incremented % prime == 0: #if new number is divisible by some prime
                break #leave for loop, and increment again
        else: #if no known primes divided "incremented" 
            output_primes.append(incremented) # add primes to list
    return output_primes

primes = []
generate_primes(primes,1)
print (primes)
generate_primes(primes,1)
print (primes)
generate_primes(primes,1)
print (primes)
'''
primesss = []
generate_primes(primesss, 2)
print(primesss)
generate_primes(primesss, 2)
print(primesss)
'''


#finding the biggest factor of a number input_number
#mialem sprawdzac czy dana liczba pierwsza dzieli mi liczbe,
# jesli tak to bym podzielil, sprawdzil czy dalej dzieli i podzielil itd
#no i w sumie wiedzialbym ze ostatnia liczba jest najwieksza, dopiero gdyby kolejna liczba pierwsza 
#byla wieksza od liczby sprawdzanej - ale ten przeskok moze byc koszmarnie duzy, wiec to podejscie
#jest debilne xD
#--
#lepiej bedzie zbierac liczby ktore dziela moja liczbe sprawdzana i mnozyc je i sprawdzac czy
#rownaja sie sprawdzanej. Bingo.
# w sumie mozna by tez moja funkcje zmodyfikowac i dac ograniczenie w parametrach. 
# I wtedy by bylo prosciej. Ale walic, zmeczony jestem max.

#to wszystko co wyzej napisalem jest bez znaczenia, boze. to jest trywialne, i mam to rozwiazanie
# przed nosem od dawna. zal.pl
'''
primes = []
input_number = 20
generate_primes(primes,1)
while input_number != 1:
    print("while input number: ", input_number)
    print("while primes: ", primes)
    if input_number % primes[-1] == 0: #if what remained is divisible by biggest so far
        input_number = input_number/primes[-1] 
        print("if after division input number: ", input_number)
    else:
        generate_primes(primes,1) #jesli nie jest podzielny, wygeneruj nowa l. pierwsza i jeszcze raz
        print("else primes: ",primes)
print(primes)
'''