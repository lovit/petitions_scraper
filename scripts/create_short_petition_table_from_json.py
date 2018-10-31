import argparse
import collections
import glob
import os
import json


class ShortPetition(
    collections.namedtuple('ShortPetition',
        'petition_idx status begin end category num_agree title')):

    def __str__(self):
        strf = '\t'.join([str(v) for v in self])
        if len(strf.split('\t')) != 7:
            return '\t'*6
        return strf

def get_value(obj, key):
    value = obj[key]
    if isinstance(value, str):
        value = value.replace('\t', ' ').strip()
    return value

def get_values(obj, keys):
    return tuple(get_value(obj, key) for key in keys)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_directory', type=str, default='../output/')
    parser.add_argument('--table_path', type=str, default='./petitions.tsv')
    parser.add_argument('--debug', dest='debug', action='store_true')

    args = parser.parse_args()
    json_directory = args.json_directory
    table_path = args.table_path
    debug = args.debug

    keys = 'petition_idx status begin end category num_agree title'.split()

    # get json paths
    json_paths = glob.glob('{}/*.json'.format(json_directory))
    if debug:
        json_paths = json_paths[:10]

    # append rows
    rows = []
    for path in json_paths:
        with open(path, encoding='utf-8') as f:
            json_obj = json.load(f)
        petition = ShortPetition(*get_values(json_obj, keys))
        if not petition[0].strip() or not petition[1].strip():
            continue
        rows.append(petition)
    rows = sorted(rows, key=lambda x:int(x.petition_idx))

    # save as table
    dirname = os.path.dirname(os.path.abspath(table_path))
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(table_path, 'w', encoding='utf-8') as f:
        f.write('\t'.join(keys)+'\n')
        for row in rows:
            f.write('{}\n'.format(row))


if __name__ == '__main__':
    main()