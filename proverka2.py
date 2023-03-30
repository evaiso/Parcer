import requests
from bs4 import BeautifulSoup
import csv
CSV = 'kursi.csv'
HOST = 'https://select.by'
URL = 'https://select.by/kurs/'
HEADERS = {
    'accept': 'Поиск этой переменной на странице сайта, который парсим. Открываем код, далее network, обновляем информацию, ищем первый файл и в нем ищем Accept.',
    'useragent': 'Аналогично выше описанному методу '
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup (html,'html.parser')
    inf = []

    for tr in soup.select('tr.tablesorter-hasChildRow'):
        tds = tr.select('td')
        tds2 = tr.select('a')
        inf.append (
            {
                'name_bank':tds2[0].text,
                'usd_buy':tds[1].text,
                'usd_sell':tds[2].text,
                'euro_buy':tds[3].text,
                'euro_sell':tds[4].text
            }
        )
    return inf

def save_content(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Доллар покупка', 'Доллар продажа', 'Евро покупка','Евро продажа'])
        for item in items:
            writer.writerow( [item['name_bank'], item['usd_buy'], item['usd_sell'], item['euro_buy'], item['euro_sell']])

def parser():
    PAGENATION = input("Укажите количество страниц для парсинга: ")
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        inf = []
        for page in range(1, PAGENATION):
            print(f'Парсим страницу: ', {page})
            html = get_html(URL,params={'page':page})
            inf.extend(get_content(html.text))
            save_content(inf, CSV)
    else:
        print("Error")

parser()