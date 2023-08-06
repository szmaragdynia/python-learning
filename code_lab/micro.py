# This script contains very small pieces of code that I wanted to try out. Some of them are extremely trivial, however I let them reside here anyway. 
  # this file was merged from several old, smaller files

# Function names are so simple and no information-bearing, because they are irrelevant - functions' sole purpose is to enable me to run only the part of the code I am interested in at any given moment.
  # I used to have separate files for learning, checking how things work etc., but that was too messy, and not really convenient whenever I wanted to recall something
  # Also, the location of 'import' statements is so odd due to the nature of that file

'''You could comment like that as well, 
but that is (as far as I remember) reserved for documentation(?),
so it's more proper to use hashes.
'''
# --------------------------------------------------------------------------------------------------------------------------------
def a():
  msg = "Hello World"
  print(msg)
  print("say_hello_var\n\n")

  price = 100
  item = "doll"
  print("Product name is " + item + " and its price is " + str(item)) #concatenating strings(!); this way does NOT insert whitespace; one argument to print()
  # >>> print("This will not work because price is not a string:" + item)
    # TypeError: can only concatenate str (not "int") to str
  print("Product name is",item,"and its price is",price) #printing multiple 'items' - multiple arguments; inserts whitespaces - notice the lack of whitespaces after first part and before last part, in the quotes
  print("Product name is {} and its price is {}".format(item, price))
  print(f"Product name is {item} and its price is  {price}")


  for i in range(10):
    print("no newline,i=",i,">>", end='') #no newline!
  print()
  
  for i in range(10):
    print("no newline and no whitespaces inserted,i=",i,">>", sep='', end='') #no newline and no whitespaces inserted
  print()
  
  for i in range(10):
    print("with newline,i=",i,">>") #with newline!
  print('\n\n')

  print("Well would you look at that syntax:", "-separator-".join(["ab","cd","gg","hy"]))

  list=[]
  for i in range(10):
    list.append(str(i))
  print("list:",list)
  print("Well look at that syntax, again!:", "-separator-".join(list)) # list items must be strings

# ----------------------------------------------------------------
# abandoned
def a2_1():
  def print_my_way(method, object): # so I dont have to type twice name and method call 
      print(object+'.'+method.__name__+'():'+method(object))

  somestring = "Chickens have nice feathers."
  print("somestring:",somestring)

  print_my_way(str.upper, somestring) # somestring.upper()
# ----------------------------------------------------------------
def a2_2():
  somestring = "Chickens have nice feathers."
  print(f"somestring: {somestring} \n----")

  print(
     "somestring.upper():",somestring.upper(),'\n'
     "somestring.lower():",somestring.lower(),'\n'
     "somestring.isupper():",somestring.isupper(),'\n'
     "somestring.upper().isupper():",somestring.upper().isupper(),'\n'     
     "len(somestring):",len(somestring),'\n'
     "somestring[5]:",somestring[5],'\n'
     "somestring[5:7]:",somestring[5:7],'\n'
     "somestring.index(\"h\"):",somestring.index("h"),'\n'
     "somestring.index(\"C\"):",somestring.index("C"),'\n'
     "somestring.index(\"c\"):",somestring.index("c"),'\n'
     "somestring.index(\"ave\"):",somestring.index("ave"),'\n'
     "somestring.index(\"ve ni\"):",somestring.index("ve ni"),'\n'
     "somestring.replace(\"a\",\"E\"):",somestring.replace("a","E"),'\n'
     
     )
  
  # print(somestring.index("blu")) won't work, because there is no such string part
# ----------------------------------------------------------------
def b():
  list = [1,2,3]
  list2 = [4,5,6]

  listoflists = [list, list2]
  
  print("list:", list)
  print("list2:", list2)
  print("listoflists [list, list2]:", listoflists)
  print("len(listoflists):", len(listoflists))

# ----------------------------------------------------------------
def b_2():
  #tuples
  tuple = (2,6);
  tuple2 = (2.5, 6.4)
  something = (1,2,3,4,5,6,7,8,9)

  print("tuple:",tuple)
  print("tuple2:",tuple2)
  print("something",something)

  print("something[4]:", something[4])
  #something[4]=2 immutable

  list_of_tuples = [(1,2), (2,5,3), (3,1)]
  print("list_of_tuples:",list_of_tuples)

# ----------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np

def c():
  x = np.linspace(0, 20, 100)  # Create a list of evenly-spaced numbers over the range
  plt.plot(x, np.sin(x))       # Plot the sine of each x point
  plt.show()                   # Display the plot
# ----------------------------------------------------------------
def d():
  print(5)
  print(5*3)
  number1 = -4
  print("number1:",number1)
  print(
    "abs(number1):",abs(number1),'\n'
    "pow(number1, 3):",pow(number1, 3),'\n'
    "max(number1, pow(number1,3)):",max(number1, pow(number1,3))
  )
  print(
    "round(3.7):",round(3.7),'\n'
    "round(3.2):",round(3.2)
  )  
  
  from math import floor, ceil, sqrt
  print(
    "floor(3.7):",floor(3.7),'\n'
    "floor(3.2):",floor(3.2),'\n'
    "ceil(3.7):",ceil(3.7),'\n'
    "ceil(3.2):",ceil(3.2),'\n'
    "sqrt(81):",sqrt(81)
  )
  # TO DO difference between math that does not need importing, the one that does need, and the numpy (e.g. np.abs and abs - are there any differences in another methods?)

# ----------------------------------------------------------------
def e():
  number1 = input("Enter number1: ")
  number2 = input("Enter number2: ")

  print("number1 + number2 - string concat!:", number1 + number2)
  #this breaks if floats are used
  try:
    print("int(number1)+int(number2):", int(number1)+int(number2))
    print("int(number1+number2):", int(number1+number2))
  except ValueError:
    print("Cannot cast to int, omitting two print statements")
  
  #this works with floats
  print("float(number1)+float(number2)",float(number1)+float(number2))
  try:
    print("float(number1+number2)",float(number1+number2))
  except ValueError:
    print(f"Cannot sensibly cast that string ({number1+number2}) to float")

# ----------------------------------------------------------------
def f():
  colours = ["white", "Yellow", "green", "some colour", "red-and-" "green-ish", 
                  "red", "greenish"]

  print("colours:",colours)
  print("colours[0]:",colours[0])
  print("colours[1]:",colours[1])
  print("colours[-0]:",colours[-0])
  print("colours[-1]:",colours[-1])
  print("colours[1:]:",colours[1:])
  print("colours[1:4]:",colours[1:4])
  colours[1] = "blAAck"
  print("now colours[1]=blAAck")
  print("colours[1:4]:",colours[1:4])
  print("colours:",colours)
  print("colours[-1:-3]:",colours[-1:-3])
  print("colours[-3:-1]:",colours[-3:-1])
  print("colours[3:1]:",colours[3:1])
  print("colours[-4:5]:",colours[-4:5])

# ----------------------------------------------------------------
def g():
  colours = ["white", "blAAck", "green", "some colour", "red-and-" "green-ish", 
                  "red", "greenish"] # from previos
  dogs = ["beagle", "dog", "sznauzer"]

  print("colours", colours)
  print("dogs", dogs)

  dogs.extend(colours)
  print("dogs after dogs.extend(colours):",dogs)

  colours.extend(colours)
  print("colour after colours.extend(colours):", colours)

  dogs.append("pointer") #yes, that's a breed, and wonderful one!
  print("dogs after dogs.append('pointer')",dogs)

  dogs.insert(0,"abcdedler")
  print("dogs after dogs.insert(0,'abcdedler')",dogs)

  dogs.remove("white")
  print('dogs after dogs.remove("white")',dogs)

  print('colours:',colours)
  colours.pop()
  print('colours after colours.pop():', colours)

  print('colours.index("green"):',colours.index("green"))
  print('colours.count("badcolor"):', colours.count("badcolor"))
  print('colours.count("greenybadcolor"):',colours.count("greenybadcolor"))

  colours.sort()
  print("colours after colours.sort()", colours)

  colours.reverse()
  print("colours after colours.reverse()", colours)

  print("dogs:",dogs)
  dogs.clear()
  print("dogs, after dogs.clear():",dogs)

# ----------------------------------------------------------------
def h():
  numbers = [1,5,6,4,234,6,8,-4,      10-10]
  print("numbers",numbers)
  numbers.sort()
  print("number after .sort()",numbers)

  numbers2 = numbers
  numbers_copy = numbers.copy()
  print("numbers2 which is numbers2=numbers:",numbers2)
  print("numbers_copy which is numbers_copy = numbers.copy():", numbers_copy)
  del numbers[1:3]
  print("numbers after del numbers[1:3]:", numbers)
  print("numbers2 after previous del numbers[1:3]:",numbers2)
  print("numbers_copy after previous del numbers[1:3]", numbers_copy)

# ----------------------------------------------------------------
def i():
  def say_hello(greeting = "Hello", name = "John"):
      print(greeting + " " + name)
      return True
      print("this is not processed")

  say_hello_var = say_hello()
  print("say_hello_var:",say_hello_var)
  print('say_hello("good morning","Caroline"), function here:',say_hello("good morning","Caroline"))
  
  print('say_hello("good morning","Caroline"):')
  say_hello("good morning","Caroline")
  
  print('say_hello("howdy"):')
  say_hello("howdy")

  print('say_hello(name = "Michael"):')
  say_hello(name = "Michael")

  print("\n-------------\n")

  is_sad = True
  if is_sad and say_hello_var:
      print("ifs work")
  elif not is_sad and not say_hello_var:
      print ("ifs keep working")
  else: 
      print("something is wrong")


# ----------------------------------------------------------------
def j():
  #dictionary
  license_for = {
      "weapon": True,
      "life": 75,
      "three_dogs": [True, True, False],
      100: "100 not allowed (whatever meaning that should convey)"
  }

  print("license_for:",license_for)
  print('license_for["weapon"]:',license_for["weapon"])
  print('license_for.get("weapon"):',license_for.get("weapon"))

  print('license_for.get("adsad"):',license_for.get("adsad"))
      #print(license_for["asdassad"]) this gives an error
  print('license_for.get("adsad", "what have you even written there!"):',license_for.get("adsad", "what have you even written there!"))
  print("license_for[100]:", license_for[100])

# ----------------------------------------------------------------
def k():
  i = 1
  while i<10:
      print(i)
      i+=1

  iteratee =""
  while iteratee != 'a':
      print("still in first while")
      iteratee = input("Input letter \"a\": ")
          # "iteratee" must be declared prior to use.
  print("left first while!")
  
  while input("Input letter \"b\": ") !='b':
      print("still in second while")
  print("left second while!")

# ----------------------------------------------------------------
def k_2():
  print('--- for letter in "Wow that is awesome":')
  for letter in "Wow that is awesome":
    print(letter)
  
  print('--- for letter in "Wow that is awesome", print end="":')
  for letter in "Wow that is awesome":
    print(letter, end="")

  print('--- for letter in "Wow that is awesome", print end="" sep="":')
  for letter in "Wow that is awesome":
    print(letter, end="",sep="")

# ----------------------------------------------------------------
def k_3():
  colours = ["white", "blAAck", "green", "some colour", "red-and-" "green-ish", 
                  "red", "greenish"] # from previos
  list_of_tuples = [(1,2), (2,5,3), (3,1)]

  print("--- for colour in colours")
  for colour in colours:
      print(colour)

  print("--- for i in range(len(colours)):")
  for i in range(len(colours)):
      print(colours[i])
      if i == 0: print("\tfirst time")
      else: print("\tnot first time")
  
  print("--- for i, colour in enumerate(colours)):")
  for i, colour in enumerate(colours):
      print(colour)
      if i == 0: print("\tfirst time")
      else: print("\tnot first time")

  print("--- for one_tuple in list_of_tuples:")
  for one_tuple in list_of_tuples:
      print(one_tuple)

# ----------------------------------------------------------------
def k_4():

  print("--- for i in range(10):")
  for i in range(10):
      print(i)

  print("--- for i in range(3, 10):")
  for i in range(3, 10):
      print(i)

  print("for i in range (0, 11, 3):")
  for i in range (0, 11, 3): # start,end,step-size. Returns 0 3 6 9
    print(i)
  
  print("for i in range (0, 12, 3):")
  for i in range (0, 12, 3): 
    print(i)

  print("for i in range (0, 13, 3):")
  for i in range (0, 13, 3): 
    print(i)

  print("for i in range(6)...else..")
  for i in range(6):
      print(i)
  else:
      print("finally finished")   #else in FOR! -after loop is finished. 
  
  print("for i in range(6)...break...else..")
  for i in range(6):
      print(i)
      if i ==3:
          break
  else:
      print("finally finished - 2") #will not execute due to 'break' above                                

  print("for i in range(12)...continue...break...else:")
  for i in range(12):
      if i == 5:
          continue #moves to next iteration
      if i == 8:
          break #leaves the loop
      print(i)
  else:
      ("I left the for--continue--break--else")
  print("Out of the loop")

# ----------------------------------------------------------------
def k_5():

  grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [0]
  ]

  print("grid:",grid)
  print("grid[0][0]:",grid[0][0])
  print("grid[1][2]:",grid[1][2])

  print("for row in grid print row")
  for row in grid: 
      print(row)

  print("for row in grid ->for col in row -> print row")
  for row in grid:
      for col in row:
          print(col)

# ----------------------------------------------------------------
def k_6():
  #writing this for the sake of picturing pythonese way of doing things
  def power(base, exponent):
      result = 1
      for i in range(exponent): #for i in exponent: 'int' object is not iterable
          result = result*base
      return result

  print("result does not matter, I Wrote that function for picturing pythonese way - power(2,3):",power(2,3))

  print("\n\n------------")

  # the below is from tutorial (stuff above maybe too, can't remember anymore), because it presents pythonese way of doing things
  #in C++ I'd probably just copy the string and check every index in it, and here python rewrites it. Basically the same, more or less
  def translator(text):
      translated =""
      for letter in text:
          if letter not in "AEOUIYaeouiy": # if ltr.lower not in "aeouiy" - more efficient?
              translated = translated + letter # concatenate what was parsed so far with the current letter
          else: translated = translated + "g" # concatenate what was parsed so far with letter 'g' instead of current letter
              #ok, in 'for x in something', it iterates over the 'indexes' and 'dereferences' the object in the index.
      return translated
  print(translator("No i co by pies na to powiedział"))

# ----------------------------------------------------------------
def l():
  try:
      number = int(input("1 Enter number: "))
      print(number)
  except: #this is too general, it catches anything
      print("1Some error") 

  try:
      number2 = int(input("2 Enter number: "))
      print(number2)
      print(number2/0)
  except ZeroDivisionError:
      print("2You tried to divide by zero")
  except ValueError: #should someone not enter integer, the program does not break thanks to error handling ("handling" in quotes here)
      print("2You entered invalid value")

  #different way for the same as above
  try:
      number3 = int(input("3Enter number, if 5 then I will try to divide by 0: "))
      print(number3)
      if number3 == 5:
        print(number3/0)
  except ZeroDivisionError as err:
      print(err)
  except ValueError as err:
      print(err)

  # I have something more in bookmarks; there is also 'finally' block which is always run (I assume)

# ----------------------------------------------------------------
from dog_class import Dog
from bigdog_class import BigDog

import constants

def m():

  number_three = constants.three
  print("three from 'constants' module is:", number_three)
  planck_constant = constants.planck_constant
  print("planck_constant from 'constants' module is:", planck_constant)

  print("----")
  dog1 = Dog("max", "terrier", 9, True)
  print("name: " + dog1.name + "\n" + "age: " + str(dog1.age) + "\n" + "breed: " + dog1.breed)
  if dog1.is_old():
      print("old dog")
  elif not dog1.is_old():
      print ("not an old dog")

  print("----")
  # dog2 = Dog(name="hockey", breed="pointer", age=3, asdasd=True) # will not work - and very well!
  dog2 = Dog(name="hockey", breed="pointer", age=3, is_vaccinated=True) 
  print("name: " + dog2.name + "\n" + "age: " + str(dog2.age) + "\n" + "breed: " + dog2.breed)
  if dog2.is_old():
      print("old dog")
  elif not dog2.is_old():
      print ("not an old dog")
  
  print("----")
  bigdog = BigDog("Pavel", "border collie", 9, True, 100)
  print("name: " + bigdog.name + "\n" + "age: " + str(bigdog.age) + "\n" + "breed: " + bigdog.breed)
  if bigdog.is_old():
      print("old dog")
  elif not bigdog.is_old():
      print ("not an old dog")
          #despite the same age, there is a different result, because the function is overloaded in the derived class 

# ----------------------------------------------------------------
# ----------------------------------------------------------------
code_fragments = {
    'a': a,
    'a2_1':a2_1,
    'a2_2':a2_2,
    'b': b,
    'b_2': b_2,
    'c': c,
    'd': d,
    'e': e,
    'f': f,
    'g': g,
    'h': h,
    'i': i,
    'j': j,
    'k': k,
    'k_2': k_2,
    'k_3': k_3,
    'k_4': k_4,
    'k_5': k_5,
    'k_6': k_6,
    'l': l,
    'm': m
  }
# ----------------------------------------------------------------
# Whenever adding new code above, you probably do not care about code below
import sys
def main():
  is_first_iteration = True
  prev_choice = 'does_not_exist' # magic number - flag
  while True:
    if len(sys.argv) > 1 and is_first_iteration:
      choice = sys.argv[1].strip().lower()
      is_first_iteration = False
    else:
      print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-')
      choice = input("Choose preferred code_fragment ('qwqw' to quit, 'agag' for previous choice): ").strip().lower()
      print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-')


    if choice == 'qwqw':
      break
    if choice == 'agag' and choice != 'does_not_exist': #previos choice does exist
      choice = prev_choice

    prev_choice = choice

    if choice in code_fragments:  
      code_fragments[choice]()
    else:
        print("Invalid choice.")
# ----------------------------------------------------------------
# ----------------------------------------------------------------
if __name__ == "__main__": 
  main()

# if script is run as main program, __name__ is assigned "__main__" (there are two underscores)
# should this script be imported by another script (e.g. "import scripto", when this file is "scripto.py" ), the __name__ in scripto.py will be "scripto"