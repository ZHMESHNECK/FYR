from aiogram.utils.markdown import hbold, hlink
from config import city, country_rooms, sort
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from aiogram import types
import requests
import time


async def call_data_country(message: types.Message, user_param):

    ua = UserAgent()

    parametrs = {
        'rooms':  '',
        'price_min': f'&price_from={user_param.min_price}' if user_param.min_price is not None else "",
        'price_max': f'&price_to={user_param.max_price}' if user_param.max_price is not None else "",
        'city': f'&city_id={city[user_param.city][2]}',
        'floor_min': f'&floor_from={user_param.min_floor}' if user_param.min_floor is not None else "",
        'floor_max': f'&floor_to={user_param.max_floor}' if user_param.max_floor is not None else "",
        'sort': f'&price_sort={sort[user_param.sort][2]}' if user_param.sort is not None else f"&price_sort={sort['Пропуск'][2]}"
    }

    count_rooms = list(user_param.count_rooms.replace(
        '-', '')) if user_param.count_rooms is not None else ""
    if len(count_rooms) == 1:
        parametrs['rooms'] = f'&rooms_id={user_param.count_rooms}&rooms_url={user_param.count_rooms}'
    elif len(count_rooms) > 1:
        parametrs['rooms'] = f'&rooms_id={country_rooms[",".join(count_rooms)]}&rooms_url={country_rooms[",".join(count_rooms)]}'

    gen_of_link = f'{parametrs["rooms"]}{parametrs["price_min"]}{parametrs["price_max"]}{parametrs["floor_min"]}{parametrs["floor_max"]}{parametrs["sort"]}{parametrs["city"]}'

    url = f'https://www.country.ua/list/?action_id=2&action_url=rent&type_id=1&type_url=flat{gen_of_link}&filter_flat_type_id=1&filter_flat_type_url=flat&price_currency=uah'

    response = requests.get(
        url=url,
        headers={'user-agent': f'{ua.random}'},
    )

    try:
        soup = BeautifulSoup(response.text, 'lxml')
        mdiv = soup.find_all(
            class_='catalog__item item-catalog item-catalog_top')

        data_country = []

        if len(mdiv) == 0 or soup.find(string='К сожалению, по вашему запросу ничего не найдено.') is not None:
            await message.answer('За заданными критериями ничего не найдено 😅\nпопробуйте изменить параметры')
            sps = []
        elif len(mdiv) <= 8:
            sps = mdiv
        elif len(mdiv) > 8:  # 8 объявлений без рекламы
            sps = mdiv[3:11]

        for div in sps:
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

        # ответ с country
        for item in data_country:
            card = f'{hlink(item.get("Адрес"), item.get("Ссылка"))}\n' \
                f'{hbold("Цена: ")}{item.get("Цена")}\n'

            await message.answer(card)
        time.sleep(2)
    except:
        await message.answer('Не удалось соединиться с country.ua')
