from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from olx_par import call_data_olx
from rieltor_par import call_data_rieltor
from country_par import call_data_country
from aiogram.utils.markdown import hbold, hlink
import environ
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
    
    # await message.answer('Начинаю поиск на 🔑 Rieltor 🔑')

    # ## запуск функции для RIELTOR
    # data_rieltor=call_data_rieltor()

    # if data_rieltor != 'error':

    #     ## ответ с rieltor
    #     for index, item in enumerate(data_rieltor):
    #         card = f'{hlink(item.get("Адрес"), item.get("Ссылка"))}\n' \
    #         f'{hbold("Цена: ")}{item.get("Цена")}\n' \
    #         f'{hbold("Район: ")}{item.get("Район")}'
            
    #         if index%10 == 0:
    #             time.sleep(3)

    #         await message.answer(card)
    #     time.sleep(2)
    # else:
    #     await message.answer('Не удалось соединиться с rieltor.ua')


    # await message.answer('Начинаю поиск на 📦 OLX 📦')

    # ## запуск функции для OLX
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

    
    await message.answer('Начинаю поиск на 🏠 country 🏠')

    ## запуск функции для country
    # data_country=call_data_country()

    # if data_country != 'error':

    #     ## ответ с country
    #     for index, item in enumerate(data_country):
    #         card = f'{hlink(item.get("Адрес"), item.get("Ссылка"))}\n' \
    #         f'{hbold("Цена: ")}{item.get("Цена")}\n'
            
    #         if index%10 == 0:
    #             time.sleep(3)

    #         await message.answer(card)
    #     time.sleep(2)
    # else:
    #     await message.answer('Не удалось соединиться с country.ua')


def main():
    executor.start_polling(dp,skip_updates=True)

if __name__ == '__main__':
    main()