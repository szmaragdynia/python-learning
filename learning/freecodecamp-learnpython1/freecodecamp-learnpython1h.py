print("---->\n\n")


plik = open("learning/freecodecamp-learnpython1/listazakupow.txt", "r")
#turbowazne: r- tylko czytanie
#            w - zapisuje w tym pliku, TZN NADPISUJE CALOSC!
#            r+ - mozesz czytac i "w", czyli TEZ NADPISAC
#            a - append - dodac na koneic. JAK DODASZ TO NIE POPRAWISZ, UWAZAJ! 

print( plik.readable() )
print("---")
print( plik.readlines() )
plik.seek(0) #wracam na poczatek pliku
print( plik.readlines()[2] )
plik.seek(0) #wracam na poczatek pliku
print("---")
print ( plik.readline() )
print ( plik.readline() )
plik.seek(0) #wracam na poczatek pliku
print("---")
for line in plik.readlines():
    print(line)

plik.close()

#jesli plik nie istnieje to go nie tworzy
#plik = open("learning/freecodecamp-learnpython1/asdfg.txt", "r")
#plik.close()

#wykomentowane bo nie ma sensu ciagle dodawac tego do konca pliku xD 
#plik = open("learning/freecodecamp-learnpython1/listazakupow.txt", "a")
#plik.write("- książki")
#plik.close()

#plik ostaje utworzony
plik = open("learning/freecodecamp-learnpython1/asdfghj.txt", "a")
plik.write("- książki")
plik.close()

#zawartosc zostaje nadpisana
plik = open("learning/freecodecamp-learnpython1/asdfghj.txt", "w")
plik.write("a")
plik.close()

#plik = open("learning/freecodecamp-learnpython1/aaaaa.txt", "r+")
        #r+ - write and read; wskaznik na poczatek pliku. brak pliku = error MOZNA NADPISAC!
#plik.close()
plik = open("learning/freecodecamp-learnpython1/bbb.txt", "a+")
    #a+ - append and read; wskaznik na koniec pliku. NIE MOZNA USUWAC

plik.close()
   

#jet wiecej trybow i roznych dobrych praktyk, ale nie mam juz na to sily ani czasu, jest w zakladkach 

print("\n\n<-----")