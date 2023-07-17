from states.temporary_storage import registration, temp_reg
from aiogram.dispatcher import FSMContext
from utils.db.reg_commands import *
from config import POSTGRES_URI
from utils.db.dbb import db
from aiogram import types
from keyboards import *
from config import dp
import traceback


async def check_register(message: types.Message):
    try:
        await db.set_bind(POSTGRES_URI)
        user = await select_user(message.from_user.id)
        if not user:
            await message.answer('У вас ещё не заданных параметров\nдавайте пройдём маленькую регистрацию ☺️', reply_markup=city_key)
            await start_reg(message)
        else:
            await message.answer(f'🛠 Параметры 🛠:\n'
                                 f'\n<b>Город</b> - {user.city if user.city is not None else "Не указано"}\n'
                                 f'\n<b>Мин. цена</b> - {str(user.min_price) + " грн" if user.min_price is not None else "Не указано"}\n'
                                 f'\n<b>Макс. цена</b> - {str(user.max_price) + " грн" if user.max_price is not None else "Не указано"}\n'
                                 f'\n<b>Кол. комнат</b> - {user.count_rooms if user.count_rooms is not None else "Не указано"}\n'
                                 f'\n<b>Мин. этаж</b> - {user.min_floor if user.min_floor is not None else "Не указано"}\n'
                                 f'\n<b>Макс. этаж</b> - {user.max_floor if user.max_floor is not None else "Не указано"}\n'
                                 f'\n<b>Сортировка</b> - {user.sort if user.sort is not None else "Не указано"}\n', reply_markup=view_param)
    except:
        await message.answer('Не удалось подключиться к базе данных', traceback.format_exc())


async def start_reg(message: types.Message):
    await message.answer('Для начала введите город в котором искать', reply_markup=city_key)
    await registration.city.set()


@dp.message_handler(state=temp_reg.choice_param)
async def single_change(message: types.Message, state: FSMContext):
    user = await select_user(message.from_user.id)
    data = {'Город': 'city', 'Кол. комнат': 'count_rooms',
            'Мин. цена': 'min_price', 'Макс. цена': 'max_price', 'Мин. этаж': 'min_floor', 'Макс. этаж': 'max_floor', 'Сортировка': 'sort'}
    data_2 = {'city': [user.city, city_key],
              'min_price': [user.min_price, price_key],
              'max_price': [user.max_price, price_m_key],
              'count_rooms': [user.count_rooms, room_key],
              'min_floor': [user.min_floor, floor_n_key],
              'max_floor': [user.max_floor, floor_x_key],
              'sort': [user.sort, sort_key]}
    param = data.get(message.text)
    print(f'param {param}')

    if param:
        await message.answer(f'Меняем {message.text} - <b>{data_2[param][0]}</b> на:', reply_markup=data_2[param][1])
        await state.update_data(choice_param=param)
        await temp_reg.param.set()

# добавить проверку города


@dp.message_handler(state=temp_reg.param)
async def single_change_2(message: types.Message, state: FSMContext):
    await state.update_data(param=message.text)
    print(f'dads {message.text}')
    data = await state.get_data()
    print(f'data {data}')
    if data['choice_param'] == 'city':
        await update_user_c(message.from_user.id, data['param'])
    elif data['choice_param'] == 'min_price':
        await update_user_n_p(message.from_user.id, data['param'])
    elif data['choice_param'] == 'max_price':
        await update_user_x_p(message.from_user.id, data['param'])
    elif data['choice_param'] == 'count_room':
        await update_user_c_r(message.from_user.id, data['param'])
    elif data['choice_param'] == 'min_floor':
        await update_user_n_f(message.from_user.id, data['param'])
    elif data['choice_param'] == 'max_floor':
        await update_user_x_f(message.from_user.id, data['param'])
    elif data['choice_param'] == 'sort':
        await update_user_s(message.from_user.id, data['param'])

    await state.finish()
    await message.answer('✅ Успешно обновлено! ✅', reply_markup=keyboard)


@dp.message_handler(state=registration.city)
async def get_city(message: types.Message, state: FSMContext):
    # добавить проверку на существующий город (config)

    if message.text == 'Пропуск':
        await state.update_data(city=None)
        await message.answer(f'Окей, буду искать в городе по умолчанию.\nУкажите пожалуйста, <b>от</b> какой суммы искать', reply_markup=price_key)
        await registration.min_price.set()
    else:
        await state.update_data(city=message.text)
        await message.answer(f'Принял, буду искать в городе <b>{message.text}</b>.\nУкажите <b>от</b> какой суммы искать', reply_markup=price_key)
        await registration.min_price.set()


@dp.message_handler(state=registration.min_price)
async def get_min_price(message: types.Message, state: FSMContext):

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
                    await message.answer(f'Принял, буду искать от <b>{message.text}</b> грн.\nУкажите <b>до</b> какой суммы искать', reply_markup=price_m_key)
                    await registration.max_price.set()
            else:
                await message.answer('Ошибка\nВведенно не число')
    except Exception:
        await message.answer('Ошибка\nВведены не корректные данные')


@dp.message_handler(state=registration.max_price)
async def get_max_price(message: types.Message, state: FSMContext):

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
                    await message.answer(f'Принял, буду искать кваритиры до <b>{message.text}</b> грн.\nУкажите количество комнат', reply_markup=room_key)
                    await registration.count_rooms.set()
            else:
                await message.answer('Ошибка\nВведенно не число')
    except Exception:
        await message.answer('Ошибка\nВведены не корректные данные')


@dp.message_handler(state=registration.count_rooms)
async def get_count_rooms(message: types.Message, state: FSMContext):
    # исправить 2-3
    try:
        if message.text == 'Пропуск':
            await message.answer('Окей, количество комнат не важно.\nУкажите <b>с</b> какого этажа искать квартиру воспользовавшись клавиатурой или введя вручную но не выше <b>20</b> этажа', reply_markup=floor_n_key)
            await state.update_data(count_rooms=None)
            await registration.min_floor.set()
        else:
            if message.text in ('1', '2', '3', '1-2', '1-3', '2-3'):
                await state.update_data(count_rooms=message.text)
                await message.answer(f'Принял, буду искать {message.text}-х комнатую квартиру\nУкажите <b>с</b> какого этажа искать квартиру воспользовавшись клавиатурой или введя вручную но не выше <b>20</b> этажа', reply_markup=floor_n_key)
                await registration.min_floor.set()
            else:
                await message.answer('не удалось распознать число')
    except:
        await message.answer('Произошла ошибка при вводе количества комнат')


@dp.message_handler(state=registration.min_floor)
async def get_min_floor(message: types.Message, state: FSMContext):

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
                await message.answer('не удалось распознать этаж\nукажите этаж от 1 до 20 включительно')
    except:
        await message.answer('Произошла ошибка при вводе этажа')


@dp.message_handler(state=registration.max_floor)
async def get_max_floor(message: types.Message, state: FSMContext):

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
                await message.answer('не удалось распознать этаж\nукажите этаж от 1 до 20 включительно')
    except:
        await message.answer('Произошла ошибка при вводе этажа')


@dp.message_handler(state=registration.sort)
async def get_sort(message: types.Message, state: FSMContext):

    try:
        if message.text == 'Пропуск':
            await message.answer('Окей, сортировка будет по стандарту', reply_markup=keyboard)
            await state.update_data(sort=None)
        elif message.text in ('Новинки', 'Дешёвые', 'Дорогие'):
            await state.update_data(max_floor=message.text)
            await message.answer(f'Принял, буду искать по {message.text}')
        else:
            # проверить
            await message.answer('Не удалось распознать вид сортировки.\nВыбирите из доступных вам', reply_markup=sort_key)
            raise

        data = await state.get_data()
        if await add_user(message.from_user.id, data.get('city'), data.get('min_price'), data.get('max_price'), data.get('count_rooms'), data.get('min_floor'), data.get('max_floor'), data.get('sort')):
            await message.answer('✅ Вы успешно зарегистрировались ✅', reply_markup=keyboard)
        else:
            await message.answer('Произошла ошибка при сохранении данных', reply_markup=keyboard)
        await state.finish()

    except Exception:
        await message.answer('Произошла ошибка при вводе сортировки\n', traceback.format_exc())
