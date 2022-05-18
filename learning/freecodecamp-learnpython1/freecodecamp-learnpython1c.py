print("---->\n\n")

kolory = ["bialy", "Zolty", "zielony", "jakistam", "czerwono" "sraczkowaty", 
                "czerwony", "sraczkowaty"]

print(kolory)
print(kolory[0])
print(kolory[1])
print(kolory[-0])
print(kolory[-1])
print(kolory[1:])
print(kolory[1:4])
kolory[1] = "czorny"
print(kolory[1:4])
print(kolory)
print(kolory[-1:-3])
print(kolory[-3:-1])
print(kolory[3:1])
print(kolory[-4:5])

#---------------------------------------
print("\n")
pieski = ["beagle", "dog", "sznaucer"]

pieski.extend(kolory)
print(pieski)

kolory.extend(kolory)
print(kolory)

pieski.append("wyyyyyyyyyżeł")
print(pieski)

pieski.insert(0,"abecadlak")
print(pieski)

pieski.remove("bialy")
print(pieski)

print(kolory)
kolory.pop()
print(kolory)

print(kolory.index("zielony"))
print(kolory.count("badcolor"))
print(kolory.count("greenybadcolor"))

kolory.sort()
print(kolory)

kolory.reverse()
print(kolory)

numerki = [1,5,6,4,234,6,8,-4,      10-10]
numerki.sort()
print(numerki)

print("---------")
numerki2 = numerki
numerki_copy = numerki.copy()
print(numerki2)
del numerki[1:3]
print("numerki: ")
print(numerki)
print("numerki2: ")
print(numerki2)
print("numerki_copy")
print(numerki_copy)

#pieski.clear()
#print(pieski)




print("\n\n<-----")
