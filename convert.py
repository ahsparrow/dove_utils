import argparse
import csv
import json
import sys

def parse(dove_file):
    towers = []
    reader = csv.DictReader(dove_file)
    for tower in reader:
        # There isn't really a satisfactory tower name in the Dove data
        place = tower['PlaceCL'] or tower['Place']

        # Skip Carillons
        if tower['RingType'] != "Full-circle ring":
            print("Carillon: " + place, file=sys.stderr)
            continue

        # Skip unassigned or temporary TowerBase IDs
        tower_base = int(tower['TowerBase'])
        if tower_base == 0 or tower_base >= 9000:
            print("Temporary TowerBase: " + place, file=sys.stderr)
            continue

        # Skip mobile rings
        try:
            latitude = float(tower['Lat'])
            longitude = float(tower['Long'])
        except ValueError:
            print("Mobile ring: " + place, file=sys.stderr)
            continue

        # Use country where county isn't specified
        county = tower['County'] or tower['Country']

        towers.append({
                'towerId': tower_base,
                'place': place,
                'dedication': tower['Dedicn'],
                'county': county,
                'iso3166': tower['ISO3166code'],
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
    parser.add_argument('output_file', type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="Output file (default stdout)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--json', action='store_true', help='JSON output')
    group.add_argument('--csv', action='store_true', help='CSV output')
    args = parser.parse_args()

    towers = parse(args.dove_file)

    if args.json:
        json.dump(towers, args.output_file, indent=2)
    else:
        # Specify field names to get consistent order
        fieldnames = [
                'towerId',
                'place',
                'dedication',
                'county',
                'iso3166',
                'latitude',
                'longitude',
                'bells',
                'weight',
                'unringable',
                'practice'
                ]
        writer = csv.DictWriter(args.output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(towers)
