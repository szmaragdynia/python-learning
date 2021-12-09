print("---->\n\n")

i = 1
while i<10:
    print(i)
    i+=1

klucz = "a"
asd =""
while asd != klucz:
    asd = input("Podaj litere \"a\": ")
        # "asd" musi byc zadeklarowane! wczesniej ta zmienna nazwalem "input" i on sie wtedy odpala,
        # ale nie wiem skad bierze ta zmienna. gdy mu wtedy podam "a" to ladnie konczy, ale gdy 
        #podam inna litere to rzuca bledem "str is not calleable" czy cos takiego

#-----------------------------------
print("\n------------------")

for ltr in "O cie panie ale jajca":
    print(ltr)


kolory = ["bialy", "Zolty", "zielony", "jakistam", "czerwono" "sraczkowaty", 
                "czerwony", "sraczkowaty"]
lista_tuplów = [(1,2), (2,5,3), (3,1)]

print("---")
for klr in kolory:
    print(klr)

print("---")
for tpl in lista_tuplów:
    print(tpl)

print("---")
for i in range(10):
    print(i)

print("---")
for i in range(3, 10):
    print(i)

print("---")
for i in range(len(kolory)):
    print(kolory[i])
    if i == 0: print("\tfirst time")
    else: print("\tnot first time")

print("---")
#ten program pisze,bo mimo ze niby prosty, to uczy myslenia po pythonowemu jakos
def potega(podstawa, wykladnik):
    wynik = 1
    for i in range(wykladnik):         #for i in wykladnik: 'int' object is not iterable
        wynik = wynik*podstawa
    return wynik

print(potega(2,3))

print("\n\n------------")
siatka = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [0]
]

print(siatka)
print(siatka[0][0])
print(siatka[1][2])

for rOW in siatka: #pisze rOW bo jak jest tak ladnie to mam zludzenie ze to keyword
    print(rOW)

for rOW in siatka:
    for COl in rOW:
        print(COl)

print("\n\n------------")
#ten program tez robie z tutka, bo on tez prezentuje pythonowskie podejscie
#w C++ bym po prostu chyba skopiowal i na danym indeksie podmienial, a tutaj on przepisuje. 
#Ale w sumie tak jak on tez moglbym...
def translator(tekst):
    przetlumaczone =""
    for ltr in tekst:
        if ltr not in "AEOUIYaeouiy": #mozna if ltr.lower not in "aeouiy" - wydajniej
            przetlumaczone = przetlumaczone + ltr  
        else: przetlumaczone = przetlumaczone + "g"
            #ok, czyli te "for costam in costam2" to on w bebechach a la iteruje po indeksach,
            #i od razu "dereferencjuje" obiekt przy kazdej iteracji... 
    return przetlumaczone
print(translator("No i co by pies na to powiedział"))

'''mozna tez tak komentowac

ale podobno lepiej # tymi dziadami xD'''

print("\n\n<-----")