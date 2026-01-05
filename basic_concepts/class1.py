# Simple function
def priceWithDiscount(value:float, discount: float):
    return value * (1 - discount)

result1 = priceWithDiscount(100, 0.2)

print(result1)

# String Formatting

def gratting(name: str):
    return f"Hello, {name}!"

print(gratting("John"))

# Format float values
pi = 3.14159265359
print(f"the value of PI rounded is: {pi:.2f}")

# Using format
template = "Hello, {}! You have {} years old!"
formatedByTemplate = template.format("Ralf", 10)
print(formatedByTemplate)

result = str.format(template, "Bob", 10)
print(result)

# Getting user input
# name = input("Enter you name: ")
# print(f"Thank you, {name}!")

# def inputAge():
#     return input("How old are you: ")

# age = inputAge()

# while not age.isnumeric():
#     print("You not send me a number, please enter you age again!")
#     age = inputAge()       

# print(f"Wow, you just have {int(age)} years!")

# List, tuples, sets

myList = ["You", "Me"]
myTuple = ("One", "Two", "Three") #ummuteble
mySet = {"One", "Two", "Three"} #without duplicated elements, no order

print(myList)
print(myTuple)
print(mySet)

print(myList[0])

#Set Operations 
setOfNumbers = {"One", "Two", "Three", "Four", "Five"}
pares = {"Two", "Four"}
impares = setOfNumbers.difference(pares)
print(impares)
print(len(impares))

#Compare with 'is'
name = "Steve"
print(name is "Steve")
print(name is not "John")

# Conditions
name = "Adam"

if name == "Adam":
    print("It's a boy!")
elif name == "June":
    print("it's a girl!")
else:
    print("IDK")    

friends = ["Lucas", "Ray", "Andre"]

if "Lucas" in friends:
    print("Lucas is in the list")

#Loops
friends = ["Lucas", "Ray", "Andre"]
while len(friends) > 0:
    removedElement = friends.pop(0)
    print(f"Remove {removedElement}")

print(friends)

# while True: 
#     response = input("Wanna play a game? (Y/n)")

#     if response == "n":
#         break
#     else:
#         print("Good Answer!")
friends = ["Lucas", "Ray", "Andre"]
for friend in friends:
    print(f"{friend} is my friend")

despesas = [1000, 30, 28.40, 600]
total = 0

for despesa in despesas:
    total += despesa

print(f"O total é {total}")

# ou
print(f"O total é {sum(despesas)}")

# List Comprehansions
friends = ["Lucas", "Ray", "Andre", "Andreia"]
starts_a = [n for n in friends if n.lower().startswith("a")]
print(starts_a)

# Dictionaries
# Can represent a map or an object
friends_ages = {
    "Ray": 32,
    "Andre": 30,
    "Andreia": 28
}

print(friends_ages["Ray"])
for name, age in friends_ages.items():
    print(f"{name} is my friend and have {age} years old!")    

if "Ray" in friends_ages:
    print(f"The age of Ray is: {friends_ages["Ray"]}")

friends = [
    {
        "name": "John",
        "age": 35
    },
    {
        "name": "Maria",
        "age": 30
    },
]

print(friends)
print(friends[0]["name"])

for f in friends:
    for k in f:
        print(f"{k} is {f[k]}")

for f in friends:
    for key, value in f.items():
        print(f"{key}, {value}") 
               
for f in friends:
    print(f"{f["name"]} is my friend and have {f["age"]} years old!")        

# Desconstructive variables
def getNameAndAgeOf(name:str, dict:{str, int}):
    if name in dict:
        return name, dict[name]

name, age = getNameAndAgeOf("Ray", friends_ages)
print(f"Name: {name}, Age: {age}")

person = ("Rafa", 30, "Dev")
name, age, profession = person

print(f"Name: {name}, Age:{age}, Proff:{profession}")
person = ("Ana", 35, "Manager")
name, _, profession = person
print(f"Name: {name}, Proff:{profession}")

person = (1, "Rafa", 30, "Dev")
id, *rest = person
print(id)
print(rest)

#Functions

def sayHello(name="The", surname="Machine"):
    print(f"Hello, {name} {surname}")

sayHello("John", "Smith")

# With Named arguments
sayHello(name="Rafael", surname="Tavares")

# Show default value
sayHello()

# Using Types to paramenter and return value
def add(a: int, b:int) -> int:
    return a + b

print(add("a", "b")) # Python not return error for this
print(add(1,2))

# Lambda - used only for small functions and chain calls
addLamb = lambda a, b: a + b
print(addLamb(1,2))

print((lambda a, b: a + b)(1,2))

numbers = [1, 2, 3, 4]  
doubled = map((lambda x: x*2), numbers)
print(list(doubled))

# Dictionary Comprehansions

users = [
    (1, "Rafa", "password"),
    (2, "Ana", "123456")
]

username_mapping = {user[1]: user for user in users} # Using the name as key of a new map
id, username, password = username_mapping["Rafa"]
print(username_mapping)
print(f"{id} - {username} - {password}")

# Functions with many arguments
def multipy(*args):  #args are a tuple
    total = 1
    for arn in args:
        total = total * arn
    return total


print(multipy(1,2,3))    

def named(**kwargs): # kwargs are a dictionary
    print(kwargs)

named(name="Rafael", surname="Tavares")

def print_nicely(**kwargs):
    named(**kwargs)
    for arg, value in kwargs.items():
        print(f"{arg}: {value}")


print_nicely(name="Rafa", age=30)

