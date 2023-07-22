from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from aiogram.utils.markdown import hbold, hlink
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium import webdriver
from config import city, sort
from bs4 import BeautifulSoup
from aiogram import types
import time

# заготовка под генерацию ссылки с параметрами
"""
from bs4 import BeautifulSoup
with open('olx.html', 'r', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')


room = ['odnokomnatnye', 'dvuhkomnatnye', 'trehkomnatnye']
city = ['/kiev/', '/odessa/', '/dnepr/', '/lvov/', '/harkov/', '/ivano-frankovsk/', '/hmelnitskij/', '/sumy/', '/nikolaev/', '/zaporozhje/', '/rovno/',
                  '/chernigov/', '/vinnitsa/', '/chernovtsy/', '/ternopol/', '/poltava/', '/cherkassy/', '/zhitomir/', '/skyi/', 'kropyvnytskyi/', '/uzhgorod/', '/lutsk/', '/kherson/']
sorti = ['created_at:desc', 'asc', 'desc']

parametrs = {
    'rooms': '',
    'price_min': '',
    'price_max': '',
    'city': city[0],
    'floor_min': '',
    'floor_max': '',
    'sort': ''
}

roomes = []
c_room = int(input('Кол. комнат: '))
while c_room != 0:
    roomes.append(c_room)
    c_room = int(input('Кол. комнат: '))
roomes = list(set(roomes))
mn_price = int(input('Мин: '))
mx_price = int(input('Мах: '))
mn_floor = int(input('ЭМин: '))
mx_floor = int(input('Эmax: '))
sort = int(input(
    '0-без сорт\n1-найновіші\n2-найдешевші\n3-найдорожчі\n'))

parametrs['rooms'] = '&'.join(
    [f'search[filter_enum_number_of_rooms_string][{num}]={room[rom-1]}' for num, rom in enumerate(list(set(roomes)))])


if mn_price != 0:
    parametrs['price_min'] = f'&search[filter_float_price:from]={mn_price}'
if mx_price != 0:
    parametrs['price_max'] = f'&search[filter_float_price:to]={mx_price}'

if mn_floor != 0:
    parametrs['floor_min'] = f'&search[filter_float_floor:from]={mn_floor}'
if mx_floor != 0:
    parametrs['floor_max'] = f'&search[filter_float_floor:to]={mx_floor}'

if sort == 1:
    parametrs['sort'] = f'&search[order]={sorti[0]}'
elif sort != 0:
    parametrs['sort'] = f'&search[order]=filter_float_price:{sorti[sort-1]}'


gen_of_link = f'{parametrs["rooms"]}{parametrs["price_min"]}{parametrs["price_max"]}{parametrs["floor_min"]}{parametrs["floor_max"]}{parametrs["sort"]}'


link = f'https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir{parametrs["city"]}?{gen_of_link}'


# print(
#     'https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/kiev/?search[filter_enum_number_of_rooms_string][0]=dvuhkomnatnye&search[filter_enum_number_of_rooms_string][1]=trehkomnatnye')
# print(
#     'https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/kiev/?search[filter_float_price:from]=4000&search[filter_float_price:to]=9000')
# print(
#     'https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/kiev/?search[filter_float_floor:from]=2&search[filter_float_floor:to]=4')
# print('https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/kiev/?search[filter_enum_number_of_rooms_string][0]=dvuhkomnatnye&search[filter_enum_number_of_rooms_string][1]=trehkomnatnye&search[filter_float_price:from]=4000&search[filter_float_price:to]=9000&search[filter_float_floor:from]=2&search[filter_float_floor:to]=5&search[order]=filter_float_price:asc')
print(link)

"""


async def call_data_olx(message: types.Message, user_param):
    data_olx = await call_data_olx_2(message, user_param)
    if data_olx == 'Old version':
        for num, _ in enumerate(range(2), 2):
            if data_olx == 'Old version':
                await message.answer(f'Попытка соединения с OLX №{num}')
                time.sleep(5)
                data_olx = await call_data_olx_2(message, user_param)
    # ответ с olx
    if isinstance(data_olx, list):
        for index, item in enumerate(data_olx):
            card = f'{hlink(item.get("Название"), item.get("Ссылка"))}\n' \
                f'{hbold("Цена: ")}{item.get("Цена")}\n' \
                f'{hbold("Район: ")}{item.get("Район")}'

            if index % 10 == 0:
                time.sleep(3)

            await message.answer(card)
    else:
        await message.answer('Не удалось соединиться с OLX')


async def call_data_olx_2(message: types.Message, user_param):

    ua = UserAgent()
    options = Options()
    options.set_preference("general.useragent.override", f'{ua.random}')
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)

    room = ['odnokomnatnye', 'dvuhkomnatnye', 'trehkomnatnye']
    parametrs = {
        'rooms': "&".join([f'search[filter_enum_number_of_rooms_string][{num}]={room[int(rom)-1]}' for num, rom in enumerate(list(map(int, user_param.count_rooms.replace('-', ''))))]) if user_param.count_rooms is not None else "",
        'price_min': f'&search[filter_float_price:from]={user_param.min_price}' if user_param.min_price is not None else "",
        'price_max': f'&search[filter_float_price:to]={user_param.max_price}' if user_param.max_price is not None else "",
        'city': city[user_param.city][0],
        'floor_min': f'&search[filter_float_floor:from]={user_param.min_floor}' if user_param.min_floor is not None else "",
        'floor_max': f'&search[filter_float_floor:to]={user_param.max_floor}' if user_param.max_floor is not None else "",
        'sort': f'&search[order]=filter_float_price:{sort[user_param.sort][0]}' if user_param.sort is not None else sort['Пропуск'][0]
    }
    gen_of_link = f'{parametrs["rooms"]}{parametrs["price_min"]}{parametrs["price_max"]}{parametrs["floor_min"]}{parametrs["floor_max"]}{parametrs["sort"]}'

    url = f'https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/{parametrs["city"]}/?{gen_of_link}'

    # Читаем страницу olx
    try:
        driver.get(url=url)

        # проверка браузера на совместимость с сайтом
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "c-wrapper-inside")))
            return 'Old version'
        except:
            pass

    except Exception as _ex:
        print(_ex)
    finally:
        # ищем объявления
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # 8 объявлений без "рекламы"
        items_divs = soup.find_all('div', class_='css-1sw7q4x')[3:11]
        driver.close()
        driver.quit()

    data_olx = []
    for item in items_divs:
        try:
            price = item.find('p', class_='css-10b0gli er34gjf0').text
        except:
            price = 'No price'
        try:
            addres = item.find('div', class_="css-u2ayx9").find('h6').text
        except:
            addres = 'No address'
        try:
            link = item.find('a').get('href')
        except:
            link = 'no url'
        try:
            area = item.find('p', class_='css-veheph er34gjf0').text.split('-')
        except:
            area = 'No area'

        data_olx.append(
            {
                "Цена": price,
                "Район": area[0],
                "Название": addres,
                "Ссылка": f'https://www.olx.ua{link}',
            }
        )
    return data_olx
