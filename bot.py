from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers.db import Db

from config import API_TOKEN

db = Db()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
