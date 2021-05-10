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
    req = [grequests.get(link) for link in urls]
    response = grequests.map(req)
    return response


def parse(data):
    """Parse and return all comments."""
    only_item_cells = Strainer('div', attrs={'class': 'comment-box'})
    comments = []
    for d in data:
        raw_comments = Soup(d.text, 'html.parser', parse_only=only_item_cells)
    for r in raw_comments:
        """ Each comment-box in page """
        ids = r.find_all('div', {'class': 'info'})
        descriptions = r.find_all('p', {'class': 'CommentsStyle1'})
        # There are n comments/descriptions in each comment-box
        n = len(descriptions)
        for i in range(n):
            """ Each comment box content """
            # It contains datetime so spilt them by \n
            CommentOwnerId = ids[i].text.strip().split('\n')[0]
            CommentDate = ids[i].text.strip().split('\n')[1]
            CommentDescription = descriptions[i].text.strip()
            # print(CommentDate)
            # print('---------------')
    return comments


resp = get_data(l.links)
result = parse(resp)

fin = time.perf_counter() - start_time
print(f'Process finished. \n --- {fin} seconds ---')
