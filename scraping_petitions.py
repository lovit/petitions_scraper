import argparse
import json
import os
import time
from glob import glob
from petitions_scraper import parse_page
from petitions_scraper import yield_petition_links

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, default='output', help='JSON storage directory')
    parser.add_argument('--begin_page', type=int, default=1, help='First page number')
    parser.add_argument('--end_page', type=int, default=10, help='Last page number')
    parser.add_argument('--sleep', type=float, default=1, help='Sleep time for each petitions')
    parser.add_argument('--verbose', dest='verbose', action='store_true')
    parser.add_argument('--force-all', dest='force', action='store_true')

    args = parser.parse_args()
    directory = args.directory
    begin_page = args.begin_page
    end_page = args.end_page
    sleep = args.sleep
    verbose = args.verbose
    force = args.force

    if not os.path.exists(directory):
        os.makedirs(directory)

    # check last index
    if force:
        last_index = 1
    else:
        paths = glob('{}/*.json'.format(directory))
        paths = sorted(paths, key=lambda x:-int(x.split('/')[-1][:-5]))
        last_index = find_last_index(paths)
        if last_index is None:
            last_index = 1

    # verbose print
    if verbose:
        print('Last (oldest index) = {}\n'.format(last_index))

    for category, title, url in yield_petition_links(begin_page, end_page, sleep, verbose=False):
        try:
            # check index
            index = int(url.split('/')[-1])
            if index < last_index:
                break

            # get petition
            petition = parse_page(url, include_replies=False, remove_agree_phrase=False)

            # save
            path = '{}/{}.json'.format(directory, index)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(petition, f, indent=2, ensure_ascii=False)

            # verbose print
            if verbose:
                print('scraped {} (~ {})'.format(index, last_index))

            # sleep
            time.sleep(sleep)

        except Exception as e:
            print(e)
            print('Unexpected exception occurred. Sleep 10 minutes ... ')
            time.sleep(600)

def read_file(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def find_last_index(paths):
    """
    Arguments
    ---------
    :param paths: list of path
        Index sorted in decreasing order

    Returns
    -------
    petition_idx
    """

    for path in paths:
        petition = read_file(path)
        petition_idx = petition['petition_idx']
        status = petition['status']
        if status == '청원종료':
            return int(petition_idx)
    return None

if __name__ == '__main__':
    main()