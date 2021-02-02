class Flight():
    def __init__(self, capacity):
        self.capacity = capacity
        self.passangers = []

    def add_passanger(self, name):
        if not self.open_seats():
            return False
        self.passangers.append(name)
        return True

    def open_seats(self):
        return self.capacity - len(self.passangers)

flight = Flight(3)

people = ["Harry","ron","gimmy","kualalumpur"]

for person in people:
    if flight.add_passanger(person):
        print(f"{person} is added")
    else:
        print(f"for {person} there was no seats")