from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
import environ

env = environ.Env()
env.read_env('.env')


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
    'Дешёвые': ['asc', 'byprice', 'nedorogo'],
    'Дорогие': ['desc', '-byprice', 'elit'],
    'Пропуск': ['', '', 'default']
}

rielt_room = ['1-room', '2-rooms', '3-rooms']
rielt_rooms = ['rooms[0]=1', 'rooms[1]=2', 'rooms[2]=3']

country_rooms ={'1,2': '1%2C2', '1,3': '1%2C3', '2,3': '2%2C3', '1,2,3': '1%2C2%2C3'}

host = env('POSTGRES_HOST')
port = env('POSTGRES_PORT')
db = env('POSTGRES_DB')
user = env('POSTGRES_USER')
password = env('POSTGRES_PASSWORD')

POSTGRES_URI = f'postgresql://{user}:{password}@{host}/{db}'


bot = Bot(token=env('TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
