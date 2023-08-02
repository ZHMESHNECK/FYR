from utils.db.registration import check_register, show_parametrs
from utils.db.schemas.temporary_storage import temp_reg
from utils.rieltor_par import call_data_rieltor
from utils.country_par import call_data_country
from utils.db.reg_commands import update_time
from aiogram.dispatcher.filters import Text
from datetime import datetime, timedelta
from utils.olx_par import call_data_olx
from aiogram import types, executor
from utils.keyboards import *
from config import dp
import time


# OSError: [WinError 64] Указанное сетевое имя более недоступно
# asyncpg.exceptions.ConnectionDoesNotExistError: connection was closed in the middle of operation
# aiogram.utils.exceptions.BadRequest: Unsupported parse_mode

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Приветствую!\nначать поиск?', reply_markup=keyboard)


@dp.message_handler(commands='help')
async def help(message: types.Message):
    await message.answer_photo(open(r'media\screen\presentation.png', 'rb'), caption='Приветсвую, я твой помошник с поиском аренды жилья,\nя ищу объявления на rieltor.ua | olx.ua | country.ua\nдавай я расскажу тебе что я умею')
    time.sleep(1)
    await message.answer_photo(open(r'media\screen\registration.png', 'rb'), caption='Для начала тебе нужно пройти регистрацию, я тебе сам её предложу в самом начале.\nИспользуй подсказки на клавиатуре\nТакже большинство параметров можно не указывать, для этого, снизу клавиатуры есть кнопка "Пропуск"')
    time.sleep(1)
    await message.answer_photo(open(r'media\screen\af_registration.png', 'rb'), caption='После регистрации вам будет доступно 2 кнопки: кнопка "искать" - сразу начнёт поиск з заданныим параметрами')
    time.sleep(1)
    await message.answer_photo(open(r'media\screen\params.png', 'rb'), caption='При нажатии кнопки "параметры" вы увидите ваши сохраненные настройки,\nа также вы сможете изменить их нажав на "Изменить параметр" и следуя инструкциям')


@dp.message_handler(Text(equals='🛠 параметры 🛠'))
async def settings(message: types.Message):
    user = await check_register(message)
    if user:
        await show_parametrs(message, user[0])


@dp.message_handler(Text(equals='🔎 Искать 🔍'))
async def search(message: types.Message):

    # Достаём параметры из БД
    user_param = await check_register(message)

    # user_param[0] - параметры пользователя
    # user_param[1] - если есть бан то значение int иначе None
    if user_param is not None:
        if isinstance(user_param[1], int):
            await message.answer(f'Запрос можно отправить только раз в минуту для предотвращения спама\nосталось <b>{user_param[1]}</b> секунд')
        elif user_param[0] is not None:
            await update_time(message.from_user.id, datetime.now()+timedelta(minutes=1))

            # await message.answer('Начинаю поиск на 🔑 Rieltor 🔑\n⬇️')

            # запуск функции для RIELTOR
            # await call_data_rieltor(message, user_param[0])

            # await message.answer('Начинаю поиск на 📦 OLX 📦\n⬇️')

            # запуск функции для OLX
            # await call_data_olx(message, user_param[0])

            await message.answer('Начинаю поиск на 🏠 country 🏠\n⬇️')

            # запуск функции для country
            await call_data_country(message, user_param[0])


@dp.message_handler(Text(equals='Изменить параметр'))
async def change_parametrs(message: types.Message):
    await message.answer('Выбирите что меняем:', reply_markup=change_board)
    await temp_reg.choice_param.set()


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
