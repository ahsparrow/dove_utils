import argparse
import csv
import sys

def translate_keys(dove_file, asset_file):
    # Read asset file and get map of tower id to Dove id
    reader = csv.DictReader(asset_file, delimiter="\\")
    dove_ids = {int(x['TowerID']):x['DoveID'] for x in reader}

    # Read Dove file and get map of Dove id to TowerBase
    reader = csv.DictReader(dove_file, delimiter="\\")
    tb_ids = {x['DoveID']:int(x['TowerBase']) for x in reader}

    # Make sure tower_ids have no gaps
    tower_ids = sorted(dove_ids.keys())
    if (len(tower_ids) != tower_ids[-1]):
        print("WARNING: Missing tower(s)", file=sys.stderr)

    for id in tower_ids:
        print(tb_ids[dove_ids[id]], end=" ")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('asset_file', type=argparse.FileType('r'),
                        default=sys.stdout)
    parser.add_argument('dove_file', type=argparse.FileType('r'),
                        default=sys.stdin)
    args = parser.parse_args()

    translate_keys(args.dove_file, args.asset_file)
