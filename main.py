from utils.db.dbb import db
from config import POSTGRES_URI
from utils.db.reg_commands import *
import asyncio


async def test():
    await db.set_bind(POSTGRES_URI)
    await db.gino.drop_all()
    await db.gino.create_all()

    await add_user(123, 'kiev', 3000, 4000, '1-2', None, None, None)

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
