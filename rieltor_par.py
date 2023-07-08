from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests


# заготовка под генерацию ссылки с параметрами
"""
from bs4 import BeautifulSoup
with open('rieltor.html', 'r', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')


room = ['1-room', '2-rooms', '3-rooms', '4-rooms']
rooms = ['rooms[0]=1', 'rooms[1]=2', 'rooms[2]=3']
city = [i.attrs['data-index-url']
        for i in soup.find_all('div', class_='nav_item_option_geo_city js_nav_input')] # взять города из config


parametrs = {
    'rooms': room[0],
    'price_min': 'price_min=4000',
    'price_max': '&price_max=9000',
    'city': city[0],
    'floor_min': '',
    'floor_max': '',
    'sort': 'byprice'
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

if len(roomes) == 1:
    parametrs['rooms'] = room[roomes[0]-1] + '/?'
else:
    list_of_room = []
    for i in roomes:
        list_of_room.append(rooms[i-1])

    parametrs['rooms'] = '?' + '&'.join(list_of_room) + '&'

if mn_price != 0:
    parametrs['price_min'] = f'price_min={mn_price}'
if mx_price != 0:
    parametrs['price_max'] = f'&price_max={mx_price}'

if mn_floor != 0:
    parametrs['floor_min'] = f'&floor_min={mn_floor}'
if mx_floor != 0:
    parametrs['floor_max'] = f'&floor_max={mx_floor}'

gen_of_link = f'{parametrs["rooms"]}{parametrs["price_min"]}{parametrs["price_max"]}{parametrs["floor_min"]}{parametrs["floor_max"]}&sort={parametrs["sort"]}'


link = f'https://rieltor.ua{parametrs["city"]}flats-rent/{gen_of_link}'

print('https://rieltor.ua/kiev/flats-rent/2-rooms/?price_min=4000&price_max=9000&sort=byprice')
print(
    'https://rieltor.ua/kiev/flats-rent/?rooms[0]=1&rooms[1]=2&price_min=4000&price_max=9000&sort=byprice')
print(
    'https://rieltor.ua/rovno/flats-rent/?price_min=4000&price_max=9000&sort=-default&floor_min=6&floor_max=9&rooms[0]=1&rooms[1]=2')
print(link)
"""

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
