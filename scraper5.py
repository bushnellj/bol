import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = 'https://www.bol.com'

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}

productlinks = []

for x in range(1,2):
        r = requests.get(f'https://www.bol.com/nl/nl/l/printers-scanners-kopieerapparaten/7134/?page={x}')
        soup = BeautifulSoup(r.content, 'html.parser')

        productlist = soup.find_all('li', class_='product-item--row')

        for item in productlist:
            for link in item.find_all('a', class_='product-title', href=True):
                productlinks.append(baseurl + link['href'])


#testlink = 'https://www.bol.com/nl/nl/p/msi-optix-g27c6p-full-hd-curved-165-hz-gaming-monitor-27-inch/9300000016569218/'

printerlist = []

for link in productlinks:
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        name = soup.find('h1', class_='page-heading').text.strip()
        price = soup.find('div', class_='price-block__highlight').text.strip()
        stock = soup.find('div', class_='buy-block--with-highlight').text.strip()
        printers = {
                'name' : name[0:30],
                'price' : price,
                'stock' : stock[0:12]
                }

        printerlist.append(printers)
        print('Name: ', printers['name'])


df = pd.DataFrame(printerlist)
df.to_csv('bol-printers.csv')
df.to_excel('bol-printers.xlsx')
print('saved to file')
