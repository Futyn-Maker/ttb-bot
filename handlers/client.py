import re
from datetime import datetime
import pytz

from aiogram import types
from aiogram.dispatcher.filters import Text

from bot import db, dp

from handlers.registration import RegistrationForm, on_form_finished
from handlers.history import generate_history

from responses.client_responses import CLIENT_RESPONSES
from responses.history_responses import HISTORY_RESPONSES
from responses.keyboards import ASK_KEYBOARD


moscow_tz = pytz.timezone("Europe/Moscow")

@dp.message_handler(commands="start", state="*")
async def start(message: types.Message):
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer(text=CLIENT_RESPONSES["need_registration"])
        await RegistrationForm.start(callback=on_form_finished)
    else:
        await message.answer(text=CLIENT_RESPONSES["start"], reply_markup=ASK_KEYBOARD)


@dp.message_handler(commands="help", state="*")
async def show_help(message: types.Message):
    await message.answer(text=CLIENT_RESPONSES["help"])


@dp.message_handler(commands="ask", state="*")
async def ask(message: types.Message):
    await message.answer(text=CLIENT_RESPONSES["ask"], reply_markup=ASK_KEYBOARD)


@dp.message_handler(commands="history", state="*")
async def show_history(message: types.Message):
    try:
        user = await db.get_user(message.from_user.id)
        if user:
            user_name, history_text = await generate_history(user)
            await message.answer(text=HISTORY_RESPONSES["history"].format(name=user_name, entries=history_text), parse_mode="HTML")
        else:
            await message.answer(text=HISTORY_RESPONSES["history_empty"])

    except Exception as e:
        await message.answer(HISTORY_RESPONSES["history_error"].format(error=e))


@dp.message_handler(commands="reminders")
async def toggle_reminders(message: types.Message):
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer(text=CLIENT_RESPONSES["need_registration"])
        await RegistrationForm.start(callback=on_form_finished)
    else:
        notifications_wanted = not user["notifications_wanted"]
        await db.update_notifications_wanted(user["id"], notifications_wanted)
        answer = CLIENT_RESPONSES["reminders_true"] if notifications_wanted else CLIENT_RESPONSES["reminders_false"]
        await message.answer(answer)


@dp.message_handler()
async def save_message(message: types.Message):
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer(text=CLIENT_RESPONSES["need_registration"])
        await RegistrationForm.start(callback=on_form_finished)
    else:
        lines = message.text.split("\n")
        for line in lines:
            if not line:
                continue
            match = re.match(r"(\d{2}[:.]\d{2})-?(\d{2}[:.]\d{2})?:? (.+)", line)
            current_date = datetime.now(moscow_tz).strftime("%Y-%m-%d")
            timestamp_start = f"{current_date} {match.group(1)}:00".replace(".", ":") if match else datetime.now(moscow_tz).strftime("%Y-%m-%d %H:%M:%S")
            timestamp_end = f"{current_date} {match.group(2)}:00".replace(".", ":") if match and match.group(2) else None
            text = match.group(3) if match else line
            await db.add_response(user["id"], timestamp_start, timestamp_end, text)
        await message.answer(CLIENT_RESPONSES["message_saved"])
