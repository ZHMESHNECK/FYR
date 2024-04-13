from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
import platform
import environ
import logging
import os

env = environ.Env()
env.read_env('.env')

osp = platform.platform()

logging.basicConfig(level=logging.WARNING, filename='logs.log',
                    filemode='w', format="%(asctime)s %(levelname)s %(message)s")

fake_user = ['Mozilla/5.0 (Macintosh; U; PPC Mac OS X; nl-nl) AppleWebKit/417.9 (KHTML, '
             'like Gecko) Safari/417.8',
             'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.10) Gecko/20050720 '
             'Fedora/1.0.6-1.1.fc3 Firefox/1.0.6',
             'Mozilla/5.0 (Windows; U; Windows NT 5.1; fr-FR; rv:1.7.6) Gecko/20050318 '
             'Firefox/1.0.2',
             'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.5.1 (KHTML, '
             'like Gecko) Safari/312.3.1',
             'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; fr-fr) AppleWebKit/312.5 (KHTML, '
             'like Gecko) Safari/312.3']


city = {
    'Киев': ['kiev', 'kiev', '29586'],
    'Одесса': ['odessa', 'odessa', '29585'],
    'Львов': ['lvov', 'lvov', None],
    'Днепр': ['dnepr', 'dnepr', '29587'],
    'Харьков': ['kharkov', 'harkov', '29588'],
    'Запорожье': ['zaporozhe', 'zaporozhje', '29595'],
    'Чернигов': ['chernigov', 'chernigov', None],
    'Черкасы': ['cherkassy', 'cherkassy', None],
    'Ужгород': ['uzhgorod', 'uzhgorod', None]
}

sort = {
    'Новинки': ['created_at:desc', 'bycreated', 'date'],
    'Дешёвые': ['filter_float_price:asc', 'byprice', 'nedorogo'],
    'Дорогие': ['filter_float_price:desc', '-byprice', 'elit'],
    'Пропуск': ['', '', 'default']
}

rielt_room = ['1-room', '2-rooms', '3-rooms']
rielt_rooms = ['rooms[0]=1', 'rooms[1]=2', 'rooms[2]=3']

country_rooms = {'1,2': '1%2C2', '1,3': '1%2C3',
                 '2,3': '2%2C3', '1,2,3': '1%2C2%2C3'}


da = os.getenv('POSTGRES_HOST')
host = env('POSTGRES_HOST')
port = env('POSTGRES_PORT')
db = env('POSTGRES_DB')
user = env('POSTGRES_USER')
password = env('POSTGRES_PASSWORD')

POSTGRES_URI = f'postgresql://{user}:{password}@{host}:{port}/{db}'


bot = Bot(token=env('TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

help_win = [
    r'bot\media\screen\presentation.png',
    r'bot\media\screen\registration.png',
    r'bot\media\screen\af_registration.png',
    r'bot\media\screen\params.png',
]
help_lin = [
    r'bot/media/screen/presentation.png',
    r'bot/media/screen/registration.png',
    r'bot/media/screen/af_registration.png',
    r'bot/media/screen/params.png',
]
