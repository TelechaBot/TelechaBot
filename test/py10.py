# -*- coding: utf-8 -*-
# @Time    : 10/16/22 1:40 PM
# @FileName: py10.py
# @Software: PyCharm
# @Github    ：sudoskys
import asyncio
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()



async def unbanUser(chat, user):
    print(chat)
    print(user)


user = 123
group = -1000


async def main():
    scheduler.add_job(
        unbanUser,
        args=[group, user],
        trigger='date',
        run_date=datetime.datetime.now() + datetime.timedelta(seconds=3)
    )
    scheduler.add_job(func=unbanUser, args=(10, 2), trigger='date',
                      run_date=datetime.datetime.now() + datetime.timedelta(seconds=3))
    print(213)
    scheduler.start()
    await asyncio.sleep(110)


asyncio.run(main())
# aioschedule.every(360).seconds.do(unbanUser, group, user).tag(str(user * abs(group)))
