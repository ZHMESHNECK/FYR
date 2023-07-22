from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
import environ

env = environ.Env()
env.read_env('.env')


city = {
    'Киев': ['kiev', 'kiev', 'flat'],
    'Одесса': ['odessa', 'odessa', 'odesa'],
    'Львов': ['lvov', 'lvov', None],
    'Днепр': ['dnepr', 'dnepr', 'dnipro'],
    'Харьков': ['kharkov', 'harkov', 'harkiv'],
    'Запорожье': ['zaporozhe', 'zaporozhje', 'zaporijjya'],
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

host = env('POSTGRES_HOST')
port = env('POSTGRES_PORT')
db = env('POSTGRES_DB')
user = env('POSTGRES_USER')
password = env('POSTGRES_PASSWORD')

POSTGRES_URI = f'postgresql://{user}:{password}@{host}/{db}'


bot = Bot(token=env('TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
