import time
from .config import SLEEP
from .config import VERBOSE
from .utils import get_soup

def parse_link(li):
    category = li.select('div[class^=bl_category]')[0].text[2:].strip() # remove '분류'
    title = li.select('a')[0].text[2:].strip() # remove '제목'
    href = li.select('a')[0]['href']
    url = href.split('?')[0]
    return (category, title, url)

def yield_petition_links(begin_page=1, end_page=10):
    for p in range(begin_page, end_page + 1):
        url = 'https://www1.president.go.kr/petitions?page={}'.format(p)
        try:
            soup = get_soup(url)
        except:
            print('\nException while getting soup page=%d' % p)
            continue

        try:
            div = soup.select('div[class^=board]')[1]
            lis = div.select('div[class^=b_list] div[class=bl_body] li')
            for li in lis:
                try:
                    link = parse_link(li)
                    yield link
                except:
                    continue
        except Exception as e:
            print('Exception while parsing link')
            print(e)
            continue

        if p % 50 == 0:
            time.sleep(SLEEP)
        time.sleep(0.8) # default sleep

        if VERBOSE:
            print('\rget petitions links from {} in ({} - {}) pages'.format(
                p, begin_page, end_page), end='')
            if p % 100 == 0:
                print()


def get_petition_links(begin_page=1, end_page=10):
    links = [link for link in yield_petition_links(begin_page, end_page)]
    print('\ngetting petition links was done')
    return links