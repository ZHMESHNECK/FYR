from utils.db.dbb import db,POSTGRES_URI
from utils.db import com
import asyncio
##
# https://www.youtube.com/watch?v=dcbuQMjHj_c&t=240s
# https://www.youtube.com/watch?v=rgmehqKzWO0

async def db_test():
    await db.set_bind(POSTGRES_URI)
    await db.gino.drop_all()
    await db.gino.create_all()

    await com.add_user(1, 'da')
    await com.add_user(3, 'asdasd')
    await com.add_user(4, 'dxzxczxc')
    await com.add_user(5, 'rrrrr')

    count = await com.sel_all()
    print(count)

    users = await com.select_u(1)
    print(users)

    await com.update_u(1, 'net')

    users = await com.select_u(1)
    print(users)

loop = asyncio.get_event_loop()
loop.run_until_complete(db_test())