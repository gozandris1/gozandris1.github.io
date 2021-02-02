import sys
try:
    x = int(input("x: "))
    y = int(input("y: "))
except ValueError:
    print("invalid input")
    sys.exit(1)

try:
    result = x / y 
except ZeroDivisionError:
    print("Error: 0val osztani nem lehet")
    sys.exit(1)


print(f"{x} per {y} is {result}")