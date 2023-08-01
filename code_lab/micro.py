# This script contains very small pieces of code that I wanted to try out. Some of them are extremely trivial, however I let them reside here anyway. 

# Function names are so simple and no information-bearing, because they are irrelevant - functions' sole purpose is to enable me to run only the part of the code I am interested in right now.
  # I used to have separate files for learning, checking how things work etc., but that was too messy, and not really convenient whenever I wanted to recall something

# --------------------------------------------------------------------------------------------------------------------------------
def a():
  msg = "Hello World"
  print(msg)
# ----------------------------------------------------------------
def b():
  lista = [1,2,3]
  lista2 = [4,5,6]

  listalist = [lista, lista2]

  print(listalist)
  print(len(listalist))



# ----------------------------------------------------------------
# ----------------------------------------------------------------
code_fragments = {
    'a': a,
    'b': b,
  }
# ----------------------------------------------------------------
# Whenever adding new code above, you probably do not care about code below
def main():
  while True:
    choice = input("Choose preferred code_fragment ('quit' to quit): ").strip().lower()

    if choice == 'quit':
        break
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