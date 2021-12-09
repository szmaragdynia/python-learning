import freecodecamp_learnpython1i_doImport
    #a to juz widzi w swoim folderze, a do plikow teksotwych musialem dawac sciezke od cwd,
    #  ktore jest takie jak glowny workspace 
        # a kij wie, moze on do importow przeszukuje wszystko w dol, a do plikow musi byc 
        # obok i nic nie szuka sam
from freecodecamp_learnpython1i_class import Pies, QA
from freecodecamp_learnpython1i_class2 import DuzyPies

trójeczka = freecodecamp_learnpython1i_doImport.trzy

print(trójeczka)

#------------------------------
print("\n------------------------------")

pies1 = Pies("azor", "terrier", 9, True)
print("imie: " + pies1.imie)
print("wiek: " + str(pies1.wiek))
if pies1.czy_stary():
    print("stary piesek")
elif not pies1.czy_stary():
    print ("nie stary piesek ")

duzypies1 = DuzyPies("gaweł", "border collie", 9, True, 100)
print("imie: " + duzypies1.imie)
print("wiek: " + str(duzypies1.wiek))
if duzypies1.czy_stary():
    print("stary piesek")
elif not duzypies1.czy_stary():
    print ("nie stary piesek ")
        #mimo tego samego wieku, daje inny wynik, bo ta funkcja jest przeciazana w klasie dziedziczacej
#------------------------------
print("\n------------------------------")

set1 = [
    "Jakiego koloru jest Słońce?\n(a) zielonego\n(b) Żółtego\n: ",
    "Jakiego koloru jest grunt?\n(a) brązowego\n(b) białosiankowatego\n: ",
    "Jakiego koloru jest kolor zielony?\n(a) zielonego\n(b) Żółtego\n: ",
    ]

questions_and_answers = [
    QA(set1[0], "b"),
    QA(set1[1], "a"),
    QA(set1[2], "a"),
]

def run_test(questions_and_answers):
    score = 0
    for qa in questions_and_answers:
        answer = input(qa.question)
        if answer == qa.answer:
            score += 1
    print("You scored " + str(score) +" out of " + str(len(questions_and_answers)))

run_test(questions_and_answers)
