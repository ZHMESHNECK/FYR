from aiogram.dispatcher.filters.state import StatesGroup, State

class registration(StatesGroup):
    """
    временное хранилище данных пока идёт регистрация юзера
    """    
    user_id = State()
    city = State()
    min_price = State()
    max_price = State()
    count_rooms = State()
    min_floor = State()
    max_floor = State()
    sort = State()

class temp_reg(StatesGroup):
    """
    временное хранилище данных пока юзер меняет данные
    """    
    choice_param = State()
    param = State()