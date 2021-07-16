import argparse
import csv
import json
import sys

def parse(dove_file):
    towers = []
    reader = csv.DictReader(dove_file)
    for tower in reader:
        # There isn't really a satisfactory tower name in the Dove data
        tower_name = tower['PlaceCL'] or tower['Place']

        # Skip Carillons
        if tower['RingType'] != "Full circle ring":
            print("Carillon: " + tower_name, file=sys.stderr)
            continue

        # Skip unassigned or temporary TowerBase IDs
        tower_base = int(tower['TowerBase'])
        if tower_base == 0 or tower_base >= 9000:
            print("Temporary TowerBase: " + tower_name, file=sys.stderr)
            continue

        # Skip mobile rings
        try:
            latitude = float(tower['Lat'])
            longitude = float(tower['Long'])
        except ValueError:
            print("Mobile ring: " + tower_name, file=sys.stderr)
            continue

        # Use country where county isn't specified
        county = tower['County'] or tower['Country']

        towers.append({
                'id': tower_base,
                'name': tower_name,
                'dedication': tower['Dedicn'],
                'county': county,
                'latitude': latitude,
                'longitude': longitude,
                'bells': int(tower['Bells']),
                'weight': int(tower['Wt']),
                'unringable': tower['UR'] != "",
                'practice':  tower['Practice']
                })

    return towers

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dove_file', type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="Input CSV file (default stdin)")
    parser.add_argument('json_file', type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="Output CSV file (default stdout)")
    args = parser.parse_args()

    towers = parse(args.dove_file)
    json.dump(towers, args.json_file, indent=2)
