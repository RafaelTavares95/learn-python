class NoTwelveError(ValueError):
    pass

def divide(dividend: int, divisor: int):
    if dividend == 12:
        raise NoTwelveError("We dont like twelve, try another number!")
    if divisor == 0:
        raise ZeroDivisionError("The divisor cannot be Zero!")
    return dividend/divisor

try:
    print(divide(1, 0))
except ZeroDivisionError as err: 
    print(err.args[0])

try:
    print(divide(12, 2)) 
except NoTwelveError as err:
    print(err.args[0])       

#We can pass a function as parameter

def calculate(*values, operation):
    return operation(*values)

print(calculate(4,2, operation=divide))