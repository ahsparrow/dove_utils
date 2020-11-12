import argparse
import csv
import sys

def new_asset(dove_file, newpks_file, old_asset_file, new_asset_file):
    # Read Tower IDs from old asset file
    reader = csv.DictReader(old_asset_file, delimiter="\\")

    tower_ids = {x['DoveID']:int(x['TowerID']) for x in reader}
    next_tower_id = max(tower_ids.values()) + 1

    # Read list of changed primary keys
    reader = csv.reader(newpks_file, delimiter="\\")
    pks = {new: old for (old, new) in reader}

    # Read Dove file
    reader = csv.DictReader(dove_file, delimiter="\\")
    dove = list(reader)

    # Add tower IDs
    for d in dove:
        if d['DoveID'] in tower_ids:
            # All good - we have a tower id for this one
            d['TowerID'] = tower_ids[d['DoveID']]
        else:
            # Has the dove id changed?
            dove_id = d['DoveID']
            if dove_id in pks:
                # Dove id has changed, get tower_id using previous id
                if pks[dove_id] in tower_ids:
                    print("DoveID change %s -> %s" % (dove_id, pks[dove_id]))
                    d['TowerID'] = tower_ids[pks[dove_id]]
                else:
                    print("WARN - Can't find tower id for changed dove id %s" % dove_id)
                    d['TowerID'] = next_tower_id
                    next_tower_id += 1
            else:
                print("New tower %s", dove_id)
                d['TowerID'] = next_tower_id
                next_tower_id += 1

    fields = ['TowerID',
              'DoveID',
              'County',
              'Place',
              'Place2',
              'Dedicn',
              'Bells',
              'Wt',
              'UR',
              'PracN',
              'PrXF',
              'Lat',
              'Long']

    # Write new asset file
    writer = csv.DictWriter(new_asset_file, fields,
                            delimiter="\\", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(dove)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dove_file', type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('newpks_file', type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('old_asset_file', type=argparse.FileType('r'),
                        default=sys.stdout)
    parser.add_argument('new_asset_file', type=argparse.FileType('w'),
                        default=sys.stdout)
    args = parser.parse_args()

    new_asset(args.dove_file, args.newpks_file, args.old_asset_file, args.new_asset_file)
