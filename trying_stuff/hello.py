# Here are all the things that I checked to get a grasp of python workings

# Function names are the way they are, because they are irrelevant, functions' only purpose is to enable me to run only the thing I am interested in right now (because that file contains many different things)
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