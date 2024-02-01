import logging
import asyncio

from aiogram.utils import executor

import aiocron

from handlers import admin, client

from bot import dp

from config import ASKALL_CRONTAB


logging.basicConfig(level=logging.DEBUG)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

@aiocron.crontab(ASKALL_CRONTAB)
async def scheduled_ask_all():
    await admin.ask_all()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
