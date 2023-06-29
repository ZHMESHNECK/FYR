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
    
    ## запуск функции для RIELTOR
    await message.answer('Начинаю поиск на 🔑 Rieltor 🔑')
    data_rieltor=call_data_rieltor()

    ## ответ с rieltor
    for index, item in enumerate(data_rieltor):
        card = f'{hlink(item.get("Адрес"), item.get("Ссылка"))}\n' \
        f'{hbold("Цена: ")}{item.get("Цена")}\n' \
        f'{hbold("Район: ")}{item.get("Район")}'
        
        if index%10 == 0:
            time.sleep(3)

        await message.answer(card)
    time.sleep(2)


    ## запуск функции для OLX
    await message.answer('Начинаю поиск на 📦 OLX 📦')

    data_olx=call_data_olx()

    if data_olx == 'Old version':
        for num, _ in enumerate(range(2),2):
            if data_olx == 'Old version':
                await message.answer(f'Попытка соединения с OLX №{num}')
                time.sleep(5)
                data_olx=call_data_olx()


    ## ответ с olx
    if isinstance(data_olx,list):
        for index, item in enumerate(data_olx):
            card = f'{hlink(item.get("Название"), item.get("Ссылка"))}\n' \
            f'{hbold("Цена: ")}{item.get("Цена")}\n' \
            f'{hbold("Район: ")}{item.get("Район")}'
            
            if index%10 == 0:
                time.sleep(3)

            await message.answer(card)
    else:
        await message.answer('Не удалось соединиться с OLX')


def main():
    executor.start_polling(dp,skip_updates=True)

if __name__ == '__main__':
    main()