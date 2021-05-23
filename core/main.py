# Collect DaruKade Comments by url

import time
import os
import datetime
import grequests

from bs4 import BeautifulSoup as Soup
from bs4 import SoupStrainer as Strainer

from database import DB
import links as li


# Start the Timer
start_time = time.perf_counter()

# File dirs
dir_path = os.path.dirname(os.path.realpath(__file__))
file = f"{dir_path}"


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


def main(data):
    """ Parse and return all comments. """
    only_item_cells = Strainer('div', attrs={'class': 'comment-box'})
    info_item_cell = Strainer('div', attrs={'class', 'title-layer'})
    brand_item_cell = Strainer('div', attrs={'class', 'right'})
    group_item_cell = Strainer('section', attrs={'class', 'accordion-layer'})
    allres = []
    count = 0

    # Database collection
    mydb.select_database('darukade')

    for d in data:
        detail = Soup(d.text, 'html.parser', parse_only=info_item_cell)
        detail_brand = Soup(d.text, 'html.parser', parse_only=brand_item_cell).text.strip()
        raw_comments = Soup(d.text, 'html.parser', parse_only=only_item_cells)
        group_item = Soup(d.text, 'html.parser', parse_only=group_item_cell)
        for group in group_item.find_all('div', {'class': 'each-row'}):
            if 'گروه' in group.text:
                Group = find_mic_detail(group.text.strip(), 1)

        # Database
        Productcode = detail.find('span', {'class': 'code'}).text.strip()
        mydb.items_col()
        item = mydb.find_one({'Productcode': Productcode})

        if item:  # Item exist.
            if item['Count'] < len(raw_comments):
                for r in raw_comments:
                    """ Each comment-box in page """
                    ids = r.find_all('div', {'class': 'info'})
                    descriptions = r.find_all('p', {'class': 'CommentsStyle1'})
                    # There are n comments/descriptions in each comment-box
                    n = len(descriptions) - item['Count']
                    for i in range(n):
                        """ Each comment box content """
                        user_comment = {
                            'InfoUpdateDate': datetime.datetime.utcnow(),
                            'ProductPageLink': li.links[count],
                            'ProductName': detail.find('h1').text.strip(),
                            'Productcode': detail.find('span', {'class': 'code'}).text.strip(),
                            'BrandNameFa': detail_brand.split('-')[0].strip(),
                            'BrandNameEn': detail_brand.split('-')[1].strip(),
                            'Group': Group,
                            'CommentOwnerId': ids[i].text.strip().split('\n')[0].strip(),
                            # It contains datetime so spilt them by \n
                            'CommentDate': ids[i].text.strip().split('\n')[1].strip(),
                            'CommentDescription': descriptions[i].text.strip().replace("\n", "")
                        }
                        mydb.insert_one(user_comment)

        else:
            item_detail = {
                        'Productcode': Productcode,
                        'ProductPageLink': li.links[count],
                        'Count': len(raw_comments),
                        }
            mydb.insert_one(item_detail)
            mydb.comments_col()
            for r in raw_comments:
                """ Each comment-box in page """
                ids = r.find_all('div', {'class': 'info'})
                descriptions = r.find_all('p', {'class': 'CommentsStyle1'})
                # There are n comments/descriptions in each comment-box
                n = len(descriptions)
                for i in range(n):
                    """ Each comment box content """
                    user_comment = {
                        'ProductPageLink': li.links[count],
                        'ProductName': detail.find('h1').text.strip(),
                        'Productcode': detail.find('span', {'class': 'code'}).text.strip(),
                        'BrandNameFa': detail_brand.split('-')[0].strip(),
                        'BrandNameEn': detail_brand.split('-')[1].strip(),
                        'Group': Group,
                        'CommentOwnerId': ids[i].text.strip().split('\n')[0].strip(),
                        # It contains datetime so spilt them by \n
                        'CommentDate': ids[i].text.strip().split('\n')[1].strip(),
                        'CommentDescription': descriptions[i].text.strip().replace("\n", "")
                    }
                    mydb.insert_one(user_comment)

                # allres.append(user_comment)
        count += 1  # For links navigation
    return allres


if __name__ == '__main__':
    
    mydb = DB()
    mydb.connect()

    resp = get_data(li.links)
    result = main(resp)
    
    site_addr = 'https://www.darukade.com'
    now = datetime.datetime.utcnow()
    mydb.refweb(now, site_addr)

    fin = time.perf_counter() - start_time
    print(f'Process finished. \n --- {fin} seconds ---')
