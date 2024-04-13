from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from aiogram.utils.markdown import hbold, hlink
from config import city, sort, fake_user, osp
from selenium import webdriver
from bs4 import BeautifulSoup
from aiogram import types
from random import choice
import asyncio
import logging
import environ
import time


env = environ.Env()
env.read_env('.env')


async def call_data_olx(message: types.Message, user_param):
    """
    функция генерирует ссылку с параметрами пользователя
    открывает firefox
    парсит olx
    закрывает firefox
    отправляет найденные объявления на сайте (max - 8 объявлений) в сообщения юзеру
    после отправки -  time.sleep(2)

    Args:
        message (types.Message): сообщзение пользователя
        user_param (_type_): параметры юзера с БД
    """
    try:
        options = Options()
        options.set_preference("general.useragent.override",
                               f'{choice(fake_user)}')
        options.add_argument('--headless')

        if "Windows" in osp:
            # путь к расположению браузера ( там же у меня и расположен geckodriver )
            options.binary_location = env('WINDOWS')
            driver = webdriver.Firefox(options=options)
        elif "Linux" in osp:
            # путь к расположению браузера
            options.binary_location = env('LINUX')
            # пусть к расположению geckodriver
            driver = webdriver.Firefox(
                executable_path=env('LINUX_DRIVER'), options=options)

        room = ['odnokomnatnye', 'dvuhkomnatnye', 'trehkomnatnye']
        parametrs = {
            'rooms': "&".join([f'search[filter_enum_number_of_rooms_string][{num}]={room[int(rom)-1]}' for num, rom in enumerate(list(map(int, user_param.count_rooms.replace('-', ''))))]) if user_param.count_rooms is not None else "",
            'price_min': f'&search[filter_float_price:from]={user_param.min_price}' if user_param.min_price is not None else "",
            'price_max': f'&search[filter_float_price:to]={user_param.max_price}' if user_param.max_price is not None else "",
            'city': city[user_param.city][0],
            'floor_min': f'&search[filter_float_floor:from]={user_param.min_floor}' if user_param.min_floor is not None else "",
            'floor_max': f'&search[filter_float_floor:to]={user_param.max_floor}' if user_param.max_floor is not None else "",
            'sort': f'&search[order]={sort[user_param.sort][0]}' if user_param.sort is not None else sort['Пропуск'][0]
        }
        gen_of_link = f'{parametrs["rooms"]}{parametrs["price_min"]}{parametrs["price_max"]}{parametrs["floor_min"]}{parametrs["floor_max"]}{parametrs["sort"]}'

        url = f'https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/{parametrs["city"]}/?{gen_of_link}'

        # список объявлений на отправку
        data_olx = []

        # Читаем страницу olx
        driver.get(url=url)

        # поиск всех объявлений
        soup = BeautifulSoup(driver.page_source, 'lxml')
        mdiv = soup.find_all('div', class_='css-1sw7q4x')

    except (Exception, TimeoutException):
        logging.error('call_data_olx - driver', exc_info=True)
        await message.answer('Не удалось соединиться с OLX')
        return

    finally:
        if 'driver' in locals():
            driver.close()
            driver.quit()

    if len(mdiv) == 0 or soup.find(string='Ми знайшли 0 оголошень') is not None:
        await message.answer('За заданными критериями ничего не найдено 😅\nпопробуйте изменить параметры')
        return
    else:
        sps = mdiv

    try:
        for div in sps:
            # если это рекламное объявление, то пропускаем его
            if not div.find('div', class_='css-1jh69qu'):
                try:
                    price = div.find('p', {'data-testid': 'ad-price'}).text
                except:
                    price = 'No price'
                try:
                    addres = div.find(
                        'div', class_="css-u2ayx9").find('h6').text
                except:
                    addres = 'No address'
                try:
                    link = div.find('a').get('href')
                except:
                    link = 'No url'
                try:
                    area = div.find(
                        'p', {'data-testid': 'location-date'}).text.split('-')
                except:
                    area = 'No area'

                if link != 'No url':
                    data_olx.append(
                        {
                            "Цена": price,
                            "Район": area[0],
                            "Название": addres,
                            "Ссылка": f'https://www.olx.ua{link}',
                        }
                    )

                # если количество объявлений больше 8 - прерываем цикл
                if len(data_olx) == 8:
                    break

        # ответ с olx
        if isinstance(data_olx, list):
            for item in data_olx:
                card = f'{hlink(item.get("Название"), item.get("Ссылка"))}\n' \
                    f'{hbold("Цена: ")}{item.get("Цена")}\n' \
                    f'{hbold("Район: ")}{item.get("Район")}'

                await message.answer(card)
        time.sleep(2)
    except:
        logging.error('call_data_olx', exc_info=True)
        await message.answer('Не удалось соединиться с OLX')
