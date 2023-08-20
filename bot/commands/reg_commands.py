from asyncpg.exceptions import UndefinedTableError
from db.schemas.dbb import User_model
from asyncpg import UniqueViolationError
from commands.check import check_max_min
from config import POSTGRES_URI
from db.schemas.dbb import db


# подключение и отключение связи с БД
def open_db(func):
    """
    Функция-декоратор которая устанавливает связь с БД, запускает функцию wrapper и после её выполнения прерывает связь

    Args:
        func (_type_): функция
    """    
    async def wrapper(*args, **kwargs):
        try:
            async with db.with_bind(POSTGRES_URI):
                return await func(*args)
        # если таблицы не существует - создаём
        except UndefinedTableError:
            async with db.with_bind(POSTGRES_URI):
                await db.gino.create_all()
                return await func(*args)
    return wrapper

@open_db
async def add_user(user_id: int, city: str or None, min_price: int or None, max_price: int or None, count_rooms: str or None, min_floor: int or None, max_floor: int or None, sort: str or None):
    """
    Добавляет модель юзера в БД

    Args:
        user_id (int): id юзера в телеграм
        city (strorNone): город
        min_price (intorNone): минимальная цена поиска
        max_price (intorNone): максимальная цена поиска
        count_rooms (strorNone): количество комнат
        min_floor (intorNone): минимальный этаж
        max_floor (intorNone): максимальный этаж
        sort (strorNone): сортировка объявлений

    Returns:
        _type_: True if успешно добавлено
    """    
    try:
        user = User_model(user_id=user_id, city=city, min_price=min_price, max_price=max_price,
                          count_rooms=count_rooms, min_floor=min_floor, max_floor=max_floor, sort=sort)
        await user.create()
        return True
    except UniqueViolationError:
        print('Юзер уже существует')


@open_db
async def select_user(user_id):
    """ 
    Возвращает модель юзера
    """
    return await User_model.query.where(User_model.user_id == user_id).gino.first()

# city
@open_db
async def update_user_c(user_id, param):
    """Обновляет параметр города в модели юзера

    Args:
        user_id (_type_): user_id
        param (_type_): параметр который устанавливаем
    """    
    user = await User_model.query.where(User_model.user_id == user_id).gino.first()
    await user.update(city=param).apply()

# min_price
@open_db
async def update_user_n_p(user_id, param):
    """
    Обновляет параметр мин. цены в модели юзера

    Args:
        user_id (_type_): user_id
        param (_type_): параметр который устанавливаем

    Returns:
        _type_: если проверка на валидность данных пройдена True else False
    """    
    user = await User_model.query.where(User_model.user_id == user_id).gino.first()
    if check_max_min(user.max_price, param):
        await user.update(min_price=param).apply()
        return True
    return False

# max_price
@open_db
async def update_user_x_p(user_id, param):
    """
    Обновляет параметр макс. цены в модели юзера

    Args:
        user_id (_type_): user_id
        param (_type_): параметр который устанавливаем

    Returns:
        _type_: если проверка на валидность данных пройдена True else False
    """  
    user = await User_model.query.where(User_model.user_id == user_id).gino.first()
    if check_max_min(param, user.min_price):
        await user.update(max_price=param).apply()
        return True
    return False

# count_room
@open_db
async def update_user_c_r(user_id, param):
    """
    Обновляет параметр количество комнат в модели юзера
    
    Args:
        user_id (_type_): user_id
        param (_type_): параметр который устанавливаем
    """    
    user = await User_model.query.where(User_model.user_id == user_id).gino.first()
    await user.update(count_rooms=param).apply()

# min_floor
@open_db
async def update_user_n_f(user_id, param):
    """
    Обновляет параметр мин. этажа в модели юзера

    Args:
        user_id (_type_): user_id
        param (_type_): параметр который устанавливаем

    Returns:
        _type_: если проверка на валидность данных пройдена True else False
    """    
    user = await User_model.query.where(User_model.user_id == user_id).gino.first()
    if check_max_min(user.max_floor, param):
        await user.update(min_floor=param).apply()
        return True
    return False

# max_floor
@open_db
async def update_user_x_f(user_id, param):
    """
    Обновляет параметр макс. этажа в модели юзера

    Args:
        user_id (_type_): user_id
        param (_type_): параметр который устанавливаем

    Returns:
        _type_: если проверка на валидность данных пройдена True else False
    """    
    user = await User_model.query.where(User_model.user_id == user_id).gino.first()
    if check_max_min(param, user.min_floor):
        await user.update(max_floor=param).apply()
        return True
    return False

# sort
@open_db
async def update_user_s(user_id, param):
    """
    Обновляет параметр сортировку в модели юзера

    Args:
        user_id (_type_): user_id
        param (_type_): параметр который устанавливаем
    """    
    user = await User_model.query.where(User_model.user_id == user_id).gino.first()
    await user.update(sort=param).apply()

@open_db
async def update_time(user_id, param):
    """
    Обновляет параметр время в модели юзера

    Args:
        user_id (_type_): user_id
        param (_type_): параметр который устанавливаем
    """    
    user = await User_model.query.where(User_model.user_id == user_id).gino.first()
    await user.update(time=param).apply()
