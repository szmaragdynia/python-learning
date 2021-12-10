print("---->\n\n")

try:

    numer = int(input("podaj numer: "))
    print(numer)
    #numer/0 #ten blad tez zlapie
except:
    print("Invalid input") #jesli ktos nie poda inta, program sie nie wysypuje tylko leci dalej xd
        #to jest zbyt ogolne except, bo bedzie wszystko łapać, 

try:
    numer2 = int(input("Podaj numerek2: "))
    print(numer2)
    numer2/0
except ZeroDivisionError:
    print("You tried to divide by zero")
except ValueError:
    print("You entered invalid value")

#mozna tez tak:
try:
    numer3 = int(input("Podaj numerek3: "))
    print(numer3)
    #numer3/0
except ZeroDivisionError as err:
    print(err)
except ValueError as err:
    print(err)


#mam cos wiecej w zakldakch, jest jescze blok "finally" ktory sie zawzse odpali, chyba

print("\n\n<-----")