import time
from .config import SLEEP
from .config import VERBOSE
from .utils import get_soup

def get_petition_links(begin_page=1, end_page=10):

    def parse_link(li):
        category = li.select('div[class^=bl_category]')[0].text[2:].strip() # remove '분류'
        petition_num = int(li.select('div[class=bl_no]')[0].text[2:].strip()) # remove '번호'
        title = li.select('a')[0].text[2:].strip() # remove '제목'
        url = 'https://www1.president.go.kr/petitions/%d' % petition_num
        return (category, title, url)

    links = []
    for p in range(begin_page, end_page + 1):
        url = 'https://www1.president.go.kr/petitions?page={}'.format(p)
        soup = get_soup(url)
        div = soup.select('div[class^=board]')
        for li in soup.select('div[class^=b_list] div[class=bl_body] li'):
            try:
                link = parse_link(li)
                links.append(link)
            except:
                continue

        if p % 10 == 0:
            time.sleep(SLEEP)
        time.sleep(0.05) # default sleep

        if VERBOSE:
            print('\rget petitions links from {} / {} pages'.format(p, max_pages), end='')

    return links