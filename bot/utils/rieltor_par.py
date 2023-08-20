from config import city, rielt_room, rielt_rooms, sort, fake_user
from aiogram.utils.markdown import hbold, hlink
from bs4 import BeautifulSoup
from aiogram import types
from random import choice
import requests
import time


async def call_data_rieltor(message: types.Message, user_param):
    """
    функция генерирует ссылку с параметрами пользователя
    парсит сайт rieltor.ua
    отправляет найденные объявления на сайте (max - 8 объявлений) в сообщения юзеру
    после отправки - time.sleep(2)

    Args:
        message (types.Message): сообщзение пользователя
        user_param (_type_): параметры юзера с БД
    """

    ua = choice(fake_user)

    parametrs = {
        'rooms': '',
        'price_min': f'&price_min={user_param.min_price}' if user_param.min_price is not None else "",
        'price_max': f'&price_max={user_param.max_price}' if user_param.max_price is not None else "",
        'city': city[user_param.city][1],
        'floor_min': f'&floor_min={user_param.min_floor}' if user_param.min_floor is not None else "",
        'floor_max': f'&floor_max={user_param.max_floor}' if user_param.max_floor is not None else "",
        'sort': f'&sort={sort[user_param.sort][1]}' if user_param.sort is not None else sort['Пропуск'][1]
    }

    count_rooms = list(map(int, user_param.count_rooms.replace(
        '-', ''))) if user_param.count_rooms is not None else ""
    if len(count_rooms) == 1:
        parametrs['rooms'] = f'{rielt_room[int(user_param.count_rooms)-1]}/?'
    elif len(count_rooms) > 1:
        list_of_room = []
        for i in count_rooms:
            list_of_room.append(rielt_rooms[int(i)-1])
        parametrs['rooms'] = '?' + '&'.join(list_of_room)

    gen_of_link = f'{parametrs["rooms"]}{parametrs["price_min"]}{parametrs["price_max"]}{parametrs["floor_min"]}{parametrs["floor_max"]}{parametrs["sort"]}'

    url = f'https://rieltor.ua/{parametrs["city"]}/flats-rent/{gen_of_link}'

    data_rieltor = []

    response = requests.get(
        url=url,
        headers={'user-agent': ua},
    )
    try:

        soup = BeautifulSoup(response.text, 'lxml')

        # поиск всех объявлений
        mdiv = soup.find_all(class_='catalog-card')

        dublicate = []

        if len(mdiv) == 0 or soup.find("div", class_='sort-wrap catalog-sort-wrap catalog-sort-wrap-pc').find('span').get_text().strip() == 'За вашим запитом пропозицій не знайдено':
            await message.answer('За заданными критериями ничего не найдено 😅\nпопробуйте изменить параметры')
            return
        else:
            sps = mdiv

        for div in sps:
            try:
                price = div.find(
                    'div', class_='catalog-card-price').text.strip()
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
                        "Ссылка": link
                    }
                )
                dublicate.append(addres)

            if len(data_rieltor) == 8:
                break

        for item in data_rieltor:
            card = f'{hlink(item.get("Адрес"), item.get("Ссылка"))}\n' \
                f'{hbold("Цена: ")}{item.get("Цена")}\n' \
                f'{hbold("Район: ")}{item.get("Район")}'

            await message.answer(card)

        time.sleep(2)
    except:
        await message.answer('Не удалось соединиться с rieltor.ua')
