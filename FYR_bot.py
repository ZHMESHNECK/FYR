from utils.db.registration import check_register, show_parametrs
from utils.db.schemas.temporary_storage import temp_reg
from utils.rieltor_par import call_data_rieltor
from utils.country_par import call_data_country
from aiogram.dispatcher.filters import Text
from utils.olx_par import call_data_olx
from aiogram import types, executor
from utils.keyboards import *
from config import dp
import time


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Приветствую!\nначать поиск?', reply_markup=keyboard)


@dp.message_handler(commands='help')
async def help(message: types.Message):
    await message.answer_photo(open(r'media\screen\presentation.png', 'rb'), caption='Приветсвую, я твой помошник с поиском аренды жилья,\nя ищу объявления на rieltor.ua | olx.ua | country.ua\nдавай я расскажу тебе что я умею')
    time.sleep(1)
    await message.answer_photo(open(r'media\screen\registration.png', 'rb'), caption='Для начала тебе нужно пройти регистрацию, я тебе сам её предложу в самом начале.\nИспользуй подсказки на клавиатуре')
    time.sleep(1)
    await message.answer_photo(open(r'media\screen\af_registration.png', 'rb'), caption='После регистрации вам будет доступно 2 кнопки: "искать" - сразу начнёт поиск з заданныим параметрами')
    time.sleep(1)
    await message.answer_photo(open(r'media\screen\params.png', 'rb'), caption='При нажатии кнопки "параметры" вы увидите ваши сохраненные настройки,\nа также вы сможете изменить их нажав на "Изменить параметр" и следуя инструкциям')


@dp.message_handler(Text(equals='🛠 параметры 🛠'))
async def settings(message: types.Message):
    user = await check_register(message)
    if user:
        await show_parametrs(message, user)


@dp.message_handler(Text(equals='🔎 Искать 🔍'))
async def search(message: types.Message):

    # Достаём параметры из БД
    user_param = await check_register(message)
    if isinstance(user_param, int):
        await message.answer(f'Запрос можно отправить только раз в минуту для предотвращения спама\nосталось <b>{user_param}</b> секунд')
    elif user_param is not None:

        await message.answer('Начинаю поиск на 🔑 Rieltor 🔑')

        # запуск функции для RIELTOR
        await call_data_rieltor(message, user_param)

        await message.answer('Начинаю поиск на 📦 OLX 📦')

        # запуск функции для OLX
        await call_data_olx(message, user_param)

        await message.answer('Начинаю поиск на 🏠 country 🏠')

        # запуск функции для country
        await call_data_country(message, user_param)


@dp.message_handler(Text(equals='Изменить параметр'))
async def change_parametrs(message: types.Message):
    await message.answer('Выбирите что меняем:', reply_markup=change_board)
    await temp_reg.choice_param.set()


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
