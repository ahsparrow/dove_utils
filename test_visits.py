import csv
import random

reader = csv.DictReader(open("dove.txt"), delimiter="\\")
ids = [d['DoveID'] for d in reader]

visits = []
for i in range(100):
    visits.append({
        'DoveId': random.choice(ids),
        'Date': "2020-7-27",
        'Notes': " ".join(random.choices(["bell", "peal", "bob doubles", "wonky"], k=5)),
        'Peal' : random.choice("YN"),
        'Quarter': random.choice("YN")})

writer = csv.DictWriter(open("visits.csv", "w"), ['DoveId', 'Date', 'Notes', 'Peal', 'Quarter'])
writer.writeheader()
writer.writerows(visits)

