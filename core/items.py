# Collect DaruKade Comments by url

import time
import os
import json

from bs4 import BeautifulSoup as Soup
from bs4 import SoupStrainer as Strainer

import grequests


# Start the Timer
start_time = time.perf_counter()

# File dirs
dir_path = os.path.dirname(os.path.realpath(__file__))
file = f"{dir_path}"

import links as l

def get_data(urls):
    """Get data of urls with grequests."""
    req = (grequests.get(link) for link in urls)
    response = grequests.map(req)
    return response


def find_mic_detail(status, pos):
    if pos == 2:
        tmp = status.split()
        tmp.pop(1)
        tmp.pop(0)
        res = ' '.join(tmp)
        return res
    if pos == 1:
        tmp = status.split()
        tmp.pop(0)
        res = ' '.join(tmp)
        return res


def parse(data):
    """Parse and return all comments."""    
    only_item_cells = Strainer('div', attrs={'class': 'comment-box'})
    info_item_cell = Strainer('div', attrs={'class', 'title-layer'})
    brand_item_cell = Strainer('div', attrs={'class', 'right'})
    group_item_cell = Strainer('section', attrs={'class', 'accordion-layer'})
    comments = []

    for d in data:
        detail = Soup(d.text, 'html.parser', parse_only=info_item_cell)
        detail_brand = Soup(d.text, 'html.parser', parse_only=brand_item_cell).text.strip()
        raw_comments = Soup(d.text, 'html.parser', parse_only=only_item_cells)
        group_item = Soup(d.text, 'html.parser', parse_only=group_item_cell)

        for group in group_item.find_all('div', {'class': 'each-row'}):
            if 'گروه' in group.text:
                Group = find_mic_detail(group.text.strip(), 1)
        # It contains detail so spilt them by \n
        object_comment = {
            'ProductPageLink': None,
            'ProductName': detail.find('h1').text.strip(),
            'Productcode': detail.find('span', {'class': 'code'}).text.strip(),
            'BrandNameFa': detail_brand.split('-')[0].strip(),
            'BrandNameEn': detail_brand.split('-')[1].strip(),
            'Group': Group,
            'Comments': None,
        }
        
        all_comments = []
        for r in raw_comments:
            """ Each comment-box in page """
            ids = r.find_all('div', {'class': 'info'})
            descriptions = r.find_all('p', {'class': 'CommentsStyle1'})
            # There are n comments/descriptions in each comment-box
            n = len(descriptions)
            for i in range(n):
                """ Each comment box content """
                user_comment = {
                    'CommentOwnerId': ids[i].text.strip().split('\n')[0].strip(),
                    # It contains datetime so spilt them by \n
                    'CommentDate': ids[i].text.strip().split('\n')[1].strip(),
                    'CommentDescription': descriptions[i].text.strip()
                }   
                all_comments.append(user_comment)
        object_comment['Comments'] = all_comments
        return object_comment

resp = get_data(l.links)
result = parse(resp)

# Serializing json   
with open('tests/output.json', 'w') as f:
    # json_object = json.dumps(result, ensure_ascii=False, indent=4)
    json.dump(result, f, ensure_ascii=False, indent=4)

fin = time.perf_counter() - start_time
print(f'Process finished. \n --- {fin} seconds ---')
