from .utils import get_soup

def get_petition_links(max_pages=10):

    def parse_link(li):
        category = li.select('div[class^=bl_category]')[0].text[2:].strip() # remove '분류'
        petition_num = int(li.select('div[class=bl_no]')[0].text[2:].strip()) # remove '번호'
        title = li.select('a')[0].text[2:].strip() # remove '제목'
        return (category, petition_num, title)

    links = []
    for p in range(1, max_pages + 1):
        url = 'https://www1.president.go.kr/petitions?page={}'.format(p)
        soup = get_soup(url)
        div = soup.select('div[class^=board]')
        for li in soup.select('div[class^=b_list] div[class=bl_body] li'):
            try:
                link = parse_link(li)
                links.append(link)
            except:
                continue

    return links