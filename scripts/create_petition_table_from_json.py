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

class LongPetition(
    collections.namedtuple('LongPetition',
        'petition_idx status begin end category num_agree title content')):

    def __str__(self):
        return '\t'.join([str(v) for v in self])

def get_value(obj, key):
    value = obj[key]
    if isinstance(value, str):
        value = value.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ').strip()
    return value

def get_values(obj, keys):
    return tuple(get_value(obj, key) for key in keys)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_directory', type=str, default='../output/')
    parser.add_argument('--table_path', type=str, default='./petitions.tsv')
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--include_content', dest='long', action='store_true')

    args = parser.parse_args()
    json_directory = args.json_directory
    table_path = args.table_path
    debug = args.debug
    long = args.long

    keys_short = 'petition_idx status begin end category num_agree title'.split()
    keys_long = 'petition_idx status begin end category num_agree title content'.split()

    keys = keys_long if long else keys_short

    # get json paths
    json_paths = glob.glob('{}/*.json'.format(json_directory))
    if debug:
        json_paths = json_paths[:10]

    # append rows
    rows = []
    for path in json_paths:
        with open(path, encoding='utf-8') as f:
            json_obj = json.load(f)
        if long:
            petition = LongPetition(*get_values(json_obj, keys))
        else:
            petition = ShortPetition(*get_values(json_obj, keys))
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