from aiogram.utils.markdown import hbold, hlink
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from aiogram import types
from config import city
import requests
import time


## заготовка под генерацию ссылки с параметрами

'''room = ['1', '2', '3']
rooms = {'1,2': '1%2C2', '1,3': '1%2C3', '2,3': '2%2C3', '1,2,3': '1%2C2%2C3'}

city = ['&city_id=29586', '&city_id=29585',
        '&city_id=29587', '&city_id=29588', '&city_id=29595']

sorti = ['default', 'date', 'nedorogo', 'elit']

parametrs = {
    'rooms': '',
    'city': '',
    'price_min': '',
    'price_max': '',
    'floor_min': '',
    'floor_max': '',
    'sort': sorti[0]
}

parametrs['city'] = city[int(
    input('1-kiev\n2-odesa\n3-dnipro\n4-harkiv\n5-zaporijjya\n'))-1]

roomes = []
c_room = input('Кол. комнат: ')
while c_room != '0':
    roomes.append(c_room)
    c_room = input('Кол. комнат: ')
roomes = list(set(roomes))
mn_price = input('Мин: ')
mx_price = input('Мах: ')
mn_floor = input('ЭМин: ')
mx_floor = input('Эmax: ')
sort = int(input(
    '0-без сорт\n1-найновіші\n2-найдешевші\n3-найдорожчі\n'))

if len(roomes) == 1:
    parametrs['rooms'] = f'&rooms_id={roomes[0]}&rooms_url={roomes[0]}'
elif len(roomes) > 1:
    parametrs['rooms'] = f'&rooms_id={rooms[",".join(roomes)]}&rooms_url={rooms[",".join(roomes)]}'


if mn_price != '0':
    parametrs['price_min'] = f'&price_from={mn_price}'
if mx_price != '0':
    parametrs['price_max'] = f'&price_to={mx_price}'

if mn_floor != '0':
    parametrs['floor_min'] = f'&floor_from={mn_floor}'
if mx_floor != '0':
    parametrs['floor_max'] = f'&floor_to={mx_floor}'

if sort != '0':
    parametrs['sort'] = f'&price_sort={sorti[sort]}'

gen_of_link = f'{parametrs["rooms"]}{parametrs["price_min"]}{parametrs["price_max"]}{parametrs["floor_min"]}{parametrs["floor_max"]}{parametrs["sort"]}{parametrs["city"]}'

link = f'https://www.country.ua/list/?action_id=2&action_url=rent&type_id=1&type_url=flat{gen_of_link}&filter_flat_type_id=1&filter_flat_type_url=flat&price_currency=uah'

print(
    'https://www.country.ua/list/?action_id=2&action_url=rent&type_id=1&type_url=flat&rooms_id=1%2C2&rooms_url=1%2C2&filter_flat_type_id=1&filter_flat_type_url=flat&price_currency=uah&price_from=4000&price_to=9000&floor_from=2&floor_to=5&city_id=29595&lang=ua&price_sort=default')
print(link)'''

async def call_data_country(message: types.Message, user_param):

    ua = UserAgent()

    parametrs = {
        'rooms': user_param.count_rooms,
        'price_min': user_param.min_price,
        'price_max': user_param.max_price,
        'city': city[user_param.city][2],
        'floor_min': user_param.min_floor,
        'floor_max': user_param.max_floor,
        'sort': user_param.sort
    }

    url = 'https://www.country.ua/ua/rent/flat.html'

    data_country = []

    response = requests.get(
        url=url,
        headers={'user-agent': f'{ua.random}'},
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
        
        ## ответ с country
        for index, item in enumerate(data_country):
            card = f'{hlink(item.get("Адрес"), item.get("Ссылка"))}\n' \
            f'{hbold("Цена: ")}{item.get("Цена")}\n'
            
            if index%10 == 0:
                time.sleep(3)

            await message.answer(card)
        time.sleep(2)        
    else:
        await message.answer('Не удалось соединиться с country.ua')
