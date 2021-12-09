from freecodecamp_learnpython1i_class import Pies

#to jest b. kiepski projekt abstrakcji, ale dla samego dowodu zostawiam
class DuzyPies(Pies):
    def __init__(self, imie, rasa,wiek, jest_szczepiony, rozmiar):
        Pies.__init__(self,imie,rasa,wiek,jest_szczepiony)
        self.rozmiar = rozmiar

    def czy_stary(self):
        if self.wiek > 8: 
            return True
        else: 
            return False
