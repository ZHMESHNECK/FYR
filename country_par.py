
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests


def call_data_country():

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

    url = 'https://www.country.ua/ua/rent/flat.html'

    data_country = []

    response = requests.get(
        url=url,
        headers={'user-agent': f'{ua.random}'},
        params=params
    )
    if response.status_code == 200:
        # with open('counry.html', 'r', encoding='utf-8') as file:
        #     src = file.read()

        soup = BeautifulSoup(response.text, 'lxml')
        # with open('counry.html', 'w', encoding='utf-8') as file:
        #     file.write(str(soup))

        mdiv = soup.find_all(
            class_='catalog__item item-catalog item-catalog_top')

        data_country = []

        #  8 объявлений без рекламы
        for div in mdiv[3:11]:
            try:
                price = div.find('div', class_='item-catalog__price').text
            except:
                price = 'Цена не найдена'
            try:
                addres = div.find(
                    'div', class_='item-catalog__address address')
            except:
                addres = 'Адрес не найден'

            try:
                link = div.find(
                    'div', class_='item-catalog__text').find('a').get('href')
            except:
                link = 'Ссылка не найдена'
            data_country.append(
                {
                    "Адрес": addres.text.replace('\xa0', ''),
                    "Цена": price,
                    "Ссылка": 'https://www.country.ua'+link
                })
        return data_country
    else:
        return 'error'
