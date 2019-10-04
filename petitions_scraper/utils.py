import re
import requests
from bs4 import BeautifulSoup
from time import gmtime, strftime


def now():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def get_soup(url, headers=None):
    r = requests.get(url, headers=headers, timeout=3)
    html = r.text
    page = BeautifulSoup(html, 'lxml')
    return page

def show_categories():
    url = 'https://www1.president.go.kr/petitions/category'
    soup = get_soup(url)
    for li in soup.select('div[class=category_area] li'):
        name = li.text
        category_idx = str(li).split('="')[-1].split('"')[0]
        print('idx = {:3}, name = {}'.format(category_idx, name))

doublespace_pattern = re.compile('\s+')
lineseparator_pattern = re.compile('\n+')

def normalize_text(text):
    #text = text.replace('\t', ' ')
    #text = text.replace('\r', ' ')
    #text = lineseparator_pattern.sub('\n', text)
    text = doublespace_pattern.sub(' ', text)
    return text.strip()