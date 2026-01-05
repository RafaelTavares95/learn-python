class Auto:
    type: str
    label: str

    def __init__(self, type, label):
        self.type = type
        self.label = label

    def make_noise(self):
        print("Rum Rum")

class Car(Auto):
    is_eletric: bool
    def __init__(self, type, label, is_eletric):
        super().__init__(type, label)    
        self.is_eletric = is_eletric

    def make_noise(self):
        if self.is_eletric:
            print("Eletric cars dont make noise")
        else:    
            super().make_noise()    


auto = Auto("road", "honda")
auto.make_noise()

car = Car("city", "toyota", False)
car.make_noise()

car2 = Car("city", "toyota", True)
car2.make_noise()