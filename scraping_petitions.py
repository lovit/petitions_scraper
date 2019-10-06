import argparse
import json
import os
import time
from glob import glob
from petitions_scraper import parse_page


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, default='output', help='JSON storage directory')
    parser.add_argument('--first_index', type=int, default=539390, help='First index of petition')
    parser.add_argument('--last_index', type=int, default=582491, help='Last (latest) index of petition')
    parser.add_argument('--index_file', type=str, default='index.txt', help='Index of petitions to be scraped')
    parser.add_argument('--sleep', type=float, default=1, help='Sleep time for each petitions')
    parser.add_argument('--repeats', type=int, default=10, help='Number of repeating')
    parser.add_argument('--verbose', dest='verbose', action='store_true')
    parser.add_argument('--show_last_index', dest='show_last_index', action='store_true')
    parser.add_argument('--show_result', dest='show_result', action='store_true')

    args = parser.parse_args()
    directory = args.directory
    first_index = args.first_index
    last_index = args.last_index
    index_file = args.index_file
    sleep = args.sleep
    repeats = args.repeats
    verbose = args.verbose
    show_last_index = args.show_last_index
    show_result = args.show_result

    # Initialize directory
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Initialize index file
    if not os.path.exists(index_file):
        save_index(index_file, [])

    # Only show last index
    if show_last_index:
        return show_last_index_func(directory)

    # Check index list
    faileds, successeds = load_index(index_file)
    if (not faileds and not successeds):
        faileds = update_target(first_index, last_index)
        save_index(index_file, faileds)

    # Only show scraping result
    if show_result:
        print('num of successed = {}'.format(len(successeds)))
        print('num of faileds = {}'.format(len(faileds)))
        return None

    ### main process ###
    # Repeating
    for num_tries in range(1, repeats + 1):

        # reload index
        faileds, successeds = load_index(index_file)
        faileds = dict(faileds)

        # scraping
        num_successeds = 0
        num_faileds = len(faileds)
        for i, (idx, status) in enumerate(sorted(faileds.items())):
            url = 'https://www1.president.go.kr/petitions/{}'.format(idx)
            try:
                petition = parse_page(url)
                if petition == -1: # 비공개청원
                    faileds[idx] = -1
                    continue
                filepath = '{}/{}.json'.format(directory, idx)
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(petition, f, ensure_ascii=False, indent=2)
                args = (idx, i, num_faileds, num_tries, repeats)
                print('Successed to scrap petition = {} ({} / {}), {} / {} tries'.format(*args))
                faileds[idx] = 1
                num_successeds += 1
            except Exception as e:
                args = (idx, i, num_faileds, num_tries, repeats)
                print('Failed to scrap petition = {} ({} / {}), {} / {} tries'.format(*args))
            time.sleep(sleep)

        # save index
        faileds = list(sorted(faileds.items()))
        index = faileds + successeds
        save_index(index_file, index)

        # check improvement
        if num_successeds == 0:
            print('Stop scraping because there is no more improvement. {} / {} tries'.format(num_tries, repeats))
            break

        args = (num_tries, repeats, num_successeds, len(faileds))
        print('num tries = {} / {}, num successeds = {} / {}'.format(*args))

def show_last_index_func(directory):
    paths = glob('{}/*.json'.format(directory))
    paths = sorted(paths, key=lambda x:-int(x.split('/')[-1][:-5]))
    last_index = -1
    for path in paths:
        with open(path, encoding='utf-8') as f:
            petition = json.load(f)
        petition_idx = petition['petition_idx']
        status = petition['status']
        if status == '청원종료':
            last_index = max(last_index, int(petition_idx))
    print("Last index is {}".format(last_index))
    return None

def update_target(first_index, last_index):
    if (first_index == -1) or (last_index == -1):
        raise ValueError('Prepare index file or set first & last index')
    faileds = [(idx, 0) for idx in range(first_index, last_index+1)]
    return faileds

def load_index(path):
    """
    status 0 means that this petition has been not yet scraped or failed
    status 1 means that this petition already scraped successfully.
    """
    def parse_status(row):
        values = row.split()
        if len(values) == 1:
            return (int(values[0]), 0)
        else:
            return (int(values[0]), int(values[1]))

    with open(path, encoding='utf-8') as f:
        next(f) # skip head
        index = [parse_status(row) for row in f]

    faileds = [row for row in index if row[1] == 0]
    successeds = [row for row in index if (row[1] == 1 or row[1] == -1)]
    return faileds, successeds

def save_index(path, index):
    index = sorted(index)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('index status\n') # write head
        for idx, status in index:
            f.write('{} {}\n'.format(idx, status))

if __name__ == '__main__':
    main()