from aiogram import Bot, Dispatcher

from handlers.db import Db

from config import API_TOKEN


db = Db()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
