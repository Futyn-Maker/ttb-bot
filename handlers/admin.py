from datetime import datetime
import pytz

from aiogram import types
from aiogram.dispatcher.filters import Text

from bot import db, dp

from handlers.history import generate_history

from responses.admin_responses import ADMIN_RESPONSES
from responses.client_responses import CLIENT_RESPONSES
from responses.keyboards import ASK_KEYBOARD


moscow_tz = pytz.timezone("Europe/Moscow")

@dp.message_handler(commands="askall")
async def ask_all(message: types.Message):
    await message.answer(ADMIN_RESPONSES["ask_all_progress"])

    async for user in db.get_all_users():
        if user["tg_id"] == message.from_user.id:
            continue

        try:
            await dp.bot.send_message(chat_id=user["tg_id"], text=CLIENT_RESPONSES["ask"], reply_markup=ASK_KEYBOARD)
            success_message = ADMIN_RESPONSES["ask_all_success"].format(datetime.now(moscow_tz).isoformat(), user["tg_name"])
            await message.answer(text=success_message)
        except Exception as e:
            failure_message = ADMIN_RESPONSES["ask_all_failure"].format(datetime.now(moscow_tz).isoformat(), user["tg_name"])
            await message.answer(text=failure_message)


@dp.message_handler(commands="historyall")
async def show_all_history(message: types.Message):
    try:
        entries = []
        async for user in db.get_all_users():
            entry = await generate_history(user)
            entries.append(CLIENT_RESPONSES["history"].format(name=entry[0], entries=entry[1]))
        await message.answer(text="\n\n".join(entries), parse_mode="HTML")

    except Exception as e:
        await message.answer(CLIENT_RESPONSES["history_error"].format(error=e))
