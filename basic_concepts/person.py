class Person:
    name: str
    age: int
    gender: str
    GENDER_TYPE = ("Male", "Female")

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}, Gender: {self.gender}"

    def show(self):
        print(f"Hello {self.name}")

    # Used to crate factories cls == Person
    @classmethod
    def man(cls, name, age):
        return cls(name, age, cls.GENDER_TYPE[0])    
    
    @classmethod
    def woman(cls, name, age):
        return cls(name, age, cls.GENDER_TYPE[1])

    @staticmethod
    def static_method_ex():
        print("This is a static method example")        


# Calling
person = Person("John", 30, "Unicorn")
person.show()
person.name = "Ralf"
person.show()

print(person)
print(person.__dict__)

Person.static_method_ex()
print(Person.GENDER_TYPE)

print(Person.man("Rafa", 32))
print(Person.woman("Isa", 32))