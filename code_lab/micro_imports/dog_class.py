class Dog:
    def __init__(self, name, breed, age, is_vaccinated):
        self.name = name # we assing what is in 'constructor' to particular instance ('self')
        self.breed = breed
        self.age = age
        self.is_vaccinated = is_vaccinated
    
    def is_old(self):
        if self.age > 10: 
            return True
        else: 
            return False