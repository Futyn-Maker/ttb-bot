from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# Buttons for ask_keyboard
_button_lesson = KeyboardButton("🔍 Урок")
_button_preparation = KeyboardButton("😎 Подготовка")
_button_journal = KeyboardButton("☸ Журнал")
_button_work_with_kids = KeyboardButton("📞 Работа с детьми")
_button_parents = KeyboardButton("📢 Родители")
_button_meeting = KeyboardButton("⭐️ Совещание")
_button_check_work = KeyboardButton("👥 Проверка работ")

ASK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
ASK_KEYBOARD.add(_button_lesson, _button_preparation)
ASK_KEYBOARD.add(_button_journal, _button_work_with_kids)
ASK_KEYBOARD.add(_button_parents, _button_meeting, _button_check_work)
