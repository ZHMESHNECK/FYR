from utils.db.dbb import db
from config import POSTGRES_URI
from utils.db.reg_commands import *
import asyncio


async def test():
    await db.set_bind(POSTGRES_URI)
    da = await select_user(545434691)
    print(da.city)

    

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
