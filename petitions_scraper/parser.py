import math
import time

from .utils import get_soup
from .utils import now
from .utils import normalize_text

def parse_page(url):
    """Parse a petition page

    It return parsed informations which is JSON format.
    It contains
      - 데이터 수집 시각
      - 상태 : [청원시작, 청원진행중, 청원종료, 브리핑]
      - 청원 개요
      - 청원 동의 수

    :param url: str format html url
        for example, 'https://www1.president.go.kr/petitions/407329'
    """

    headers = {
        "Referer": "https://www1.president.go.kr/petitions/?c=0&only=2&page=4&order=1",
    }
    soup = get_soup(url, headers=headers)
    if not soup:
        raise ValueError('Exception: parse_page. soup is None')

    if is_closed_petition(soup):
        return -1

    crawled_at = now()
    category, begin, end = parse_meta(soup)
    title = soup.select('h3[class=petitionsView_title]')[0].text
    content = parse_content(soup)
    num_agree = parse_number_of_agree(soup)
    petition_idx = url.split('/')[-1]
    status = parse_status(soup)

    json_format = _as_json(crawled_at, category, begin, end,
        content, num_agree, petition_idx, status, title)

    return json_format

def _as_json(crawled_at, category, begin, end, content,
    num_agree, petition_idx, status, title):

    json_format = {
        'crawled_at' : crawled_at,
        'category' : category,
        'begin' : begin,
        'end' : end,
        'content' : content,
        'num_agree' : num_agree,
        'petition_idx': petition_idx,
        'status' : status,
        'title': title
    }

    return json_format

def is_closed_petition(soup):
    text = '청원 요건에 위배되어 관리자에 의해 비공개된 청원입니다.'
    try:
        return text == soup.select('span[class=text]')[0].text.strip()
    except:
        return False

def parse_meta(soup):
    meta = soup.select('ul[class=petitionsView_info_list] li')
    if not meta or len(meta) != 4:
        raise ValueError('Exception: parse_meta')
    category = meta[0].text.strip()[4:]
    begin = meta[1].text.strip()[4:]
    end = meta[2].text.strip()[4:]
    return category, begin, end

def parse_content(soup):
    content = soup.select('div[class=petitionsView_write] div[class=View_write]')
    if not content:
        return ''
    return normalize_text(content[0].text)

def parse_number_of_agree(soup):
    agree = soup.select('div[class=Reply_area_head] span')
    if not agree:
        return -1
    return int(agree[0].text.replace(',',''))

def parse_status(soup):
    stage_names = '청원시작 청원진행중 청원종료 브리핑'.split()
    stages = soup.select('div[class=petitionsView_grapy] li')
    for stage, name in zip(stages, stage_names):
        if '현재 상태' in stage.text:
            return name
    return 'Exception'
