from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests


def call_data_rieltor():

    ua = UserAgent()
    city = 'kiev'
    price_min = ''
    price_max = ''
    sort = "byprice"

    room = ''

    params = {
        "price_min": price_min,
        "price_max": price_max,
        "sort": sort
    }

    url = 'https://rieltor.ua/{}/flats-rent/{}'.format(city, room)

    data_rieltor = []

    response = requests.get(
        url=url,
        headers={'user-agent': f'{ua.random}'},
        params=params
    )
    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'lxml')
        mdiv = soup.find_all(class_='catalog-card')
        dublicate = []

        # 8 объявлений
        for div in mdiv[:8]:
            try:
                price = div.find('div', class_='catalog-card-price').text.strip()
            except:
                price = 'No price'
            try:
                addres = div.find('div', class_="catalog-card-address").text
            except:
                addres = 'No address'
            try:
                link = div.find('a', class_='catalog-card-media').get('href')
            except:
                link = 'No link'
            try:
                area = div.find(
                    'div', class_='catalog-card-region').find_all('a')[1].text.strip()
            except:
                area = 'No area'

            if addres not in dublicate:
                data_rieltor.append(
                    {
                        "Цена": price,
                        "Район": area,
                        "Адрес": addres,
                        "Ссылка": link,
                    }
                )
                dublicate.append(addres)
        return data_rieltor
    else:
        return 'error'
