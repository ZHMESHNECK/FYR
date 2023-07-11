from utils.db.testdb import User
from asyncpg import UniqueViolationError


async def add_user(user_id: int,city: str):
    try:
        user = User(user_id=user_id,city=city)
        await user.create()
    except UniqueViolationError:
        print('не удалось создать юзера')

async def sel_all():
    users = await User.query.gino.all()
    return users

async def select_u(user_id):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user

async def update_u(user_id, new_name):
    user = await select_u(user_id)
    await user.update(city=new_name).apply()