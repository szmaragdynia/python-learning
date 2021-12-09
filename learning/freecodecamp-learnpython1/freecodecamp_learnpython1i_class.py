class Pies:
    def __init__(self, imie, rasa, wiek, jest_szczepiony):
        self.imie = imie #konkretnemu obiektowi przypiszemy to co w "konstruktorze"
        self.rasa = rasa
        self.wiek = wiek
        self.jest_szczepiony = jest_szczepiony
    
    def czy_stary(self):
        if self.wiek > 10: 
            return True
        else: 
            return False

class QA:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
