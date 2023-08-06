from dog_class import Dog

#this is very bad use of an abstraction and classes, but I leave this for the sake of seeing how importing etc works (it works with no surprise)
class BigDog(Dog):
    def __init__(self, name, breed, age, is_vaccinated, size):
        Dog.__init__(self, name, breed, age, is_vaccinated)
        self.size = size

    def is_old(self):
        if self.age > 8: 
            return True
        else: 
            return False
