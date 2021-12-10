
from math import * #do floor i ceil

print("---->\n\n")
print("Hello world")
#-------------------------------------

tree_type = "Fir"
tree_height = 100
print("There was a lonely tree in a field, a tree of " + tree_type)
print("and it was " + str(tree_height) + " metres tall!")

tree_type = "birch"
print("And that " + tree_type +" was glad it was alive")

#---------------------------------------
jakisstring = "Ale jaja"

print(jakisstring.upper())
print(jakisstring.lower())
print(jakisstring.isupper())
print(jakisstring.upper().isupper())
print(len(jakisstring))
print(jakisstring[5])
print(jakisstring[5:7])
print(jakisstring.index("l"))
print(jakisstring.index("a"))
print(jakisstring.index("aja"))
print(jakisstring.index("le ja"))
#ponizsze sie zesrywa, i slusznie
# print(jakisstring.index("les"))
print(jakisstring.replace("a","e"))

#----------------------------------------
print(5)
print(5*3)
numerek = -4
print(numerek)
#print(numerek + "dupa") nope, ofc
print(str(numerek) + "dupa")
print(abs(numerek))
print(pow(numerek, 3))
print(max(numerek, pow(numerek,3)))
print(round(3.7))
print(round(3.2))
#DO TEGO NIZEJ MUSZE ZAIMPORTOWAC MATH
print(floor(3.7))
print(ceil(3.2))
print(sqrt(81))



#----------------z neta 
for i in range(10):
    print(i, end='') #bez nowej linii

print('.','.','.','.','.','.','.') #normlanie ze spacja
print('.','.','.','.','.','.','.', sep='') #tutaj bez

koszt = 100
nazwa = "laleczka"
print("Nazwa produktu to " + nazwa + " a jego cena to " + str(koszt)) #sklejam stringa i jego jako arg
print("Nazwa produktu to",nazwa,"a jego cena to",koszt) #nie trzeba spacji. 5 argumentow i one robia stringa
print("Nazwa produktu to {} a jego cena to {}".format(nazwa, koszt))
print(f"Nazwa produktu to {nazwa} a jego cena to {koszt}")

#inna rzecz

print("No i patrz na to:", "-separator-".join(["ab","cd","gg","hy"]))

tablica =[]
for i in range(10):
    tablica.append(str(i))

print(tablica)

print("No i patrz na to2:", "-separator-".join(tablica))
#wow ale to jest zajebiste xD
print("\n\n<-----")
