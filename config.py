import environ
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

env = environ.Env()
env.read_env('.env')
city = ['/kiev/', '/odessa/', '/dnepr/', '/lvov/', '/harkov/', '/ivano-frankovsk/', '/hmelnitskij/', '/sumy/', '/nikolaev/', '/zaporozhje/', '/rovno/',
                  '/chernigov/', '/vinnitsa/', '/chernovtsy/', '/ternopol/', '/poltava/', '/cherkassy/', '/zhitomir/', '/skyi/', 'kropyvnytskyi/', '/uzhgorod/', '/lutsk/', '/kherson/']


host = env('POSTGRES_HOST')
port = env('POSTGRES_PORT')
db = env('POSTGRES_DB')
user = env('POSTGRES_USER')
password = env('POSTGRES_PASSWORD')

POSTGRES_URI = f'postgresql://{user}:{password}@{host}/{db}'


bot = Bot(token=env('TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
