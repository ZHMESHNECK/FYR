from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from main import call_data_rieltor,call_data_olx
from aiogram.utils.markdown import hbold, hlink
import environ
import json
import time
env = environ.Env()
env.read_env('.env')

bot = Bot(token=env('TOKEN'),parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['🔎 Искать 🔍']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Что именно искать', reply_markup=keyboard)

@dp.message_handler(Text(equals='🔎 Искать 🔍'))
async def search(message: types.Message):
    await message.answer('Начинаю поиск...')

    data_rieltor=call_data_rieltor()
    data_olx=call_data_olx()

    ## СМС с rieltor
    for index, item in enumerate(data_rieltor):
        card = f'{hlink(item.get("Название"), item.get("Ссылка"))}\n' \
        f'{hbold("Цена: ")}{item.get("Цена")}\n' \
        f'{hbold("Название: ")}{item.get("Название")}'
        
        if index%10 == 0:
            time.sleep(3)

        await message.answer(card)

def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()