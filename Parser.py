import re
import os
import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent



url = "https://www.detmir.ru/catalog/index/name/lego/page/1/"

ua = UserAgent()

headers = {'User-Agent': ua.random,
           'Content-Type': 'application/json',
           'X-CSRF-Token': '1',
           'X-Requested-With': 'detmir-js-sdk',
           }

cookies = dict(BCPermissionLevel='PERSONAL')

list_pages = []
list_tags = []
name = []
price = []
p_price = []
link = []
id = []


def get_pages(lp: list):
    page = 1
    while page < 18:
        new_page = "https://www.detmir.ru/catalog/index/name/lego/page/{}/".format(page)
        page += 1
        lp.append(new_page)
    return lp


def get_soup(lp: list):
    for i in lp:
        with open('html.txt', 'w', encoding='utf-8') as f:
            response = requests.get(i, headers=headers, cookies=cookies)
            f.write(response.text)
            with open("html.txt", encoding='utf-8') as nf:
                soup = BeautifulSoup(nf, 'html.parser')
                tags = soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['oQ'])

                for names in tags.find_all('p', class_='ND'):
                    name_re = re.sub(r'\d+$', '', *names)
                    name.append(name_re)
                    id_re = re.sub(r'\D', '', *names)
                    if len(id_re) == 5:
                        id.append(id_re)
                    else:
                        id.append(id_re[-5:])

                for qwerty in (tags.find_all('div', class_='NN NR') and tags.find_all('div', class_='NN')):
                    string = str(qwerty)
                    first, second = string[:50], string[50:]  # len(string)/2
                    p_price_re1 = re.sub(r'\D', '', first)
                    p_price_re2 = re.sub(r'\D', '', second)
                    p_price_re3 = (p_price_re1 + ' ' + p_price_re2)
                    if len(p_price_re3) > 5:
                        p_price.append(p_price_re1)
                        price.append(p_price_re2)
                    if len(p_price_re3) < 6:
                        p_price.append(p_price_re2)
                        price.append(p_price_re1)

                for links1 in tags:
                    for links2 in links1.find_all('a', href=True):
                        link.append(links2['href'])


def cvs_writer(*args):
    with open('result.csv', 'w', newline='', encoding='utf-8') as csvf:
        writer = csv.writer(csvf)
        writer.writerows([['id', 'title', 'price', 'promo_price', 'url']])
        for line1, line2, line3, line4, line5 in zip(*args):
            writer.writerows([[line1, line2, line3, line4, line5]])


if __name__ == '__main__':
    p = get_pages(list_pages)
    get_soup(p)
    cvs_writer(id, name, price, p_price, link)
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'html.txt')
    os.remove(path)