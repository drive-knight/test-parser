import re
import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


url = "https://www.detmir.ru/catalog/index/name/lego/"

ua = UserAgent()

headers = {'User-Agent': ua.random,
           'Content-Type': 'application/json',
           'X-CSRF-Token': '1',
           'X-Requested-With': 'detmir-js-sdk',
           }

cookies = dict(BCPermissionLevel='PERSONAL')
response = requests.get(url, headers=headers, cookies=cookies)


with open('html.txt', 'w', encoding='utf-8') as f:
    f.write(response.text)

with open("html.txt", encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')


tags = soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['n_9'])

link_list = []
price_list = []
p_price_list = []
name_list = []
id_list = []
city_list = []


el = 0
try:
    while el < 501:
        for link in tags.contents[el]:
            for a in link.find_all('a', href=True):
                link_list.append(a['href'])
                el += 1
except IndexError:
    pass

el = 0
try:
    while el < 501:
        for p_price in tags.contents[el].find("p", class_="Oe"):
            # p_price1 = re.sub(r'\D', '', p_price)
            if p_price is not None:
                p_price_list.append(p_price)
                el += 1
            else:
                p_price_list.append("-")
                el +=1
except IndexError:
    pass

el = 0
try:
    while el < 501:
        for price in tags.contents[el].find("p", class_="Of").find(class_='Og'):
            # price1 = re.sub(r'\D', '', price)
            price_list.append(price)
            el += 1
except IndexError:
    pass

el = 0
try:
    while el < 501:
        for name in tags.contents[el].p:
            name_re = re.sub(r'[^\w\s]+|[\d]+', '', name)
            id_re = re.sub(r'\D', '', name)
            name_list.append(name_re)
            id_list.append(id_re)
            el += 1
except IndexError:
    pass


with open('result.csv', 'w', newline='', encoding='utf-8') as csvf:
    writer = csv.writer(csvf)   
    writer.writerows([['id', 'title', 'price', 'promo_price', 'url']])
    for line1, line2, line3, line4, line5 in zip(id_list, name_list, price_list, p_price_list, link_list):
        writer.writerows([[line1, line2, line3, line4, line5]])