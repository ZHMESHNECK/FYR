from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.db.reg_commands import select_user, add_user
from aiogram.dispatcher import FSMContext
from config import POSTGRES_URI
from utils.db.dbb import db
from aiogram import types
from config import dp
from states.register import registration
import traceback


async def check_register(message: types.Message):
    # try:
    await db.set_bind(POSTGRES_URI)
    check_user = await select_user(message.from_user.id)
    print(f'check_user {check_user}')
    if not check_user:
        await start_reg(message)
    else:
        await message.answer('Вы уже зарегистрированы')
    # except:
    #     await message.answer('Не удалось подключиться к базе данных')


async def start_reg(message: types.Message):
    await message.answer('Для начала введите город в котором искать')
    await registration.city.set()


@dp.message_handler(state=registration.city)
async def get_city(message: types.Message, state: FSMContext):
    # добавить проверку на существующий город (config)
    price_key = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='3000'), KeyboardButton(text='4000')
            ],
            [
                KeyboardButton(text='5000'), KeyboardButton(text='6000')
            ],
            [
                KeyboardButton(text='7000'), KeyboardButton(text='8000')
            ],
            [
                KeyboardButton(text='Пропуск')
            ]
        ],
        resize_keyboard=True,
    )
    if message.text == 'Пропуск':
        await state.update_data(city=None)
        await message.answer(f'Окей, буду искать в городе по умолчанию\nУкажите пожалуйста, <b>от</b> какой суммы искать', reply_markup=price_key)
        await registration.min_price.set()
    else:
        await state.update_data(city=message.text)
        await message.answer(f'Принял, буду искать в городе <b>{message.text}</b>\nУкажите <b>от</b> какой суммы искать', reply_markup=price_key)
        await registration.min_price.set()


@dp.message_handler(state=registration.min_price)
async def get_min_price(message: types.Message, state: FSMContext):
    price_m_key = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='6000'), KeyboardButton(text='7000')
            ],
            [
                KeyboardButton(text='8000'), KeyboardButton(text='9000')
            ],
            [
                KeyboardButton(text='10.000'), KeyboardButton(text='11.000')
            ],
            [
                KeyboardButton(text='Пропуск')
            ]
        ],
        resize_keyboard=True
    )
    try:
        if message.text == 'Пропуск':
            await message.answer('Окей, начальная цена не важна.\nУкажите <b>до</b> какой суммы искать', reply_markup=price_m_key)
            await state.update_data(min_price=None)
            await registration.max_price.set()
        else:
            if message.text.isnumeric():
                if int(message.text) < 2000 or int(message.text) > 50000:
                    await message.answer('Ошибка\nЧисло выходит из допустимого диапазона')
                else:
                    await state.update_data(min_price=int(message.text))
                    await message.answer(f'Принял, буду искать от <b>{message.text}</b> грн\nУкажите <b>до</b> какой суммы искать', reply_markup=price_m_key)
                    await registration.max_price.set()
            else:
                await message.answer('Ошибка\nВведенно не число')
    except Exception:
        await message.answer('Ошибка\nВведены не корректные данные')


@dp.message_handler(state=registration.max_price)
async def get_max_price(message: types.Message, state: FSMContext):
    room_key = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='1'), KeyboardButton(text='1-2')
            ],
            [
                KeyboardButton(text='2'), KeyboardButton(text='1-3')
            ],
            [
                KeyboardButton(text='3'), KeyboardButton(text='2-3')
            ],
            [
                KeyboardButton(text='Пропуск')
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    try:
        if message.text == 'Пропуск':
            await message.answer('Окей, конечная цена не важна.\nУкажите количество комнат', reply_markup=room_key)
            await state.update_data(max_price=None)
            await registration.count_rooms.set()
        else:
            if message.text.isnumeric():
                if int(message.text) < 2000 and int(message.text) > 60000:
                    await message.answer('Ошибка\nЧисла выходит из допустимого диапазона')
                else:
                    await state.update_data(max_price=int(message.text))
                    await message.answer(f'Принял, буду искать кваритиры до <b>{message.text}</b> грн\nУкажите количество комнат', reply_markup=room_key)
                    await registration.count_rooms.set()
            else:
                await message.answer('Ошибка\nВведенно не число')
    except Exception:
        await message.answer('Ошибка\nВведены не корректные данные')


@dp.message_handler(state=registration.count_rooms)
async def get_c_count_rooms(message: types.Message, state: FSMContext):
    floor_n_key = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='1'), KeyboardButton(text='2')
            ],
            [
                KeyboardButton(text='3'), KeyboardButton(text='4')
            ],
            [
                KeyboardButton(text='5'), KeyboardButton(text='6')
            ],
            [
                KeyboardButton(text='7'), KeyboardButton(text='8')
            ],
            [
                KeyboardButton(text='Пропуск')
            ]
        ],
        resize_keyboard=True,
    )
    try:
        if message.text == 'Пропуск':

            await message.answer('Окей, количество комнат не важно.\nУкажите <b>с</b> какого этажа искать квартиру воспользовавшись клавиатурой или введя вручную но не выше <b>20</b> этажа', reply_markup=floor_n_key)
            await state.update_data(count_rooms=None)
            await registration.min_floor.set()
        else:
            mes = message.text.replace('-', '')
            if message.text.isnumeric():
                if len(message.text) in (1, 2) and int(message.text) < 14:
                    await state.update_data(count_rooms=int(mes))
                    await message.answer(f'Принял, буду искать {message.text}-х комнатую квартиру\nУкажите <b>с</b> какого этажа искать квартиру воспользовавшись клавиатурой или введя вручную но не выше <b>20</b> этажа', reply_markup=floor_n_key)
                    await registration.min_floor.set()
                else:
                    await message.answer('число выходит из диапазона допустимых')
            else:
                await message.answer('не удалось распознать число')
    except:
        await message.answer('Произошла ошибка при вводе количества комнат')


@dp.message_handler(state=registration.min_floor)
async def get_min_floor(message: types.Message, state: FSMContext):
    floor_x_key = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='1'), KeyboardButton(text='2')
            ],
            [
                KeyboardButton(text='3'), KeyboardButton(text='4')
            ],
            [
                KeyboardButton(text='5'), KeyboardButton(text='6')
            ],
            [
                KeyboardButton(text='7'), KeyboardButton(text='8')
            ],
            [
                KeyboardButton(text='Пропуск')
            ]
        ],
        resize_keyboard=True,
    )
    try:
        if message.text == 'Пропуск':
            await message.answer('Окей, с какого этажа искать не важно.\nУкажите <b>до</b> какого этажа искать квартиру', reply_markup=floor_x_key)
            await state.update_data(min_floor=None)
            await registration.max_floor.set()
        else:
            if message.text.isnumeric() and int(message.text) <= 20:
                await state.update_data(min_floor=int(message.text))
                await message.answer(f'Принял, буду искать с {message.text} этажа.\nУкажите <b>до</b> какого этажа искать квартиру', reply_markup=floor_x_key)
                await registration.max_floor.set()
            else:
                await message.answer('не удалось распознать этаж\n укажите этаж от 1 до 20 включительно')
    except:
        await message.answer('Произошла ошибка при вводе этажа')


@dp.message_handler(state=registration.max_floor)
async def get_max_floor(message: types.Message, state: FSMContext):
    sort_key = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Новинки')
            ],
            [
                KeyboardButton(text='Дешёвые')
            ],
            [
                KeyboardButton(text='Дорогие')
            ],
            [
                KeyboardButton(text='Пропуск')
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    try:
        if message.text == 'Пропуск':
            await message.answer('Окей, <b>до</b> какого этажа искать не важно.\nУкажите сортировку объявлений', reply_markup=sort_key)
            await state.update_data(max_floor=None)
            await registration.sort.set()
        else:
            if message.text.isnumeric() and int(message.text) <= 20:
                await state.update_data(max_floor=int(message.text))
                await message.answer(f'Принял, буду искать до {message.text} этажа.\nУкажите сортировку объявлений', reply_markup=sort_key)
                await registration.sort.set()
            else:
                await message.answer('не удалось распознать этаж\n укажите этаж от 1 до 20 включительно')
    except:
        await message.answer('Произошла ошибка при вводе этажа')


@dp.message_handler(state=registration.sort)
async def get_sort(message: types.Message, state: FSMContext):
    start_buttons = ['🔎 Искать 🔍', '🛠 регистрация 🛠']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    try:
        if message.text == 'Пропуск':
            await message.answer('Окей, сортировка будет по стандарту', reply_markup=keyboard)
            await state.update_data(sort=None)
        elif message.text in ('Новинки', 'Дешёвые', 'Дорогие'):
            await state.update_data(max_floor=message.text)
            await message.answer(f'Принял, буду искать по {message.text}')
        await state.finish()
        da = await state.get_data()
        if await add_user(message.from_user.id, da.get('city'), da.get('min_price'), da.get('max_price'), da.get('count_rooms'), da.get('min_floor'), da.get('max_floor'), da.get('sort')):
            await message.answer('Вы успешно зарегистрировались', reply_markup=keyboard)
        else:
            await message.answer('Произошла ошибка при сохранении данных', reply_markup=keyboard)

    except Exception:
        await message.answer('Произошла ошибка при вводе сортировки\n', traceback.format_exc())
