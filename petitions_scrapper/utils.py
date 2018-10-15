import re
import requests
from bs4 import BeautifulSoup
from time import gmtime, strftime


def now():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def get_soup(url):
    r = requests.get(url)
    html = r.text
    page = BeautifulSoup(html, 'lxml')
    return page

doublespace_pattern = re.compile('\s+')
lineseparator_pattern = re.compile('\n+')

def normalize_text(text):
    #text = text.replace('\t', ' ')
    #text = text.replace('\r', ' ')
    #text = lineseparator_pattern.sub('\n', text)
    text = doublespace_pattern.sub(' ', text)
    return text.strip()