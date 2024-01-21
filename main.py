import requests
from pyquery import PyQuery

response = requests.get('https://www.cnbcindonesia.com/news/indeks/3/1')
print(response)

html = PyQuery(response.text)

link = html.find('ul[class="list media_rows middle thumb terbaru gtm_indeks_feed"] >li')
print(link.find('a').attr('href'))

for url in link:
    print(PyQuery(url).find('a').attr('href'))

