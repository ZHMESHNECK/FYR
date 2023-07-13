from utils.db.schemas.reg_model import User_model
from asyncpg import UniqueViolationError


async def add_user(user_id: int, city: str, min_price: int, max_price: int, count_rooms: int, min_floor: int, max_floor: int, sort: str):
    try:
        user = User_model(user_id=user_id, city=city, min_price=min_price, max_price=max_price,
                          count_rooms=count_rooms, min_floor=min_floor, max_floor=max_floor, sort=sort)
        await user.create()
    except UniqueViolationError:
        print('не удалось создать юзера')


async def sel_all():
    users = await User_model.query.gino.all()
    return users


async def select_user(user_id):
    user = await User_model.query.where(User_model.user_id == user_id).gino.first()
    return user


async def update_u(user_id, new_name):
    user = await select_user(user_id)
    await user.update(city=new_name).apply()
