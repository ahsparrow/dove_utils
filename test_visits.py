import argparse
import csv
import datetime
import random
import sys

import lorem

def make_visits(dove_file, out_file, num_visits):
    reader = csv.DictReader(dove_file, delimiter="\\")
    ids = [d['TowerBase'] for d in reader]

    visits = []
    for i in range(num_visits):
        dt = datetime.date.today() - \
                datetime.timedelta(days=random.randint(0, 3650))
        pq = random.choice("PQN")

        visits.append({
            'TowerBase': random.choice(ids),
            'Date': dt.isoformat(),
            'Notes': lorem.get_sentence(word_range=(1, 5)),
            'Peal' : "Y" if pq == "P" else "N",
            'Quarter': "Y" if pq == "Q" else "N"
        })

    writer = csv.DictWriter(
            out_file, ['TowerBase', 'Date', 'Notes', 'Peal', 'Quarter'])
    writer.writeheader()
    writer.writerows(visits)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--visits", "-v", type=int, default=10,
                        help="Number of visits")
    parser.add_argument('dove_file', type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('out_file', type=argparse.FileType('w'),
                        default=sys.stdout)
    args = parser.parse_args()

    make_visits(args.dove_file, args.out_file, args.visits)

