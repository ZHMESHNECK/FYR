from utils.db.registration import check_register
from states.temporary_storage import temp_reg
from aiogram.dispatcher.filters import Text
from rieltor_par import call_data_rieltor
from country_par import call_data_country
from aiogram import types, executor
from olx_par import call_data_olx
from keyboards import *
from config import dp

# https://www.youtube.com/watch?v=rgmehqKzWO0
# https://www.youtube.com/watch?v=dcbuQMjHj_c&t=240s
# https://pythonru.com/biblioteki/shemy-v-sqlalchemy-orm


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Приветствую!\nначать поиск?', reply_markup=keyboard)


@dp.message_handler(Text(equals='🛠 параметры 🛠'))
async def settings(message: types.Message):
    await check_register(message)


@dp.message_handler(Text(equals='🔎 Искать 🔍'))
async def search(message: types.Message):

    await message.answer('Начинаю поиск на 🔑 Rieltor 🔑')

    # ## запуск функции для RIELTOR
    # await call_data_rieltor(message)

    await message.answer('Начинаю поиск на 📦 OLX 📦')

    # ## запуск функции для OLX
    # await call_data_olx(message)

    await message.answer('Начинаю поиск на 🏠 country 🏠')

    # запуск функции для country
    # await call_data_country(message)


@dp.message_handler(Text(equals='Изменить параметр'))
async def change_parametrs(message: types.Message):
    await message.answer('Выбирите что меняем:', reply_markup=change_board)
    await temp_reg.choice_param.set()

def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
