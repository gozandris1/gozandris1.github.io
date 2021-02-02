class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(input("x: "),input("y: "))
print(p.x, p.y)