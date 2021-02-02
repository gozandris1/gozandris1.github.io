people = [
    {"name": "harry", "house": "shit"},
    {"name": "vmi", "house":"fantas"},
    {"name":"slsals","house":"cola"}
]

people.sort(key=lambda person: person["name"])

print(people)