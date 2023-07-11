from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import environ

env = environ.Env()

class reg(StatesGroup):
    rooms = State()
    price_min = State()
    price_max = State()
    mn_floor = State()
    mx_floor = State()
    city = State()
    sort = State()


bot = Bot(env("TOKEN"),
          parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def settings(message: types.Message):
    try:
        conn = psycopg2.connect(host="localhost", port=5432,
                                dbname="FYR", user="postgres", password="qwerty123")
        conn.autocommit = True
        print("Database opened successfully")
        with conn.cursor() as curs:
            curs.execute("SELECT id FROM users WHERE id=%s",
                         (f'{message.from_user.id}',))
            if len(curs.fetchall()) == 0:
                await bot.send_message(message.from_user.id, 'Добро пожаловать\nперед использованием бота нужно задать параметры поиска, используйте команду /register')
        conn.close()
    except Exception:
        await bot.send_message(message.from_user.id, 'Не удалось соединиться с базой')


@dp.message_handler(commands=['register'])
async def register(message: types.Message):
    await bot.send_message(message.from_user.id, 'Для начала введите город в котором искать')
    await reg.city.set()


@dp.message_handler(state=reg.city)
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
        await state.update_data(city='')
        await bot.send_message(message.from_user.id, f'Окей, буду искать в городе по умолчанию\nУкажите пожалуйста, <b>от</b> какой суммы искать', reply_markup=price_key)
        await reg.price_min.set()
    else:
        await state.update_data(city=message.text)
        await bot.send_message(message.from_user.id, f'Принял, буду искать в городе <b>{message.text}</b>\nУкажите <b>от</b> какой суммы искать', reply_markup=price_key)
        await reg.price_min.set()


@dp.message_handler(state=reg.price_min)
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
            await bot.send_message(message.from_user.id, 'Окей, начальная цена не важна.\nУкажите <b>до</b> какой суммы искать', reply_markup=price_m_key)
            await state.update_data(price_min='')
            await reg.price_max.set()
        else:
            if message.text.isnumeric():
                if int(message.text) < 2000 or int(message.text) > 50000:
                    await bot.send_message(message.from_user.id, 'Ошибка\nЧисло выходит из допустимого диапазона')
                else:
                    await state.update_data(price_min=int(message.text))
                    await bot.send_message(message.from_user.id, f'Принял, буду искать от <b>{message.text}</b> грн\nУкажите <b>до</b> какой суммы искать', reply_markup=price_m_key)
                    await reg.price_max.set()
            else:
                await bot.send_message(message.from_user.id, 'Ошибка\nВведенно не число')
    except Exception:
        await bot.send_message(message.from_user.id, 'Ошибка\nВведены не корректные данные')


@dp.message_handler(state=reg.price_max)
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
            await bot.send_message(message.from_user.id, 'Окей, конечная цена не важна.\nУкажите количество комнат', reply_markup=room_key)
            await state.update_data(price_max='')
            await reg.rooms.set()
        else:
            if message.text.isnumeric():
                if int(message.text) < 2000 and int(message.text) > 60000:
                    await bot.send_message(message.from_user.id, 'Ошибка\nЧисла выходит из допустимого диапазона')
                else:
                    await state.update_data(price_max=int(message.text))
                    await bot.send_message(message.from_user.id, f'Принял, буду искать кваритиры до <b>{message.text}</b> грн\nУкажите количество комнат', reply_markup=room_key)
                    await reg.rooms.set()
            else:
                await bot.send_message(message.from_user.id, 'Ошибка\nВведенно не число')
    except Exception:
        await bot.send_message(message.from_user.id, 'Ошибка\nВведены не корректные данные')


@dp.message_handler(state=reg.rooms)
async def get_c_rooms(message: types.Message, state: FSMContext):
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

            await bot.send_message(message.from_user.id, 'Окей, количество комнат не важно.\nУкажите <b>с</b> какого этажа искать квартиру воспользовавшись клавиатурой или введя вручную но не выше <b>20</b> этажа', reply_markup=floor_n_key)
            await state.update_data(rooms='')
            await reg.mn_floor.set()
        else:
            mes = message.text.replace('-', '')
            if message.text.isnumeric():
                if len(message.text) in (1, 2) and int(message.text) < 14:
                    await state.update_data(rooms=int(mes))
                    await bot.send_message(message.from_user.id, f'Принял, буду искать {message.text}-х комнатую квартиру\nУкажите <b>с</b> какого этажа искать квартиру воспользовавшись клавиатурой или введя вручную но не выше <b>20</b> этажа', reply_markup=floor_n_key)
                    await reg.mn_floor.set()
                else:
                    await bot.send_message(message.from_user.id, 'число выходит из диапазона допустимых')
            else:
                await bot.send_message(message.from_user.id, 'не удалось распознать число')
    except:
        await bot.send_message(message.from_user.id, 'Произошла ошибка при вводе количества комнат')


@dp.message_handler(state=reg.mn_floor)
async def get_mn_floor(message: types.Message, state: FSMContext):
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
            await bot.send_message(message.from_user.id, 'Окей, с какого этажа искать не важно.\nУкажите <b>до</b> какого этажа искать квартиру',reply_markup=floor_x_key)
            await state.update_data(mn_floor='')
            await reg.mx_floor.set()
        else:
            if message.text.isnumeric() and int(message.text) <= 20:
                await state.update_data(mn_floor=int(message.text))
                await bot.send_message(message.from_user.id, f'Принял, буду искать с {message.text} этажа.\nУкажите <b>до</b> какого этажа искать квартиру',reply_markup=floor_x_key)
                await reg.mx_floor.set()
            else:
                await bot.send_message(message.from_user.id, 'не удалось распознать этаж\n укажите этаж от 1 до 20 включительно')
    except:
        await bot.send_message(message.from_user.id, 'Произошла ошибка при вводе этажа')


@dp.message_handler(state=reg.mx_floor)
async def get_mx_floor(message: types.Message, state: FSMContext):
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
            await bot.send_message(message.from_user.id, 'Окей, <b>до</b> какого этажа искать не важно.\nУкажите сортировку объявлений', reply_markup=sort_key)
            await state.update_data(mx_floor='')
            await reg.sort.set()
        else:
            if message.text.isnumeric() and int(message.text) <= 20:
                await state.update_data(mx_floor=int(message.text))
                await bot.send_message(message.from_user.id, f'Принял, буду искать до {message.text} этажа.\nУкажите сортировку объявлений', reply_markup=sort_key)
                await reg.sort.set()
            else:
                await bot.send_message(message.from_user.id, 'не удалось распознать этаж\n укажите этаж от 1 до 20 включительно')
    except:
        await bot.send_message(message.from_user.id, 'Произошла ошибка при вводе этажа')


@dp.message_handler(state=reg.sort)
async def get_sort(message: types.Message, state: FSMContext):
    try:
        if message.text == 'Пропуск':
            await bot.send_message(message.from_user.id, 'Окей, сортировка будет по стандарту\nСпасибо за регистрацию!')
            await state.update_data(sort='')
        elif message.text in ('Новинки', 'Дешёвые', 'Дорогие'):
            await state.update_data(mx_floor=message.text)
            await bot.send_message(message.from_user.id, f'Принял, буду искать по {message.text}.\nСпасибо за регистрацию!')
        da = await state.get_data()
        print(da)
        await state.finish()
    except:
        await bot.send_message(message.from_user.id, 'Произошла ошибка при вводе сортировки')


executor.start_polling(dp, skip_updates=True)
