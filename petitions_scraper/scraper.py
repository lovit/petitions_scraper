import time
from .utils import get_soup

def parse_link(li):
    category = li.select('div[class^=bl_category]')[0].text[2:].strip() # remove '분류'
    title = li.select('a')[0].text[2:].strip() # remove '제목'
    href = li.select('a')[0]['href']
    url = href.split('?')[0]
    return (category, title, url)

def yield_petition_links(begin_page=1, end_page=10, sleep=0.5, verbose=True):
    """
    Arguments
    ---------
    begin_page : int
        First page number
    end_page : int
        Last page number
    sleep : float
        Sleep time for each page
    verbose : Boolean
        If True, it shows status

    Yields
    ------
    (category, title, url)
    """
    raise ValueError("This function doesn't works any more")

    """
    for p in range(begin_page, end_page + 1):
        url = 'https://www1.president.go.kr/petitions?c=0&only=2&page={}&order=1'.format(p)
        try:
            soup = get_soup(url)
            print(soup.text)
        except:
            print('\nException while getting soup page=%d' % p)
            continue

        try:
            lis = soup.select('ul[class=petition_list] div[class=bl_wrap]')
            print(len(lis))
            for li in lis:
                try:
                    link = parse_link(li)
                    yield link
                except Exception as e:
                    print(e)
                    continue
        except Exception as e:
            print('Exception while parsing link')
            print(e)
            continue

        time.sleep(sleep)

        if verbose:
            print('\rget petitions links from {} in ({} - {}) pages'.format(
                p, begin_page, end_page), end='')
            if p % 100 == 0:
                print()
    """


def get_petition_links(begin_page=1, end_page=10, sleep=0.5, verbose=True):
    """
    Arguments
    ---------
    begin_page : int
        First page number
    end_page : int
        Last page number
    sleep : float
        Sleep time for each page
    verbose : Boolean
        If True, it shows status

    Returns
    ------
    list of links. Each link is three column tuple. (category, title, url)
    """

    raise ValueError("This function doesn't works any more")

    """
    links = [link for link in yield_petition_links(begin_page, end_page, sleep, verbose)]
    print('\ngetting petition links was done')
    return links
    """
