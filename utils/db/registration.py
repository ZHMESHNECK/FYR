from utils.db.schemas.temporary_storage import registration, temp_reg
from aiogram.dispatcher import FSMContext
from utils.db.reg_commands import *
from config import POSTGRES_URI
from utils.keyboards import *
from utils.db.dbb import db
from aiogram import types
from utils.check import *
from config import dp
import traceback


async def check_register(message: types.Message):
    try:
        await db.set_bind(POSTGRES_URI)
        user = await select_user(message.from_user.id)
        if not user:
            await message.answer('У вас ещё нет заданных параметров\nдавайте пройдём маленькую регистрацию ☺️', reply_markup=city_key)
            await start_reg(message)
        else:
            if check_time(user.time):
                return (user, None)
            time = user.time - datetime.now()
            return (user, int(time.seconds))
    except:
        await message.answer('Не удалось подключиться к базе данных', traceback.format_exc())


async def start_reg(message: types.Message):
    await message.answer('Для начала введите город в котором искать', reply_markup=city_key)
    await registration.city.set()


async def show_parametrs(message: types.Message, user):
    await message.answer(f'🛠 Параметры 🛠:\n'
                         f'\n<b>Город</b> - {user.city if user.city is not None else "Не указано"}\n'
                         f'\n<b>Мин. цена</b> - {str(user.min_price) + " грн" if user.min_price is not None else "Не указано"}\n'
                         f'\n<b>Макс. цена</b> - {str(user.max_price) + " грн" if user.max_price is not None else "Не указано"}\n'
                         f'\n<b>Кол. комнат</b> - {user.count_rooms if user.count_rooms is not None else "Не указано"}\n'
                         f'\n<b>Мин. этаж</b> - {user.min_floor if user.min_floor is not None else "Не указано"}\n'
                         f'\n<b>Макс. этаж</b> - {user.max_floor if user.max_floor is not None else "Не указано"}\n'
                         f'\n<b>Сортировка</b> - {user.sort if user.sort is not None else "Не указано"}\n', reply_markup=view_param)


@dp.message_handler(state=temp_reg.choice_param)
async def single_change(message: types.Message, state: FSMContext):
    await db.set_bind(POSTGRES_URI)
    user = await select_user(message.from_user.id)
    data = {'Город': 'city', 'Кол. комнат': 'count_rooms',
            'Мин. цена': 'min_price', 'Макс. цена': 'max_price', 'Мин. этаж': 'min_floor', 'Макс. этаж': 'max_floor', 'Сортировка': 'sort'}
    data_2 = {'city': [user.city, city_key],
              'min_price': [user.min_price, price_n_key],
              'max_price': [user.max_price, price_x_key],
              'count_rooms': [user.count_rooms, room_key],
              'min_floor': [user.min_floor, floor_n_key],
              'max_floor': [user.max_floor, floor_x_key],
              'sort': [user.sort, sort_key]}
    param = data.get(message.text)

    if message.text == 'Отмена':
        await message.answer('Отменено', reply_markup=keyboard)
        await state.update_data(choice_param=None)
        await state.finish()
    elif param:
        await message.answer(f'Меняем {message.text} - <b>{data_2[param][0]}</b> на:', reply_markup=data_2[param][1])
        await state.update_data(choice_param=param)
        await temp_reg.param.set()


@dp.message_handler(state=temp_reg.param)
async def single_change_2(message: types.Message, state: FSMContext):
    await state.update_data(param=message.text)
    data = await state.get_data()
    try:
        if data['choice_param'] == 'city':
            if data['param'] == 'Пропуск':
                await update_user_c(message.from_user.id, None)
            elif check_city(data['param']):
                await update_user_c(message.from_user.id, data['param'])
            else:
                await message.answer('Не удалось распознать город для поиска.\nИспользуйте доступные города предложенные на клавиатуре 👇', reply_markup=city_key)
                return
            await state.finish()
        elif data['choice_param'] == 'min_price':
            if data['param'] == 'Пропуск':
                await update_user_n_p(message.from_user.id, None)
            elif check_num(data['param']):
                await update_user_n_p(message.from_user.id, int("".join(data['param'].replace('.', ''))))
            else:
                await message.answer('Не удалось распознать число', reply_markup=price_n_key)
                return
            await state.finish()
        elif data['choice_param'] == 'max_price':
            if data['param'] == 'Пропуск':
                await update_user_x_p(message.from_user.id, None)
            elif check_num(data['param']):
                if await update_user_x_p(message.from_user.id, int("".join(data['param'].replace('.', '')))):
                    pass
                else:
                    await message.answer('Минимальное число не может быть больше максимального', reply_markup=price_x_key)
                    return
            else:
                await message.answer('Не удалось распознать число', reply_markup=price_x_key)
                return
            await state.finish()
        elif data['choice_param'] == 'count_rooms':
            if data['param'] == 'Пропуск':
                await update_user_c_r(message.from_user.id, None)
            elif check_c_room(data['param']):
                await update_user_c_r(message.from_user.id, data['param'])
            else:
                await message.answer('Не удалось распознать количество комнат', reply_markup=room_key)
                return
            await state.finish()
        elif data['choice_param'] == 'min_floor':
            if data['param'] == 'Пропуск':
                await update_user_n_f(message.from_user.id, None)
            elif check_num(data['param']) and check_floor(data['param']):
                await update_user_n_f(message.from_user.id, int(data['param']))
            else:
                await message.answer('Не удалось распознать число', reply_markup=floor_n_key)
                return
            await state.finish()
        elif data['choice_param'] == 'max_floor':
            if data['param'] == 'Пропуск':
                await update_user_x_f(message.from_user.id, None)
            elif check_num(data['param']) and check_floor(data['param']):
                if await update_user_x_f(message.from_user.id, int(data['param'])):
                    pass
                else:
                    await message.answer('Минимальное число не может быть больше максимального', reply_markup=floor_x_key)
                    return
            else:
                await message.answer('Не удалось распознать число', reply_markup=floor_x_key)
                return
            await state.finish()
        elif data['choice_param'] == 'sort':
            if data['param'] == 'Пропуск':
                await update_user_s(message.from_user.id, None)
            elif check_sort(data['param']):
                await update_user_s(message.from_user.id, data['param'])
            else:
                await message.answer('Не удалось распознать сортировку', reply_markup=sort_key)
                return
            await state.finish()
    except:
        await message.answer('При обновлении данных произошла ошибка', traceback.format_exc())
        await state.finish()
        return

    await message.answer('✅ Успешно обновлено! ✅', reply_markup=keyboard)


@dp.message_handler(state=registration.city)
async def get_city(message: types.Message, state: FSMContext):

    if check_city(message.text):
        await state.update_data(city=message.text)
        await message.answer(f'Принял, буду искать в городе <b>{message.text}</b>.\nУкажите <b>от</b> какой суммы искать', reply_markup=price_n_key)
        await registration.min_price.set()
    else:
        await message.answer('Не удалось распознать город для поиска.\nИспользуйте доступные города предложенные на клавиатуре 👇')


@dp.message_handler(state=registration.min_price)
async def get_min_price(message: types.Message, state: FSMContext):

    try:
        if message.text == 'Пропуск':
            await message.answer('Окей, начальная цена не важна.\nУкажите <b>до</b> какой суммы искать', reply_markup=price_x_key)
            await state.update_data(min_price=None)
            await registration.max_price.set()
        else:
            if check_num(message.text):
                num = int("".join(message.text.replace('.', '')))
                if num < 2000 or num > 50000:
                    await message.answer('Ошибка\nЧисло выходит из допустимого диапазона', reply_markup=price_n_key)
                else:
                    await state.update_data(min_price=num)
                    await message.answer(f'Принял, буду искать от <b>{message.text}</b> грн.\nУкажите <b>до</b> какой суммы искать', reply_markup=price_x_key)
                    await registration.max_price.set()
            else:
                await message.answer('Ошибка\nВведенно не число', reply_markup=price_n_key)
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
            if check_num(message.text):
                num = int("".join(message.text.replace('.', '')))
                if num < 2000 and num > 60000:
                    await message.answer('Ошибка\nЧисла выходит из допустимого диапазона', reply_markup=price_x_key)
                else:
                    data = await state.get_data()
                    if check_max_min(num, data.get('min_price')):
                        await state.update_data(max_price=num)
                        await message.answer(f'Принял, буду искать кваритиры до <b>{message.text}</b> грн.\nУкажите количество комнат', reply_markup=room_key)
                        await registration.count_rooms.set()
                    else:
                        await message.answer('Минимальное число не может быть больше максимального', reply_markup=price_x_key)
            else:
                await message.answer('Ошибка\nВведенно не число', reply_markup=price_x_key)
    except Exception:
        await message.answer('Ошибка\nВведены не корректные данные', traceback.format_exc())


@dp.message_handler(state=registration.count_rooms)
async def get_count_rooms(message: types.Message, state: FSMContext):
    try:
        if message.text == 'Пропуск':
            await message.answer('Окей, количество комнат не важно.\nУкажите <b>с</b> какого этажа искать квартиру воспользовавшись клавиатурой или введя вручную но не выше <b>20</b> этажа', reply_markup=floor_n_key)
            await state.update_data(count_rooms=None)
            await registration.min_floor.set()
        else:
            if check_c_room(message.text):
                await state.update_data(count_rooms=message.text)
                await message.answer(f'Принял, буду искать {message.text}-х комнатую квартиру\nУкажите <b>с</b> какого этажа искать квартиру воспользовавшись клавиатурой или введя вручную но не выше <b>20</b> этажа', reply_markup=floor_n_key)
                await registration.min_floor.set()
            else:
                await message.answer('не удалось распознать число', reply_markup=room_key)
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
            if check_floor(message.text):
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
            if check_floor(message.text):
                data = await state.get_data()
                if check_max_min(int(message.text), data.get('min_floor')):
                    await state.update_data(max_floor=int(message.text))
                    await message.answer(f'Принял, буду искать до {message.text} этажа.\nУкажите сортировку объявлений', reply_markup=sort_key)
                    await registration.sort.set()
                else:
                    await message.answer('Минимальное число не может быть больше максимального', reply_markup=floor_x_key)
            else:
                await message.answer('не удалось распознать этаж\nукажите этаж от 1 до 20 включительно', reply_markup=floor_x_key)
    except:
        await message.answer('Произошла ошибка при вводе этажа')


@dp.message_handler(state=registration.sort)
async def get_sort(message: types.Message, state: FSMContext):

    try:
        if message.text == 'Пропуск':
            await message.answer('Окей, сортировка будет по стандарту', reply_markup=keyboard)
            await state.update_data(sort=None)
        elif check_sort(message.text):
            await state.update_data(sort=message.text)
            await message.answer(f'Принял, буду искать по {message.text}', reply_markup=keyboard)
        else:
            await message.answer('Не удалось распознать вид сортировки.\nВыбирите из доступных вам', reply_markup=sort_key)
            return
        data = await state.get_data()
        if await add_user(message.from_user.id, data.get('city'), data.get('min_price'), data.get('max_price'), data.get('count_rooms'), data.get('min_floor'), data.get('max_floor'), data.get('sort')):
            await message.answer('✅ Вы успешно зарегистрировались ✅', reply_markup=keyboard)
            await state.finish()
        else:
            await message.answer('Произошла ошибка при сохранении данных', reply_markup=keyboard)

    except Exception:
        await message.answer('Произошла ошибка при вводе сортировки\n', traceback.format_exc())
