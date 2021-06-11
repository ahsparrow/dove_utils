import argparse
import csv
import sys

def new_asset(dove_file, asset_file):
    # Read Dove file, ignoring towers with temporary TowerBase and carillons
    reader = csv.DictReader(dove_file, delimiter="\\")
    dove = [x for x in reader if
            int(x['TowerBase']) < 9000 and int(x['Bells']) <= 16]

    fields = ['TowerBase',
              'County',
              'Place',
              'PlaceCL',
              'Dedicn',
              'Bells',
              'Wt',
              'UR',
              'PracN',
              'PrXF',
              'Lat',
              'Long']

    # Write new asset file
    writer = csv.DictWriter(asset_file, fields,
                            delimiter="\\", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(dove)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dove_file', type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('asset_file', type=argparse.FileType('w'),
                        default=sys.stdout)
    args = parser.parse_args()

    new_asset(args.dove_file, args.asset_file)
