from utils.db.schemas.reg_model import User_model
from asyncpg import UniqueViolationError


async def add_user(user_id: int, city: str or None, min_price: int or None, max_price: int or None, count_rooms: str or None, min_floor: int or None, max_floor: int or None, sort: str or None):
    try:
        user = User_model(user_id=user_id, city=city, min_price=min_price, max_price=max_price,
                          count_rooms=count_rooms, min_floor=min_floor, max_floor=max_floor, sort=sort)
        await user.create()
        return True
    except UniqueViolationError:
        print('Юзер уже существует')


async def sel_all():
    return await User_model.query.gino.all()


async def select_user(user_id):
    return await User_model.query.where(User_model.user_id == user_id).gino.first()


async def update_user_c(user_id, param):
    user = await select_user(user_id)
    await user.update(city=param).apply()


async def update_user_n_p(user_id, param):
    user = await select_user(user_id)
    await user.update(min_price=param).apply()

async def update_user_x_p(user_id, param):
    user = await select_user(user_id)
    await user.update(max_price=param).apply()


async def update_user_c_r(user_id, param):
    user = await select_user(user_id)
    await user.update(count_room=param).apply()


async def update_user_n_f(user_id, param):
    user = await select_user(user_id)
    await user.update(min_floor=param).apply()


async def update_user_x_f(user_id, param):
    user = await select_user(user_id)
    await user.update(max_floor=param).apply()


async def update_user_s(user_id, param):
    user = await select_user(user_id)
    await user.update(sort=param).apply()
