import argparse
import json
import os
import time
import sys
sys.path.append('../')

from petitions_scraper import parse_page
from petitions_scraper import get_petition_links

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--index_filename', type=str,
                        default='../data/petition_links.csv')
    parser.add_argument('--output_directory', type=str,
                        default='../output/')
    parser.add_argument('--category_numbers', type=str, default='36',
                        help='_ separated category idx')
    parser.add_argument('--include_agree_phrase', dest='include_agree_phrase',
                        action='store_true')
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--sleep', type=float, default=1.0)

    with open('categories.json', encoding='utf-8') as f:
        category_dictionary = json.load(f)

    args = parser.parse_args()    
    index_filename = args.index_filename
    output_directory = args.output_directory
    remove_agree_phrase = not args.include_agree_phrase
    debug = args.debug
    sleep = args.sleep
    categories = args.category_numbers
    categories = categories.split('_')

    # check category idx
    for c in categories:
        if not c in category_dictionary:
            message = 'Check category id {}\n categories = {}'.format(
                c, category_dictionary)
            raise ValueError(message)

    # convert idx to name
    def convert(idx):
        return category_dictionary[idx]

    categories = {convert(idx) for idx in categories}
    print('Categories : {}'.format(categories))

    # load index file
    def match(c):
        return c in categories

    with open(index_filename, encoding='utf-8') as f:
        indices = [doc.strip().split('\t') for doc in f]
        indices = [index for index in indices if len(index) == 3]
        urls = [url for category, title, url in indices if match(category)]
    print('Num of urls = {}, indices = {}'.format(len(urls), len(indices)))

    # check path
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # scraping
    for i, url in enumerate(urls):

        # get a petition
        try:
            petition = parse_page(url, include_replies=True,
                remove_agree_phrase=remove_agree_phrase)
        except Exception as e:
            # ignore deleted page
            continue

        # save scraped result
        petition_idx = url.split('/')[-1]
        output_path = '%s/%s.json' % (output_directory, petition_idx)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(petition, f, indent=2, ensure_ascii=False)

        # check mode
        if debug and i > 10:
            break
        # verbose
        if i % 20 == 0:
            print('scrapping {} / {} petitions'.format(i+1, len(urls)))
            time.sleep(5)
        time.sleep(0.5)


if __name__ == '__main__':
    main()